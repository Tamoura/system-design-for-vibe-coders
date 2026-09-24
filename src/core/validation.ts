import { z } from 'zod';
import { ROLES } from './roles';

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

/**
 * Lesson 1.1: sign-up input. Better Auth re-checks the password length; this
 * schema gives the form friendly messages. Length beats composition rules
 * (NIST SP 800-63B), so there is no "one symbol, one capital" rule here.
 */
export const signUpInput = z.object({
  name: z.string().trim().min(1, 'Tell us your name').max(80),
  email: z.string().trim().toLowerCase().email('Enter a valid email address'),
  password: z.string().min(12, 'Use at least 12 characters').max(128),
});

export type SignUpInput = z.infer<typeof signUpInput>;

/** Lesson 1.2: "create an organization". The slug is derived from the name (src/core/slugs.ts). */
export const createOrganizationInput = z.object({
  name: z.string().trim().min(2, 'Use at least 2 characters').max(60),
});

/** Lesson 1.2 (🟡): "invite a teammate". Whether the inviter may grant `role` is checked separately (canGrantRole). */
export const inviteInput = z.object({
  email: z.string().trim().toLowerCase().email('Enter a valid email address'),
  role: z.enum(ROLES),
});
