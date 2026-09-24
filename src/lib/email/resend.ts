import type { EmailTransport } from './transport';

/**
 * Lesson 4.1 (🟢): the production provider, Resend, over its HTTP API
 * (https://resend.com/docs/api-reference/emails/send-email). No SDK needed:
 * one POST. The Idempotency-Key header makes a retried job safe: Resend
 * returns the first send's result instead of sending again.
 *
 * Not exercised against Resend's servers here (no internet in the course's
 * build environment); tests and the smoke test use SMTP and memory. A bad API
 * key makes send() throw, the job is retried with backoff, and the user's
 * request never notices (lesson 4.1 🟡, "a provider outage delays emails").
 */
export function createResendTransport(apiKey: string, endpoint = 'https://api.resend.com/emails'): EmailTransport {
  return {
    name: 'resend',
    async send(email) {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { authorization: `Bearer ${apiKey}`, 'content-type': 'application/json', 'idempotency-key': email.idempotencyKey },
        body: JSON.stringify({ from: email.from, to: [email.to], subject: email.subject, html: email.html, text: email.text, headers: email.headers }),
      });
      if (!res.ok) throw new Error(`Resend answered ${res.status}: ${(await res.text()).slice(0, 200)}`);
      const { id } = (await res.json()) as { id: string };
      return { messageId: id };
    },
  };
}
