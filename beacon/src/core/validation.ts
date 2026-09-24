import { z } from 'zod';

/**
 * Validation for "add a monitor". Shared by the form's server action and, later,
 * the public API (lesson 5.2), so the rules live in exactly one place.
 */
export const ALLOWED_INTERVALS = [30, 60, 300, 900] as const;

export const createMonitorInput = z.object({
  name: z.string().trim().min(1, 'Give the monitor a name').max(80),
  url: z
    .string()
    .trim()
    .url('Enter a full URL, like https://example.com/health')
    .refine((u) => /^https?:\/\//i.test(u), 'Only http:// and https:// URLs can be monitored'),
  intervalSeconds: z.coerce
    .number()
    .int()
    .refine((n) => (ALLOWED_INTERVALS as readonly number[]).includes(n), 'Pick one of the listed intervals'),
});

export type CreateMonitorInput = z.infer<typeof createMonitorInput>;
