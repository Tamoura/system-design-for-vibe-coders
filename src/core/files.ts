/*
 * Lesson 2.2: the rules for user uploads, as pure functions (no I/O), so they
 * are easy to test and the same rules run before signing and after upload.
 *
 * Only raster images are accepted. SVG is deliberately missing: an SVG is a
 * document that can carry <script>, and serving one from Beacon's domain is
 * stored XSS (lesson 2.2, "Validation happens on the server, twice").
 */

import type { Permission } from './permissions';

export const FILE_KINDS = ['logo', 'incident_screenshot'] as const;
export type FileKind = (typeof FILE_KINDS)[number];

/** Who may upload what (lesson 1.3's permissions): logos are part of the status page, owners and admins only. */
export const UPLOAD_PERMISSION: Record<FileKind, Permission> = {
  logo: 'page.publish',
  incident_screenshot: 'incident.write',
};

export const IMAGE_TYPES = {
  'image/png': ['.png'],
  'image/jpeg': ['.jpg', '.jpeg'],
  'image/webp': ['.webp'],
} as const;
export type ImageType = keyof typeof IMAGE_TYPES;

const MB = 1024 * 1024;

export const UPLOAD_RULES: Record<FileKind, { maxBytes: number; types: readonly ImageType[]; folder: string }> = {
  logo: { maxBytes: 2 * MB, types: ['image/png', 'image/jpeg', 'image/webp'], folder: 'logos' },
  incident_screenshot: { maxBytes: 5 * MB, types: ['image/png', 'image/jpeg', 'image/webp'], folder: 'screenshots' },
};

/** Presigned URLs live for minutes, not days: they get pasted into chats. */
export const UPLOAD_URL_TTL_SECONDS = 5 * 60;
export const DOWNLOAD_URL_TTL_SECONDS = 5 * 60;

export type UploadRefusal = 'too_large' | 'empty' | 'type_not_allowed' | 'extension_mismatch';

export const REFUSAL_MESSAGES: Record<UploadRefusal | 'not_uploaded' | 'content_mismatch' | 'size_mismatch', string> = {
  too_large: 'That file is too large.',
  empty: 'That file is empty.',
  type_not_allowed: 'Only PNG, JPEG and WebP images can be uploaded.',
  extension_mismatch: 'The file name does not match its type.',
  not_uploaded: 'The upload did not arrive. Try again.',
  content_mismatch: 'That file is not the image it claims to be.',
  size_mismatch: 'The uploaded file is not the size that was announced.',
};

/**
 * Before signing (🟢): check what the browser *declares*. The browser can
 * lie, so this is only the first of two checks; completeUpload() looks at the
 * real bytes. Returns null when the request is acceptable.
 */
export function checkUploadRequest(kind: FileKind, file: { name: string; type: string; size: number }): UploadRefusal | null {
  const rules = UPLOAD_RULES[kind];
  if (file.size <= 0) return 'empty';
  if (file.size > rules.maxBytes) return 'too_large';
  if (!(rules.types as readonly string[]).includes(file.type)) return 'type_not_allowed';
  const extensions: readonly string[] = IMAGE_TYPES[file.type as ImageType];
  if (!extensions.some((ext) => file.name.toLowerCase().endsWith(ext))) return 'extension_mismatch';
  return null;
}

/**
 * After upload (🟡): what the bytes really are, from their "magic number" —
 * the first few bytes every PNG, JPEG and WebP file starts with. The same idea
 * as the `file-type` npm package, for the three formats Beacon accepts.
 * Needs at least the first 12 bytes; returns null for anything else.
 */
export function sniffImageType(bytes: Uint8Array): ImageType | null {
  const starts = (sig: number[], offset = 0) => sig.every((b, i) => bytes[offset + i] === b);
  if (starts([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) return 'image/png';
  if (starts([0xff, 0xd8, 0xff])) return 'image/jpeg';
  if (starts([0x52, 0x49, 0x46, 0x46]) && starts([0x57, 0x45, 0x42, 0x50], 8)) return 'image/webp'; // "RIFF"…"WEBP"
  return null;
}
export const SNIFF_BYTES = 12;

/**
 * Keys are ours, never the user's file name (which can contain "../",
 * unicode or collisions): orgs/{orgId}/{folder}/{fileId}. The org prefix makes
 * per-tenant deletion, usage reports and bucket policies simple (lesson 2.2,
 * "Per-tenant key prefixes").
 */
export function objectKey(orgId: string, kind: FileKind, fileId: string): string {
  return `orgs/${orgId}/${UPLOAD_RULES[kind].folder}/${fileId}`;
}

export function thumbnailKey(key: string): string {
  return `${key}.thumb.webp`;
}

const UUID = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}';
// Lesson 8.1: plus orgs/<org>/exports/<export id>.json, the organization's data export.
const KEY_PATTERN = new RegExp(`^orgs/(${UUID})/(?:(?:logos|screenshots)/${UUID}(?:\\.thumb\\.webp)?|exports/${UUID}\\.json)$`);

/** Is this a key Beacon could have generated? (Also the local driver's guard against path tricks.) */
export function isValidKey(key: string): boolean {
  return KEY_PATTERN.test(key);
}

/** A cheap guard against id-swapping bugs: signing code asserts the key is under the caller's org. */
export function keyBelongsToOrg(key: string, orgId: string): boolean {
  const match = KEY_PATTERN.exec(key);
  return match !== null && match[1] === orgId;
}
