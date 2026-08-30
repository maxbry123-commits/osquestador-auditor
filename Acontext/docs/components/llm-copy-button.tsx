'use client';

import { Check, Copy, FileText } from 'lucide-react';
import { useCallback, useState } from 'react';

export function LLMCopyButton({ markdownUrl }: { markdownUrl: string }) {
  const [copied, setCopied] = useState(false);

  const onClick = useCallback(async () => {
    try {
      const res = await fetch(markdownUrl);
      const text = await res.text();
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // silently fail
    }
  }, [markdownUrl]);

  return (
    <button
      type="button"
      className="inline-flex items-center gap-1.5 rounded-lg border bg-fd-secondary px-2.5 py-1.5 text-xs font-medium text-fd-muted-foreground transition-colors hover:bg-fd-accent hover:text-fd-accent-foreground"
      onClick={onClick}
    >
      {copied ? (
        <>
          <Check className="size-3.5" />
          Copied!
        </>
      ) : (
        <>
          <Copy className="size-3.5" />
          Copy for LLM
        </>
      )}
    </button>
  );
}

export function ViewMarkdownLink({ markdownUrl, githubUrl }: { markdownUrl: string; githubUrl?: string }) {
  return (
    <div className="flex flex-row flex-wrap gap-2">
      <a
        href={markdownUrl}
        target="_blank"
        rel="noreferrer"
        className="inline-flex items-center gap-1.5 rounded-lg border bg-fd-secondary px-2.5 py-1.5 text-xs font-medium text-fd-muted-foreground transition-colors hover:bg-fd-accent hover:text-fd-accent-foreground no-underline"
      >
        <FileText className="size-3.5" />
        View as Markdown
      </a>
      {githubUrl && (
        <a
          href={githubUrl}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1.5 rounded-lg border bg-fd-secondary px-2.5 py-1.5 text-xs font-medium text-fd-muted-foreground transition-colors hover:bg-fd-accent hover:text-fd-accent-foreground no-underline"
        >
          Edit on GitHub
        </a>
      )}
    </div>
  );
}
