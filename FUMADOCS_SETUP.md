# Fumadocs Setup for python-binance

This document describes the Fumadocs setup for generating and serving API documentation for the python-binance library.

## Overview

Fumadocs is a documentation framework that generates beautiful, searchable documentation from Python docstrings. This setup converts the python-binance package into a Next.js-powered documentation website.

## Project Structure

```
python-binance/
├── app/                    # Next.js app directory
│   ├── docs/              # Documentation pages
│   │   ├── layout.tsx    # Docs layout
│   │   └── [[...slug]]/  # Dynamic doc pages
│   ├── globals.css        # Global styles with Fumadocs themes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── content/               # Generated MDX documentation
│   └── docs/             # API docs (auto-generated)
│       └── (api)/        # API reference
├── lib/                   # Library code
│   └── source.ts         # Fumadocs content source configuration
├── scripts/              # Build scripts
│   └── generate-docs.mjs # MDX generation script
├── generate_docs.py      # Python script to generate JSON from binance package
├── mdx-components.tsx    # MDX components configuration
├── next.config.mjs       # Next.js configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Node.js dependencies and scripts
```

## Installation

### Prerequisites

- Python 3.9+ with python-binance installed in development mode
- Node.js 18+ and npm

### Setup Steps

1. **Install Python dependencies**:
   ```bash
   pip install -e .
   pip install ./node_modules/fumadocs-python
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

## Usage

### Generate Documentation

Generate API documentation from the python-binance package:

```bash
npm run generate-docs
```

This command runs two sub-commands:
- `generate-json`: Extracts API documentation from Python docstrings into `binance.json`
- `generate-mdx`: Converts the JSON into MDX files in `content/docs/(api)/`

### Development

Start the development server:

```bash
npm run dev
```

Visit http://localhost:3000 to see the documentation site.

### Production Build

Build the documentation site for production:

```bash
npm run build
```

This will:
1. Generate the latest API documentation
2. Build the Next.js application

Start the production server:

```bash
npm run start
```

## How It Works

### 1. Documentation Extraction (generate_docs.py)

The Python script uses `griffe` and `fumadocs-python` to extract documentation from the binance package:

- Loads the `binance` module using griffe
- Patches the version lookup to handle the package name mismatch (module: "binance", package: "python-binance")
- Parses all classes, functions, and modules with their docstrings
- Outputs structured JSON to `binance.json`

### 2. MDX Conversion (scripts/generate-docs.mjs)

The Node.js script converts the JSON into MDX files:

- Reads `binance.json`
- Uses `fumadocs-python` to convert the structure into MDX format
- Generates files in `content/docs/(api)/` with proper frontmatter and components

### 3. Next.js Integration

The Next.js app serves the documentation:

- **lib/source.ts**: Configures fumadocs to load MDX files
- **app/docs/layout.tsx**: Provides the documentation layout with sidebar navigation
- **app/docs/[[...slug]]/page.tsx**: Renders individual documentation pages
- **mdx-components.tsx**: Registers Python-specific MDX components

### 4. Styling

Fumadocs comes with pre-built themes:

- `fumadocs-ui/css/neutral.css`: Neutral color theme
- `fumadocs-ui/css/preset.css`: Base styles
- `fumadocs-python/preset.css`: Python-specific component styles

## Customization

### Changing the Theme

Edit `app/globals.css` to use a different color theme:

```css
@import 'tailwindcss';
@import 'fumadocs-ui/css/ocean.css';  /* ocean theme */
@import 'fumadocs-ui/css/preset.css';
@import 'fumadocs-python/preset.css';
```

Available themes: `neutral`, `ocean`, `catppuccin`

### Adding Custom Pages

Add MDX files to `content/docs/` (outside of `(api)/`) to create custom documentation pages:

```
content/docs/
├── (api)/           # Auto-generated API docs (don't edit)
├── getting-started.mdx
├── examples.mdx
└── guides/
    └── trading.mdx
```

### Modifying the Layout

Edit `app/docs/layout.tsx` to customize:

- Navigation title
- Sidebar structure
- Footer content
- Search configuration

## Troubleshooting

### Package Name Mismatch

If you see `PackageNotFoundError: No package metadata was found for binance`, ensure:

1. python-binance is installed: `pip install -e .`
2. The `generate_docs.py` script correctly patches the version lookup

### MDX Generation Fails

If `npm run generate-mdx` fails:

1. Ensure `binance.json` exists and is valid
2. Check that all fumadocs packages are installed
3. Try removing `content/docs/(api)/` and regenerating

### TypeScript Errors

Run the TypeScript compiler to check for errors:

```bash
npx tsc --noEmit
```

### Development Server Issues

If the development server won't start:

1. Delete `.next/` directory: `rm -rf .next`
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Regenerate docs: `npm run generate-docs`

## CI/CD Integration

To integrate documentation generation into your CI/CD pipeline:

```yaml
# .github/workflows/docs.yml
name: Generate Docs

on:
  push:
    branches: [main, master]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          pip install -e .
          npm install
          pip install ./node_modules/fumadocs-python

      - name: Generate docs
        run: npm run generate-docs

      - name: Build site
        run: npm run build

      # Deploy to your hosting platform
```

## Additional Resources

- [Fumadocs Documentation](https://fumadocs.dev)
- [Fumadocs Python Plugin](https://fumadocs.dev/docs/headless/python)
- [Next.js Documentation](https://nextjs.org/docs)
- [python-binance Repository](https://github.com/sammchardy/python-binance)
