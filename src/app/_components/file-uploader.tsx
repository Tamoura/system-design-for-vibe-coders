'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { directUpload } from './direct-upload';

/**
 * A file picker that uploads straight to storage (lesson 2.2). The `accept`
 * attribute is a convenience for the user, not a check: the server validates
 * before signing and again after upload.
 */
export function FileUploader({ requestUrl, orgSlug, label }: { requestUrl: string; orgSlug: string; label: string }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<{ error: boolean; text: string } | null>(null);

  async function onChange(e: React.ChangeEvent<HTMLInputElement>) {
    const input = e.currentTarget;
    const file = input.files?.[0];
    if (!file) return;
    setBusy(true);
    setMessage(null);
    try {
      const result = await directUpload(requestUrl, orgSlug, file);
      if (result.status === 'rejected') setMessage({ error: true, text: `Rejected: ${result.reason}` });
      else setMessage({ error: false, text: result.status === 'processing' ? 'Uploaded, processing…' : 'Uploaded.' });
      router.refresh();
    } catch (err) {
      setMessage({ error: true, text: (err as Error).message });
    } finally {
      setBusy(false);
      input.value = '';
    }
  }

  return (
    <div className="grid" style={{ gap: '.3rem' }}>
      <label className="muted">
        {label}{' '}
        <input type="file" accept="image/png,image/jpeg,image/webp" onChange={onChange} disabled={busy} data-testid="file-input" />
      </label>
      {busy && <span className="muted">Uploading…</span>}
      {message && (
        <span className={message.error ? 'error' : 'muted'} role="status" data-testid="upload-message">
          {message.text}
        </span>
      )}
    </div>
  );
}
