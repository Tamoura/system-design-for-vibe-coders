/**
 * Lesson 2.2, in the browser: the three steps of a direct upload.
 *   1. ask Beacon for a signed URL (Beacon checks role, size and type)
 *   2. PUT the file straight to storage with that URL
 *   3. tell Beacon it is done (Beacon checks the bytes that arrived)
 */
export type UploadOutcome = { fileId: string; status: 'pending' | 'processing' | 'ready' | 'rejected'; reason: string | null };

export async function directUpload(requestUrl: string, orgSlug: string, file: File): Promise<UploadOutcome> {
  const ticket = await fetch(requestUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ name: file.name, type: file.type, size: file.size }),
  });
  const ticketBody = await ticket.json().catch(() => ({}));
  if (!ticket.ok) throw new Error(ticketBody.message ?? `Upload refused (${ticketBody.error ?? ticket.status})`);
  const { fileId, upload } = ticketBody.data as { fileId: string; upload: { method: string; url: string; headers: Record<string, string> } };

  const put = await fetch(upload.url, { method: upload.method, headers: upload.headers, body: file });
  if (!put.ok) throw new Error(`Storage refused the upload (${put.status})`);

  const done = await fetch(`/api/orgs/${orgSlug}/files/${fileId}/complete`, { method: 'POST' });
  const doneBody = await done.json().catch(() => ({}));
  if (!done.ok) throw new Error(doneBody.message ?? `Upload failed (${doneBody.error ?? done.status})`);
  return doneBody.data as UploadOutcome;
}
