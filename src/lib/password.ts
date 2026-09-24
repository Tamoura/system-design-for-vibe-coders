import { hash, verify } from '@node-rs/argon2';

/*
 * Lesson 1.1: passwords are hashed with argon2id, never encrypted, never stored
 * plain. Argon2id is deliberately slow and salted, so a stolen `accounts` table
 * cannot be cracked in bulk. The library's defaults (19 MiB memory, 2
 * iterations, 1 lane) are the OWASP Password Storage Cheat Sheet's baseline.
 *
 * Better Auth uses scrypt by default; we pass these two functions to it so
 * Beacon matches the lesson's "argon2id or bcrypt" rule.
 */
const ARGON2ID = 2; // Algorithm.Argon2id (a const enum, so we spell out the value)

export function hashPassword(password: string): Promise<string> {
  return hash(password, { algorithm: ARGON2ID });
}

export function verifyPassword({ hash: stored, password }: { hash: string; password: string }): Promise<boolean> {
  return verify(stored, password).catch(() => false);
}
