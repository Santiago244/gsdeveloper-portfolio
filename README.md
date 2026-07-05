# GS Developer Portfolio

Astro portfolio for `gsdeveloper.dev`.

This project combines:

- Navfolio structure: portfolio, blog, projects, about, search, content collections
- Apex-inspired visual direction: stronger display typography, darker surfaces, service-site feel
- Custom GS Developer palette: light blue accents instead of yellow

## Local Development

```bash
npm install
npm run dev
```

Astro will print a local URL, usually:

```txt
http://localhost:4321
```

## Production Build

```bash
npm run build
npm run preview
```

Build output goes to:

```txt
dist/
```

## Cloudflare Pages

Use these settings:

```txt
Framework preset: Astro
Build command: npm run build
Build output directory: dist
Node version: 22.12.0 or newer
```

After the first successful deploy, connect the custom domain:

```txt
gsdeveloper.dev
www.gsdeveloper.dev
```

## Main Files To Edit

```txt
src/config/site.toml              Site identity, nav, homepage text
src/content/about.mdx             About page
src/content/projects/index.mdx    Projects page intro
src/content/blog/                 Blog/dev notes
src/styles/global.css             Global visual theme
src/components/cards/IntroCard.astro
src/components/cards/ProfileCard.astro
```

## Notes

If `npm install` hangs, check network access to the npm registry:

```bash
npm view astro version
```

The project no longer requires Bun for normal development or production builds.
