import { describe, expect, it } from 'vitest';
import { decideIncident, overallStatus, uptimePercent } from '@/core/incidents';

describe('decideIncident', () => {
  it('does not open on a single failure', () => {
    expect(decideIncident(false, [false, true, true])).toBe('none');
  });
  it('does not open on two failures (lesson 4.2: three in a row)', () => {
    expect(decideIncident(false, [false, false, true])).toBe('none');
  });
  it('opens after three failures in a row', () => {
    expect(decideIncident(false, [false, false, false, true])).toBe('open');
  });
  it('respects a custom threshold', () => {
    expect(decideIncident(false, [false], 2)).toBe('none');
    expect(decideIncident(false, [false, false], 2)).toBe('open');
  });
  it('resolves an open incident on the first success', () => {
    expect(decideIncident(true, [true, false, false])).toBe('resolve');
  });
  it('keeps an open incident open while failing', () => {
    expect(decideIncident(true, [false, false])).toBe('none');
  });
  it('does nothing without data', () => {
    expect(decideIncident(false, [])).toBe('none');
  });
});

describe('uptimePercent', () => {
  it('is null with no results', () => expect(uptimePercent([])).toBeNull());
  it('rounds to one decimal', () => {
    expect(uptimePercent([{ ok: true }, { ok: true }, { ok: false }])).toBe(66.7);
  });
});

describe('overallStatus', () => {
  it('is operational when everything is up', () => expect(overallStatus(['up', 'up'])).toBe('operational'));
  it('is a partial outage when some are down', () => expect(overallStatus(['up', 'down'])).toBe('partial_outage'));
  it('is a major outage when all known monitors are down', () => expect(overallStatus(['down', 'unknown'])).toBe('major_outage'));
  it('is unknown with no data', () => expect(overallStatus(['unknown'])).toBe('unknown'));
});
