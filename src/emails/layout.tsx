import { Body, Button, Container, Head, Hr, Html, Link, Preview, Section, Text } from '@react-email/components';
import type { ReactNode } from 'react';

/*
 * Lesson 4.1: email HTML is stuck around 2005 (tables, inline styles, Outlook
 * rendering with Word). React Email's components output that HTML for us, so
 * a template reads like any other React component. Every template here is
 * wrapped in this layout, and every email also gets a plain-text part,
 * rendered from the same component (src/emails/index.tsx).
 */

const page = { backgroundColor: '#f6f7f9', fontFamily: '-apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif', padding: '24px 0' };
const card = { backgroundColor: '#ffffff', border: '1px solid #e3e6eb', borderRadius: '12px', padding: '24px', maxWidth: '520px' };
const brand = { fontSize: '16px', fontWeight: 800, color: '#1a1f29', margin: '0 0 16px' };
const footer = { fontSize: '12px', lineHeight: '18px', color: '#5d6675', margin: '0' };

export const text = { fontSize: '15px', lineHeight: '24px', color: '#1a1f29', margin: '0 0 14px' };
export const muted = { fontSize: '13px', lineHeight: '20px', color: '#5d6675', margin: '0 0 12px' };

export function EmailLayout({
  preview,
  children,
  reason,
  unsubscribeUrl,
}: {
  /** The grey line inbox apps show next to the subject. */
  preview: string;
  children: ReactNode;
  /** Why this person got this email, printed in the footer. */
  reason: string;
  /** Lesson 4.1/4.2: subscribed and optional mail carries a way out that needs no login. */
  unsubscribeUrl?: string;
}) {
  return (
    <Html lang="en">
      <Head />
      <Preview>{preview}</Preview>
      <Body style={page}>
        <Container style={card}>
          <Text style={brand}>◉ Beacon</Text>
          {children}
          <Hr style={{ borderColor: '#e3e6eb', margin: '20px 0 12px' }} />
          <Text style={footer}>
            {reason}
            {unsubscribeUrl && (
              <>
                {' '}
                <Link href={unsubscribeUrl} style={{ color: '#5d6675' }}>Unsubscribe</Link>
              </>
            )}
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

/** A button, with the link repeated as text for clients that hide buttons. */
export function Action({ href, label }: { href: string; label: string }) {
  return (
    <Section style={{ margin: '4px 0 16px' }}>
      <Button href={href} style={{ backgroundColor: '#2f4f9a', color: '#ffffff', borderRadius: '8px', padding: '10px 18px', fontWeight: 600, fontSize: '15px' }}>
        {label}
      </Button>
      <Text style={{ ...muted, margin: '12px 0 0' }}>
        Or open this link: <Link href={href}>{href}</Link>
      </Text>
    </Section>
  );
}

/** "3 minutes", "2 hours 5 minutes": for incident durations. */
export function duration(fromIso: string, toIso: string): string {
  const minutes = Math.max(1, Math.round((Date.parse(toIso) - Date.parse(fromIso)) / 60_000));
  if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'}`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return `${h} hour${h === 1 ? '' : 's'}${m ? ` ${m} minute${m === 1 ? '' : 's'}` : ''}`;
}

/** Times in emails are UTC and say so (lesson 4.1: the reader's timezone is a later refinement). */
export function utc(iso: string): string {
  return `${iso.slice(0, 16).replace('T', ' ')} UTC`;
}
