import type { Monitor } from '@/db/schema';

/*
 * Lesson 1.3: response DTOs. An API returns an allow-listed shape, never the
 * raw row, so a column added later (organization_id today, a secret tomorrow)
 * cannot leak into a response by accident.
 */

export type MonitorDto = {
  id: string;
  name: string;
  url: string;
  intervalSeconds: number;
  paused: boolean;
  createdAt: string;
};

export function toMonitorDto(m: Monitor): MonitorDto {
  return {
    id: m.id,
    name: m.name,
    url: m.url,
    intervalSeconds: m.intervalSeconds,
    paused: m.paused,
    createdAt: m.createdAt.toISOString(),
  };
}
