"use client";

import { useState, useCallback } from "react";

function CopyCard({
  url,
  title,
  description,
  icon,
}: {
  url: string;
  title: string;
  description: string;
  icon: React.ReactNode;
}) {
  const [state, setState] = useState<"idle" | "loading" | "copied">("idle");

  const handleCopy = useCallback(async () => {
    setState("loading");
    try {
      const res = await fetch(url);
      const text = await res.text();
      await navigator.clipboard.writeText(text);
      setState("copied");
      setTimeout(() => setState("idle"), 2500);
    } catch {
      setState("idle");
    }
  }, [url]);

  return (
    <button
      onClick={handleCopy}
      disabled={state === "loading"}
      className="flex items-start gap-4 rounded-xl border border-fd-border bg-fd-card p-5 text-left transition-colors hover:bg-fd-accent hover:border-fd-ring disabled:opacity-60 w-full"
    >
      <div className="rounded-lg bg-fd-muted p-2.5 text-fd-muted-foreground shrink-0">
        {icon}
      </div>
      <div className="min-w-0">
        <div className="font-semibold text-fd-foreground text-sm">
          {state === "copied" ? "Copied to clipboard!" : title}
        </div>
        <div className="text-fd-muted-foreground text-xs mt-1">
          {description}
        </div>
      </div>
    </button>
  );
}

function LinkCard({
  href,
  title,
  description,
  icon,
}: {
  href: string;
  title: string;
  description: string;
  icon: React.ReactNode;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-4 rounded-xl border border-fd-border bg-fd-card p-5 text-left transition-colors hover:bg-fd-accent hover:border-fd-ring w-full no-underline"
    >
      <div className="rounded-lg bg-fd-muted p-2.5 text-fd-muted-foreground shrink-0">
        {icon}
      </div>
      <div className="min-w-0">
        <div className="font-semibold text-fd-foreground text-sm">{title}</div>
        <div className="text-fd-muted-foreground text-xs mt-1">
          {description}
        </div>
      </div>
    </a>
  );
}

const GITHUB_REPO = "sammchardy/python-binance";
const GITHUB_DOCS_BRANCH = "docs";

export function LLMPageActions() {
  return (
    <div className="grid gap-3 sm:grid-cols-2 not-prose my-6">
      <CopyCard
        url="/llms.txt"
        title="Copy Page Index"
        description="Titles and URLs of all doc pages — lightweight context for AI."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
        }
      />
      <CopyCard
        url="/llms-full.txt"
        title="Copy Full Docs"
        description="All documentation content as Markdown — complete context for AI."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20"/></svg>
        }
      />
    </div>
  );
}

export function LLMOpenButtons() {
  const fullDocsUrl =
    typeof window !== "undefined"
      ? `${window.location.origin}/llms-full.txt`
      : "/llms-full.txt";

  return (
    <div className="grid gap-3 sm:grid-cols-2 not-prose my-6">
      <LinkCard
        href={`https://github.com/${GITHUB_REPO}/tree/${GITHUB_DOCS_BRANCH}/docs/content/docs`}
        title="Open in GitHub"
        description="Browse the docs source files on GitHub."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
        }
      />
      <LinkCard
        href="/llms-full.txt"
        title="View as Markdown"
        description="Open the full docs as raw Markdown text."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
        }
      />
      <LinkCard
        href={`https://scira.ai?q=Read+the+python-binance+docs+at+${encodeURIComponent(fullDocsUrl)}+and+help+me+use+the+library`}
        title="Open in Scira AI"
        description="Chat with docs context in Scira AI."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="m16 10-4 4-4-4"/></svg>
        }
      />
      <LinkCard
        href={`https://chatgpt.com/?hint=search&q=Read+the+python-binance+docs+at+${encodeURIComponent(fullDocsUrl)}+and+help+me+use+the+library`}
        title="Open in ChatGPT"
        description="Start a ChatGPT conversation with docs context."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"/></svg>
        }
      />
      <LinkCard
        href={`https://claude.ai/new?q=Read+the+python-binance+docs+at+${encodeURIComponent(fullDocsUrl)}+and+help+me+use+the+library`}
        title="Open in Claude"
        description="Start a Claude conversation with docs context."
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M4.709 15.955l4.397-10.985c.245-.614.793-.97 1.405-.97.598 0 1.122.34 1.385.93l4.508 10.09-2.19.96-3.703-8.39-3.612 9.325-2.19-.96zm5.735 1.56l1.06-2.735 4.078.001 1.1 2.457-4.33 1.902-1.908-1.624zm8.001-5.628l-1.095-2.453 2.19-.96 1.096 2.453-2.19.96z"/></svg>
        }
      />
      <LinkCard
        href={`https://cursor.com`}
        title="Open in Cursor"
        description={`Add docs via Settings > Features > Docs > ${typeof window !== "undefined" ? window.location.origin : ""}/llms-full.txt`}
        icon={
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m4 17 6-6-6-6"/><path d="M12 19h8"/></svg>
        }
      />
    </div>
  );
}
