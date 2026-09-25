/**
 * Lesson 7.4: scripts read the same configuration file Next.js reads in
 * development (`.env.local`, then `.env`). Variables already set in the
 * environment win, so production (where there is no file; the platform sets
 * the variables) and CI behave exactly as before. Import it FIRST.
 */
import { existsSync } from 'node:fs';

for (const file of ['.env.local', '.env']) {
  if (existsSync(file)) process.loadEnvFile(file);
}
