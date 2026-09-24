'use client';

/** A date-time picker preset to 24 hours ago, in the viewer's time zone (sent along, for the server). */
export function SinceInput() {
  const d = new Date(Date.now() - 24 * 3600_000);
  const local = new Date(d.getTime() - d.getTimezoneOffset() * 60_000).toISOString().slice(0, 16);
  return (
    <>
      <input id="since" name="since" type="datetime-local" defaultValue={local} suppressHydrationWarning />
      <input type="hidden" name="tzOffsetMinutes" value={d.getTimezoneOffset()} suppressHydrationWarning />
    </>
  );
}
