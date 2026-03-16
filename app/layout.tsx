import "./global.css";
import { RootProvider } from "fumadocs-ui/provider/next";
import type { ReactNode } from "react";
import {
  AISearch,
  AISearchPanel,
  AISearchTrigger,
} from "@/components/ai/search";

export const metadata = {
  title: "python-binance Documentation",
  description:
    "Documentation for python-binance - Python wrapper for the Binance exchange API",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <RootProvider>
          <AISearch>
            <AISearchPanel />
            {children}
            <AISearchTrigger
              position="float"
              className="inline-flex items-center gap-2 rounded-2xl bg-fd-secondary text-fd-muted-foreground px-4 py-2 text-sm shadow-lg hover:bg-fd-accent transition-colors"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
              </svg>
              Ask AI
            </AISearchTrigger>
          </AISearch>
        </RootProvider>
      </body>
    </html>
  );
}
