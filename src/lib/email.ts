/**
 * Send an email. For now it prints the message to the server console, which is
 * enough to click verification, reset and invitation links while developing.
 *
 * TODO(4.1): send real transactional email (Mailpit locally, a provider in
 * production). Until then, anything that "emails a link" only logs it, so do
 * not run this build for real users.
 */
export async function sendEmail(message: { to: string; subject: string; text: string }): Promise<void> {
  console.log(`\n[email] to=${message.to} subject="${message.subject}"\n${message.text}\n[/email]\n`);
}
