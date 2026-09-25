/**
 * Lesson 2.2: prepare an S3-compatible bucket for Beacon, in code rather than
 * by clicking in a console. Only for STORAGE_DRIVER=s3 (the local driver
 * needs no setup).
 *
 *   npm run storage:setup
 *
 * - creates the bucket if it does not exist;
 * - blocks public access where the store supports it (AWS S3; others are
 *   private unless you open them);
 * - allows the browser at APP_URL to PUT and GET with presigned URLs (CORS),
 *   which direct uploads need.
 */
import './load-env'; // lesson 7.4: .env.local, like Next.js (must be the first import)
import {
  CreateBucketCommand,
  HeadBucketCommand,
  PutBucketCorsCommand,
  PutPublicAccessBlockCommand,
} from '@aws-sdk/client-s3';
import { s3Client, s3ConfigFromEnv } from '../src/lib/storage/s3';

const config = s3ConfigFromEnv();
const s3 = s3Client(config);
const Bucket = config.bucket;
const appUrl = process.env.APP_URL ?? 'http://localhost:3000';

try {
  await s3.send(new HeadBucketCommand({ Bucket }));
  console.log(`• bucket ${Bucket} exists`);
} catch {
  await s3.send(new CreateBucketCommand({ Bucket }));
  console.log(`✓ created bucket ${Bucket}`);
}

try {
  await s3.send(
    new PutPublicAccessBlockCommand({
      Bucket,
      PublicAccessBlockConfiguration: { BlockPublicAcls: true, IgnorePublicAcls: true, BlockPublicPolicy: true, RestrictPublicBuckets: true },
    }),
  );
  console.log('✓ public access blocked');
} catch (err) {
  console.log(`• public access block not supported here (${(err as Error).name}); keep the bucket private in its own settings`);
}

await s3.send(
  new PutBucketCorsCommand({
    Bucket,
    CORSConfiguration: {
      CORSRules: [{ AllowedOrigins: [new URL(appUrl).origin], AllowedMethods: ['PUT', 'GET'], AllowedHeaders: ['content-type'], MaxAgeSeconds: 3600 }],
    },
  }),
);
console.log(`✓ CORS: ${new URL(appUrl).origin} may PUT and GET with presigned URLs`);
