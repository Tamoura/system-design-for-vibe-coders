'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import type { SearchResult } from '@/core/search';

const TYPE_LABEL = { page: 'Page', monitor: 'Monitor', incident: 'Incident' } as const;

/**
 * Lesson 2.3 (🟡): the cmd-K palette. Ctrl+K / ⌘K opens it anywhere in the
 * org; typing searches pages, monitors and incidents in one call; ↑/↓ move,
 * Enter opens, Esc closes. Keyboard only is enough.
 *
 * Keystrokes are debounced (150 ms), and a newer query aborts the older
 * request so results never arrive out of order.
 */
export function CommandPalette({ orgSlug }: { orgSlug: string }) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [active, setActive] = useState(0);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  // Ctrl+K / ⌘K toggles the palette from anywhere on the page.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setOpen((o) => !o);
      }
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  useEffect(() => {
    if (open) inputRef.current?.focus();
    else triggerRef.current?.focus({ preventScroll: true });
  }, [open]);

  // Debounced search; an empty query returns the navigation pages.
  useEffect(() => {
    if (!open) return;
    const controller = new AbortController();
    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/orgs/${orgSlug}/search?q=${encodeURIComponent(query)}`, { signal: controller.signal });
        if (res.ok) {
          setResults((await res.json()).data);
          setActive(0);
        }
      } catch {
        // aborted by a newer keystroke
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }, 150);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [query, open, orgSlug]);

  function close() {
    setOpen(false);
    setQuery('');
  }

  function go(result: SearchResult | undefined) {
    if (!result) return;
    close();
    router.push(result.href);
  }

  function onInputKey(e: React.KeyboardEvent) {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActive((a) => Math.min(a + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive((a) => Math.max(a - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      go(results[active]);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      close();
    }
  }

  return (
    <>
      <button ref={triggerRef} type="button" className="btn secondary palette-trigger" onClick={() => setOpen(true)} aria-keyshortcuts="Control+K Meta+K">
        Search… <kbd>Ctrl K</kbd>
      </button>
      {open && (
        <div className="palette-backdrop" onMouseDown={close}>
          <div className="palette card" role="dialog" aria-modal="true" aria-label="Search" onMouseDown={(e) => e.stopPropagation()}>
            <input
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={onInputKey}
              placeholder="Search monitors, incidents and pages…"
              role="combobox"
              aria-expanded={results.length > 0}
              aria-controls="palette-results"
              aria-activedescendant={results[active] ? `palette-option-${active}` : undefined}
              aria-autocomplete="list"
              data-testid="palette-input"
            />
            <ul id="palette-results" role="listbox" className="palette-results" aria-busy={loading}>
              {results.map((r, i) => (
                <li
                  key={`${r.type}-${r.id}`}
                  id={`palette-option-${i}`}
                  role="option"
                  aria-selected={i === active}
                  className={i === active ? 'active' : undefined}
                  onMouseEnter={() => setActive(i)}
                  onClick={() => go(r)}
                  data-type={r.type}
                >
                  <span className="badge">{TYPE_LABEL[r.type]}</span> <strong>{r.title}</strong> <span className="muted">{r.subtitle}</span>
                  {r.snippet && (
                    <div className="muted snippet">
                      {/* Matched words become <mark> elements, never HTML from the server. */}
                      {r.snippet.map((part, j) => (part.hit ? <mark key={j}>{part.text}</mark> : <span key={j}>{part.text}</span>))}
                    </div>
                  )}
                </li>
              ))}
              {!loading && query.trim() && results.length === 0 && <li className="muted">No results.</li>}
            </ul>
            <div className="muted palette-help">↑↓ to move · Enter to open · Esc to close</div>
          </div>
        </div>
      )}
    </>
  );
}
