# GS Developer Portfolio

Personal portfolio for **Cesar Santiago Gonzalez Cuellar**, an ICT student at the University of Žilina focused on data science, artificial intelligence, and telecommunications.

Live site: [gsdeveloper.dev](https://gsdeveloper.dev)  
GitHub: [Santiago244](https://github.com/Santiago244)

## About The Project

This portfolio presents my work at the intersection of artificial intelligence, data science, and telecommunications. It highlights projects related to machine learning, RF signal analysis, software development, databases, Java, Python, and modern web technologies.

The site is built as a code-first portfolio instead of a page-builder website. That makes it easier to customize the design, keep the source version-controlled, and deploy updates automatically through Cloudflare Pages.

## What It Showcases

- Data science and machine learning projects
- Automatic Modulation Classification and RF signal datasets
- Python, Java, databases, and practical software development
- Web projects built with modern frontend tools
- Notes, project writeups, and learning progress
- Professional background in IT support, customer support, and technical communication

## Tech Stack

- Astro
- TypeScript
- HTML
- CSS / SCSS-inspired styling
- JavaScript
- MDX content
- Pagefind search
- Cloudflare Pages

## Project Structure

```txt
src/config/site.toml              Main site content and profile data
src/content/about.mdx             About page content
src/content/projects/index.mdx    Projects page content
src/content/blog/                 Blog posts and development notes
src/styles/global.css             Global theme and visual style
src/components/                   Reusable Astro components
public/images/                    Static images and profile assets
```

## Deployment

The site is designed to be deployed on Cloudflare Pages. Cloudflare builds the Astro project and serves the generated static files from the `dist` directory.

```txt
Build command: npm run build
Build output directory: dist
```

Every update pushed to the GitHub repository can trigger a new Cloudflare Pages deployment.

## Purpose

The goal of this repository is to document my technical growth and present my work clearly to recruiters, collaborators, and other developers. It is both a portfolio website and a living record of the projects I am building while studying ICT, artificial intelligence, and telecommunications.
