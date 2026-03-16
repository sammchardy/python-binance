"use client";

import {
  createContext,
  useContext,
  useState,
  useRef,
  useEffect,
  useCallback,
  type ReactNode,
} from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const AISearchContext = createContext<{
  open: boolean;
  setOpen: (open: boolean) => void;
}>({
  open: false,
  setOpen: () => {},
});

export function AISearch({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return (
    <AISearchContext.Provider value={{ open, setOpen }}>
      {children}
    </AISearchContext.Provider>
  );
}

export function AISearchTrigger({
  children,
  className,
  position,
}: {
  children: ReactNode;
  className?: string;
  position?: "float";
}) {
  const { setOpen } = useContext(AISearchContext);

  return (
    <button
      onClick={() => setOpen(true)}
      className={`${className ?? ""} ${position === "float" ? "fixed bottom-6 right-6 z-50" : ""}`}
    >
      {children}
    </button>
  );
}

export function AISearchPanel() {
  const { open, setOpen } = useContext(AISearchContext);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || isStreaming) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input.trim(),
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setIsStreaming(true);
    setError(null);

    const assistantId = crypto.randomUUID();
    setMessages((prev) => [
      ...prev,
      { id: assistantId, role: "assistant", content: "" },
    ]);

    try {
      abortRef.current = new AbortController();

      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: newMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
        signal: abortRef.current.signal,
      });

      if (!res.ok) {
        const errText = await res.text().catch(() => "");
        throw new Error(errText || `API error: ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let accumulated = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        accumulated += decoder.decode(value, { stream: true });
        const current = accumulated;
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId ? { ...m, content: current } : m,
          ),
        );
      }
      // Flush remaining bytes
      accumulated += decoder.decode();
    } catch (err) {
      if (err instanceof Error && err.name !== "AbortError") {
        setError(err.message);
        setMessages((prev) => prev.filter((m) => m.id !== assistantId));
      }
    } finally {
      setIsStreaming(false);
      abortRef.current = null;
    }
  }, [input, isStreaming, messages]);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage();
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-fd-background border border-fd-border rounded-xl shadow-2xl w-full max-w-xl mx-4 flex flex-col max-h-[80vh]">
        <div className="flex items-center justify-between p-4 border-b border-fd-border">
          <h2 className="font-semibold text-sm">
            Ask AI about python-binance
          </h2>
          <button
            onClick={() => {
              setOpen(false);
              abortRef.current?.abort();
            }}
            className="text-fd-muted-foreground hover:text-fd-foreground text-lg leading-none"
          >
            &times;
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3 min-h-[200px]">
          {messages.length === 0 && (
            <p className="text-fd-muted-foreground text-sm text-center mt-8">
              Ask anything about python-binance...
            </p>
          )}
          {messages.map((m) => (
            <div
              key={m.id}
              className={`text-sm ${m.role === "user" ? "text-right" : "text-left"}`}
            >
              <div
                className={`inline-block rounded-lg px-3 py-2 max-w-[85%] ${
                  m.role === "user"
                    ? "bg-fd-primary text-fd-primary-foreground"
                    : "bg-fd-muted text-fd-foreground"
                }`}
              >
                <div className="whitespace-pre-wrap">
                  {m.content || (isStreaming ? "" : "")}
                </div>
              </div>
            </div>
          ))}
          {error && (
            <div className="text-sm text-red-500 text-center">{error}</div>
          )}
          {isStreaming && messages[messages.length - 1]?.content === "" && (
            <div className="text-sm text-fd-muted-foreground">Thinking...</div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form
          onSubmit={onSubmit}
          className="p-4 border-t border-fd-border flex gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="How do I place a market order?"
            className="flex-1 bg-fd-muted rounded-lg px-3 py-2 text-sm outline-none placeholder:text-fd-muted-foreground"
            autoFocus
          />
          <button
            type="submit"
            disabled={isStreaming || !input.trim()}
            className="bg-fd-primary text-fd-primary-foreground rounded-lg px-4 py-2 text-sm font-medium disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
