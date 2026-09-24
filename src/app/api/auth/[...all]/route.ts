import { toNextJsHandler } from 'better-auth/next-js';
import { auth } from '@/lib/auth';

// Lesson 1.1: Better Auth's own endpoints (sign-in, sign-out, OAuth callbacks,
// email verification and reset links) are all served from /api/auth/*.
export const { GET, POST } = toNextJsHandler(auth);
