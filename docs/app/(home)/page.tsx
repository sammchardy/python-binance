import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center text-center px-4">
      <h1 className="text-4xl font-bold mb-4">python-binance</h1>
      <p className="text-lg text-fd-muted-foreground mb-8 max-w-xl">
        Python wrapper for the Binance exchange API. Supports REST endpoints,
        WebSocket streams, and depth caches for both sync and async usage.
      </p>
      <Link
        href="/docs"
        className="inline-flex items-center rounded-lg bg-fd-primary px-6 py-3 text-fd-primary-foreground font-medium hover:opacity-90 transition-opacity"
      >
        Get Started
      </Link>
    </main>
  );
}
