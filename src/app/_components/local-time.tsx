'use client';

import { useEffect, useState } from 'react';

/**
 * Lesson 6.1 (🟡): "an incident at 03:14 is useless unless you say whose
 * 03:14". Times are stored in UTC; the browser formats them with Intl in the
 * viewer's own locale and time zone. The server renders UTC (it cannot know
 * the zone), then the browser replaces it after hydration.
 */
export function LocalTime({ iso }: { iso: string }) {
  const [text, setText] = useState(`${iso.slice(0, 16).replace('T', ' ')} UTC`);
  useEffect(() => {
    setText(new Intl.DateTimeFormat(undefined, { dateStyle: 'medium', timeStyle: 'short', timeZoneName: 'short' }).format(new Date(iso)));
  }, [iso]);
  return <time dateTime={iso}>{text}</time>;
}
