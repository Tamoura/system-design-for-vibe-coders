import { describe, expect, it } from 'vitest';
import { checkUploadRequest, isValidKey, keyBelongsToOrg, objectKey, sniffImageType, thumbnailKey } from '@/core/files';

/* Lesson 2.2: the upload rules, before signing and after upload. */

const ORG = '0190a6f2-1111-4222-8333-444455556666';
const OTHER = '0190a6f2-9999-4222-8333-444455556666';
const FILE = '0190a6f2-aaaa-4bbb-8ccc-dddddddddddd';

describe('checkUploadRequest (before a URL is signed)', () => {
  it('accepts a small PNG logo', () => {
    expect(checkUploadRequest('logo', { name: 'acme.png', type: 'image/png', size: 40_000 })).toBeNull();
    expect(checkUploadRequest('logo', { name: 'ACME.JPEG', type: 'image/jpeg', size: 40_000 })).toBeNull();
  });

  it('rejects a 10 MB file', () => {
    expect(checkUploadRequest('logo', { name: 'huge.png', type: 'image/png', size: 10 * 1024 * 1024 })).toBe('too_large');
    expect(checkUploadRequest('incident_screenshot', { name: 'huge.png', type: 'image/png', size: 10 * 1024 * 1024 })).toBe('too_large');
  });

  it('rejects an .exe, whatever type it claims', () => {
    expect(checkUploadRequest('logo', { name: 'setup.exe', type: 'application/x-msdownload', size: 1000 })).toBe('type_not_allowed');
    expect(checkUploadRequest('logo', { name: 'setup.exe', type: 'image/png', size: 1000 })).toBe('extension_mismatch');
    expect(checkUploadRequest('logo', { name: 'logo.png.exe', type: 'image/png', size: 1000 })).toBe('extension_mismatch');
  });

  it('rejects SVG (script inside an image) and empty files', () => {
    expect(checkUploadRequest('logo', { name: 'logo.svg', type: 'image/svg+xml', size: 1000 })).toBe('type_not_allowed');
    expect(checkUploadRequest('logo', { name: 'logo.png', type: 'image/png', size: 0 })).toBe('empty');
  });
});

describe('sniffImageType (after upload: what the bytes really are)', () => {
  const bytes = (...b: number[]) => new Uint8Array([...b, ...new Array(12).fill(0)]);
  it('recognises PNG, JPEG and WebP by their magic numbers', () => {
    expect(sniffImageType(bytes(0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a))).toBe('image/png');
    expect(sniffImageType(bytes(0xff, 0xd8, 0xff, 0xe0))).toBe('image/jpeg');
    expect(sniffImageType(new TextEncoder().encode('RIFF\u0000\u0000\u0000\u0000WEBPVP8 '))).toBe('image/webp');
  });

  it('does not recognise a text file renamed to .png, HTML, or an .exe', () => {
    expect(sniffImageType(new TextEncoder().encode('just some text, not an image'))).toBeNull();
    expect(sniffImageType(new TextEncoder().encode('<svg onload="alert(1)">'))).toBeNull();
    expect(sniffImageType(bytes(0x4d, 0x5a, 0x90, 0x00))).toBeNull(); // "MZ": a Windows executable
    expect(sniffImageType(new Uint8Array())).toBeNull();
  });
});

describe('object keys', () => {
  it('are generated under the org prefix, never from the file name', () => {
    expect(objectKey(ORG, 'logo', FILE)).toBe(`orgs/${ORG}/logos/${FILE}`);
    expect(objectKey(ORG, 'incident_screenshot', FILE)).toBe(`orgs/${ORG}/screenshots/${FILE}`);
    expect(thumbnailKey(objectKey(ORG, 'incident_screenshot', FILE))).toBe(`orgs/${ORG}/screenshots/${FILE}.thumb.webp`);
  });

  it('keyBelongsToOrg guards against signing another org’s key', () => {
    const key = objectKey(ORG, 'logo', FILE);
    expect(keyBelongsToOrg(key, ORG)).toBe(true);
    expect(keyBelongsToOrg(key, OTHER)).toBe(false);
  });

  it('isValidKey refuses path tricks', () => {
    expect(isValidKey(`orgs/${ORG}/logos/${FILE}`)).toBe(true);
    expect(isValidKey(`orgs/${ORG}/logos/../../etc/passwd`)).toBe(false);
    expect(isValidKey(`orgs/${ORG}/logos/${FILE}/../x`)).toBe(false);
    expect(isValidKey('/etc/passwd')).toBe(false);
  });
});
