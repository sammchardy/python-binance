import { source } from "@/lib/source";
import type { InferPageType } from "fumadocs-core/source";

export async function getLLMText(page: InferPageType<typeof source>) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const data = page.data as any;
  const processed = typeof data.getText === "function"
    ? await data.getText("processed")
    : data.description ?? "";

  return `# ${page.data.title} (${page.url})

${processed}`;
}
