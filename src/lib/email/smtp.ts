import nodemailer from 'nodemailer';
import { messageIdFor, type EmailTransport } from './transport';

/**
 * Lesson 4.1 (🟢): SMTP through nodemailer. `SMTP_URL` like
 * smtp://localhost:1025 (Mailpit) or smtps://user:pass@smtp.postmarkapp.com:465.
 * The message goes out as multipart/alternative: plain text and HTML.
 */
export function createSmtpTransport(url: string): EmailTransport {
  const transporter = nodemailer.createTransport(url);
  return {
    name: 'smtp',
    async send(email) {
      const info = await transporter.sendMail({
        from: email.from,
        to: email.to,
        subject: email.subject,
        text: email.text,
        html: email.html,
        headers: email.headers,
        messageId: messageIdFor(email.idempotencyKey),
      });
      return { messageId: info.messageId };
    },
  };
}
