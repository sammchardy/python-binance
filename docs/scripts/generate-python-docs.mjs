import { convert, write } from "fumadocs-python";
import * as fs from "node:fs/promises";
import * as path from "node:path";

async function generate() {
  const outDir = "content/docs/api";

  // Clean output directory
  await fs.rm(outDir, { recursive: true, force: true });
  await fs.mkdir(outDir, { recursive: true });

  // Read the generated JSON
  const content = JSON.parse(
    (await fs.readFile("./api-output/binance.json")).toString(),
  );

  // Convert JSON to MDX using fumadocs-python
  const converted = convert(content, { baseUrl: "/docs/api" });

  // Write MDX files
  await write(converted, { outDir });

  // Count generated files
  const files = await fs.readdir(outDir, { recursive: true });
  const mdxFiles = files.filter((f) => f.endsWith(".mdx"));
  console.log(`Generated ${mdxFiles.length} MDX files in ${outDir}`);
}

generate().catch((err) => {
  console.error("Error generating API docs:", err);
  process.exit(1);
});
