import { describe, expect, it } from 'vitest';
import { isUsableSlug, slugify, withRandomSuffix } from '@/core/slugs';
import { safeRedirect } from '@/core/safe-redirect';

describe('slugify', () => {
  it('makes URL-safe slugs', () => {
    expect(slugify('Acme Inc.')).toBe('acme-inc');
    expect(slugify("Ana's workspace")).toBe('ana-s-workspace');
    expect(slugify('Café  Crème')).toBe('cafe-creme');
  });
  it('falls back when nothing usable is left', () => expect(slugify('!!!')).toBe('org'));
});

describe('isUsableSlug', () => {
  it('rejects slugs that would shadow Beacon routes', () => {
    expect(isUsableSlug('login')).toBe(false);
    expect(isUsableSlug('status')).toBe(false);
    expect(isUsableSlug('api')).toBe(false);
  });
  it('accepts ordinary slugs', () => expect(isUsableSlug('acme-inc')).toBe(true));
  it('rejects bad characters', () => expect(isUsableSlug('Acme/..')).toBe(false));
  it('suffixed slugs are usable', () => expect(isUsableSlug(withRandomSuffix('login'))).toBe(true));
});

describe('safeRedirect', () => {
  it('keeps same-site paths', () => expect(safeRedirect('/acme/monitors')).toBe('/acme/monitors'));
  it('refuses other sites', () => {
    expect(safeRedirect('https://evil.example')).toBe('/dashboard');
    expect(safeRedirect('//evil.example')).toBe('/dashboard');
    expect(safeRedirect('/\\evil.example')).toBe('/dashboard');
  });
  it('falls back when missing', () => expect(safeRedirect(null)).toBe('/dashboard'));
});
