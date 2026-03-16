import { createOpenRouter } from "@openrouter/ai-sdk-provider";
import { streamText } from "ai";
import { source } from "@/lib/source";

export async function POST(req: Request) {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) {
    return new Response("OPENROUTER_API_KEY environment variable is not set", {
      status: 500,
    });
  }

  const openrouter = createOpenRouter({ apiKey });

  let body: { messages?: { role: string; content?: string; parts?: { type: string; text: string }[] }[] };
  try {
    body = await req.json();
  } catch {
    return new Response("Invalid JSON body", { status: 400 });
  }

  // Normalize messages — handle both { content } and { parts } formats
  const messages = (body.messages ?? []).map((m) => ({
    role: m.role as "user" | "assistant" | "system",
    content:
      m.content ??
      m.parts
        ?.filter((p) => p.type === "text")
        .map((p) => p.text)
        .join("") ??
      "",
  }));

  if (messages.length === 0) {
    return new Response("No messages provided", { status: 400 });
  }

  // Build context from documentation pages
  const pages = source.getPages();
  const docsContext = pages
    .map((page) => `- ${page.data.title}: ${page.data.description ?? ""}`)
    .join("\n");

  try {
    const result = streamText({
      model: openrouter("openrouter/auto"),
      system: `You are a helpful assistant for python-binance, a Python wrapper for the Binance exchange API. Answer questions about the library based on the documentation. Be concise and include code examples when relevant.

Available documentation pages:
${docsContext}`,
      messages,
    });

    return result.toTextStreamResponse();
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return new Response(`AI request failed: ${message}`, { status: 502 });
  }
}
