# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static HTML email/newsletter template for a "Life Science Newsletter". There are no build tools, frameworks, package managers, or dependencies — the entire project is a single file: `index.html`.

## Structure

- `index.html` — The complete newsletter template. All CSS is inline in a `<style>` block. Content is added inside the `.content` div, replacing the `<!-- Add your content here -->` placeholder.

## Development

Open `index.html` directly in a browser to preview. No server or build step is needed.

## Conventions

- All styles are defined in the `<style>` block in `<head>` — do not use external stylesheets or inline `style=` attributes.
- Brand color: `#6baed6` (used for header and footer backgrounds).
- Placeholder text uses `[Recipient's Name]` bracket notation for variable fields.
