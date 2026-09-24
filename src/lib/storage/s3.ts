import {
  DeleteObjectCommand,
  GetObjectCommand,
  HeadObjectCommand,
  PutObjectCommand,
  S3Client,
  S3ServiceException,
} from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import type { Storage } from './index';

export type S3Config = {
  bucket: string;
  region: string;
  endpoint?: string;
  forcePathStyle: boolean;
  accessKeyId?: string;
  secretAccessKey?: string;
};

export function s3ConfigFromEnv(): S3Config {
  const bucket = process.env.S3_BUCKET;
  if (!bucket) throw new Error('STORAGE_DRIVER=s3 needs S3_BUCKET (see .env.example)');
  return {
    bucket,
    region: process.env.S3_REGION ?? 'auto', // "auto" is what R2 expects; AWS wants a real region
    endpoint: process.env.S3_ENDPOINT || undefined, // unset = AWS itself
    forcePathStyle: process.env.S3_FORCE_PATH_STYLE === 'true', // most self-hosted stores need it
    accessKeyId: process.env.S3_ACCESS_KEY_ID,
    secretAccessKey: process.env.S3_SECRET_ACCESS_KEY,
  };
}

export function s3Client(config: S3Config): S3Client {
  return new S3Client({
    region: config.region,
    endpoint: config.endpoint,
    forcePathStyle: config.forcePathStyle,
    credentials: config.accessKeyId && config.secretAccessKey ? { accessKeyId: config.accessKeyId, secretAccessKey: config.secretAccessKey } : undefined,
  });
}

/**
 * Lesson 2.2: the S3 API, so the same code runs against AWS, R2, Garage or
 * SeaweedFS by changing an endpoint and credentials ("don't hard-code AWS").
 */
export function createS3Storage(config: S3Config = s3ConfigFromEnv()): Storage {
  const s3 = s3Client(config);
  const Bucket = config.bucket;
  const notFound = (err: unknown) => err instanceof S3ServiceException && (err.$metadata.httpStatusCode === 404 || err.name === 'NotFound' || err.name === 'NoSuchKey');

  return {
    signUpload(key, contentType, expiresIn) {
      // ContentType is part of the signature: S3 refuses the PUT if the browser
      // sends another type. Size is NOT limited by a presigned PUT; that is
      // why completeUpload() checks the real size afterwards (a presigned POST
      // with a content-length-range policy is the alternative).
      return getSignedUrl(s3, new PutObjectCommand({ Bucket, Key: key, ContentType: contentType }), { expiresIn });
    },
    signDownload(key, expiresIn) {
      return getSignedUrl(s3, new GetObjectCommand({ Bucket, Key: key }), { expiresIn });
    },
    async head(key) {
      try {
        const res = await s3.send(new HeadObjectCommand({ Bucket, Key: key }));
        return { size: res.ContentLength ?? 0, contentType: res.ContentType ?? null };
      } catch (err) {
        if (notFound(err)) return null;
        throw err;
      }
    },
    async readStart(key, length) {
      const res = await s3.send(new GetObjectCommand({ Bucket, Key: key, Range: `bytes=0-${length - 1}` }));
      return (await res.Body?.transformToByteArray()) ?? new Uint8Array();
    },
    async get(key) {
      const res = await s3.send(new GetObjectCommand({ Bucket, Key: key }));
      return (await res.Body?.transformToByteArray()) ?? new Uint8Array();
    },
    async put(key, bytes, contentType) {
      await s3.send(new PutObjectCommand({ Bucket, Key: key, Body: bytes, ContentType: contentType }));
    },
    async delete(key) {
      await s3.send(new DeleteObjectCommand({ Bucket, Key: key }));
    },
  };
}
