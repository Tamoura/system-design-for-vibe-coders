/** Absolute links for emails, SMS and Slack: they are read outside the browser, so a path is not enough. */
export function appUrl(path: string): string {
  return `${(process.env.APP_URL ?? 'http://localhost:3000').replace(/\/$/, '')}${path}`;
}

