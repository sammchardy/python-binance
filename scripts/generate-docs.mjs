import { rimraf } from 'rimraf';
import * as Python from 'fumadocs-python';
import * as fs from 'node:fs/promises';

// Output JSON file path
const jsonPath = './binance.json';

async function generate() {
  const out = 'content/docs/(api)';

  // Clean previous output
  await rimraf(out);

  // Read the JSON file
  const content = JSON.parse((await fs.readFile(jsonPath)).toString());

  // Convert to MDX using fumadocs-python
  const converted = Python.convert(content, {
    baseUrl: '/docs',
  });

  // Write the converted docs
  await Python.write(converted, {
    outDir: out,
  });

  console.log(`✓ Generated docs in ${out}`);
}

void generate();
