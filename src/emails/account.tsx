import { Text } from '@react-email/components';
import { Action, EmailLayout, muted, text } from './layout';

/*
 * Lesson 4.1 (🟢): the account emails. Links only, never secrets in the text,
 * and a line for the person who did NOT ask for this email.
 */

export type VerifyEmailProps = { name: string; url: string };

export function VerifyEmail({ name, url }: VerifyEmailProps) {
  return (
    <EmailLayout preview="Confirm your email address to finish setting up Beacon." reason="You are receiving this because someone signed up for Beacon with this address.">
      <Text style={text}>Hi {name},</Text>
      <Text style={text}>Confirm your email address to finish setting up your Beacon account.</Text>
      <Action href={url} label="Confirm email" />
      <Text style={muted}>If you did not sign up for Beacon, ignore this email and nothing will happen.</Text>
    </EmailLayout>
  );
}

export type ResetPasswordProps = { name: string; url: string };

export function ResetPassword({ name, url }: ResetPasswordProps) {
  return (
    <EmailLayout preview="Reset your Beacon password. The link works for one hour." reason="You are receiving this because a password reset was requested for this address.">
      <Text style={text}>Hi {name},</Text>
      <Text style={text}>Someone asked to reset your Beacon password. If it was you, choose a new one within the next hour:</Text>
      <Action href={url} label="Choose a new password" />
      <Text style={muted}>If it wasn’t you, ignore this email. Your password stays the same.</Text>
    </EmailLayout>
  );
}

export type InvitationProps = { inviterEmail: string; orgName: string; role: string; url: string };

export function Invitation({ inviterEmail, orgName, role, url }: InvitationProps) {
  return (
    <EmailLayout preview={`Join ${orgName} on Beacon.`} reason={`You are receiving this because ${inviterEmail} invited this address.`}>
      <Text style={text}>
        {inviterEmail} invited you to join <strong>{orgName}</strong> on Beacon as {role}.
      </Text>
      <Action href={url} label="Accept invitation" />
      <Text style={muted}>The link works once and expires in 7 days. If you were not expecting it, ignore this email.</Text>
    </EmailLayout>
  );
}
