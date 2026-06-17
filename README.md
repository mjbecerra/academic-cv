# Melgris José Becerra Ruiz — Academic CV

Personal academic website and CV for **Melgris José Becerra Ruiz**, Geographer & Environmental Scientist (PhD, UFPA 2024).

**Live site:** https://mjbecerra.github.io

[![Deploy to GitHub Pages](https://github.com/mjbecerra/mjbecerra.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/mjbecerra/mjbecerra.github.io/actions/workflows/deploy.yml)

---

## About

Research focused on GIS, indigenous territories, climate change perceptions, and socio-environmental dynamics in the Amazon and coastal Latin America. Coordinator at CLACSO's Working Group on Critical Latin American Geographic Thought.

- ORCID: [0000-0001-6675-7370](https://orcid.org/0000-0001-6675-7370)
- Google Scholar: [Melgris Becerra](https://scholar.google.com/citations?user=d9VzGo0AAAAJ)
- LinkedIn: [melgris-jose-becerra](https://www.linkedin.com/in/melgris-jose-becerra/)

---

## Tech stack

Built with [Hugo](https://gohugo.io) + [HugoBlox Academic CV](https://hugoblox.com) template, deployed to GitHub Pages.

| Tool | Version |
|------|---------|
| Hugo Extended | 0.163.2 (minimum — see note below) |
| HugoBlox blox module | `20260527025321` |
| CSS | Tailwind CSS v4 via `@tailwindcss/cli` |
| Package manager | pnpm |

> **Important:** The HugoBlox module requires Hugo ≥ 0.163.x. Older versions cause a fatal build error.

---

## Local development

```bash
# 1. Install Node.js dependencies (required for Tailwind CSS)
pnpm install

# 2. Start dev server
hugo server

# Site runs at http://localhost:1313
```

> `node_modules` is gitignored. Run `pnpm install` after every `git clean` or fresh clone.

---

## Updating content

### Author profile (bio, links, education, experience)

Edit [`data/authors/me.yaml`](data/authors/me.yaml). This is the single source of truth for all personal information displayed across the site.

### Publications

Each publication lives in its own folder under [`content/publications/`](content/publications/):

```
content/publications/
  geospatiality-climate-change-2020/
    index.md
  critical-environmental-education-2023/
    index.md
  ...
```

**Minimal publication front matter:**

```yaml
---
title: "Paper title"
authors: [me, "Co-Author Name"]
date: "2024-06-29T00:00:00Z"
publication_types: ["article-journal"]   # article-journal | chapter | book | dataset | report
publication:
  name: "Journal Name"
hugoblox:
  ids:
    doi: "10.xxxx/xxxxx"   # use hugoblox.ids.doi — top-level doi: is deprecated
peer_reviewed: true
open_access: true
featured: false   # true = appears in the featured grid on homepage
tags: ["tag1", "tag2"]
links:
  - type: pdf
    url: "https://doi.org/..."
---
```

### Homepage sections

Configured in [`content/_index.md`](content/_index.md).

### Experience, skills, languages

Configured in [`data/authors/me.yaml`](data/authors/me.yaml) under `experience`, `skills`, and `languages` keys.

---

## Deploy

Every push to `main` triggers the GitHub Actions workflow in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

```
push → main
  └─ pnpm install + Hugo build
       └─ peaceiris/actions-gh-pages
            └─ push public/ → gh-pages branch → GitHub Pages
```

GitHub Pages is configured to serve from the `gh-pages` branch.

---

## Project structure

```
config/_default/
  hugo.yaml          # baseURL, build settings
  params.yaml        # site identity, theme, SEO description
  menus.yaml         # navigation: Bio · Papers · Experience · Projects

content/
  _index.md          # homepage layout
  experience.md      # experience & skills page
  publications/      # 14 publications (one folder each)
  projects/          # research projects

data/authors/me.yaml # all author profile data

assets/media/
  authors/me.png     # profile photo

static/
  favicon.svg        # SVG favicon (MB initials)
  site.webmanifest   # PWA manifest
  uploads/resume.pdf # CV PDF

layouts/_partials/hooks/head-end/
  seo.html           # Person JSON-LD schema, meta keywords

hugoblox.yaml        # Hugo version pin, deploy host
```

---

## License

Site content © Melgris José Becerra Ruiz. All rights reserved.

Framework: [HugoBlox](https://github.com/HugoBlox/kit) — [MIT License](LICENSE.md).
