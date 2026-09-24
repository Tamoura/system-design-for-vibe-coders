import { messageIdFor, type EmailTransport, type OutgoingEmail } from './transport';

/**
 * Tests: every accepted message lands in `messages`. Set `outage` to make the
 * "provider" refuse everything, like a bad API key or a provider that is down.
 */
class MemoryTransport implements EmailTransport {
  readonly name = 'memory';
  readonly messages: OutgoingEmail[] = [];
  outage = false;

  async send(email: OutgoingEmail) {
    if (this.outage) throw new Error('provider unavailable (simulated outage)');
    this.messages.push(email);
    return { messageId: messageIdFor(email.idempotencyKey) };
  }

  /** Messages to one address, oldest first. */
  to(address: string) {
    return this.messages.filter((m) => m.to === address);
  }

  reset() {
    this.messages.length = 0;
    this.outage = false;
  }
}

export const memoryTransport = new MemoryTransport();
