---
title: 'Building gsdeveloper.dev with Astro'
description: 'The first development note for this portfolio: why the site is code-first, static, and deployed through Cloudflare Pages.'
date: '2026-06-28T00:00:00+02:00'
draft: true
showHeroImage: false
tags:
  - Astro
  - Portfolio
  - Cloudflare
categories:
  - Development Notes
series:
  - Portfolio Build
comments: false
sidebar:
  enable: true
  toc: true
  relatedPosts: true
---

This portfolio started as a decision between a WordPress builder workflow and a code-first workflow.

The code-first path won because the site should also demonstrate the work behind it: component structure, styling decisions, deployment, performance, and the ability to turn design references into a real interface.

## Stack

- Astro for the site framework
- Markdown and MDX for writing
- Cloudflare Pages for deployment
- GitHub for version control
- Light-blue visual system inspired by the Apex marketing theme

## Why Astro

Astro is a good fit because the first version of the portfolio does not need a heavy backend. Most pages are static, fast, and content-focused. JavaScript can be added only where it creates value, such as future Three.js sections or project demos.

## Next Steps

The first milestone is simple: publish a polished home page, add real project pages, and connect the domain. After that, the site can grow into a stronger professional archive.
