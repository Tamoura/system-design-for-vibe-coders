import { describe, expect, it } from 'vitest';
import { createMonitorInput } from '@/core/validation';

describe('createMonitorInput', () => {
  it('accepts a valid monitor and coerces the interval', () => {
    const r = createMonitorInput.parse({ name: ' API ', url: 'https://example.com/health', intervalSeconds: '60' });
    expect(r).toEqual({ name: 'API', url: 'https://example.com/health', intervalSeconds: 60 });
  });
  it('rejects non-http schemes', () => {
    expect(createMonitorInput.safeParse({ name: 'x', url: 'ftp://example.com', intervalSeconds: 60 }).success).toBe(false);
  });
  it('rejects intervals that are not on the list', () => {
    expect(createMonitorInput.safeParse({ name: 'x', url: 'https://example.com', intervalSeconds: 7 }).success).toBe(false);
  });
  it('requires a name', () => {
    expect(createMonitorInput.safeParse({ name: '  ', url: 'https://example.com', intervalSeconds: 60 }).success).toBe(false);
  });
});
