# faresamir7.github.io

Personal website of **Fares Amir Hassen** — Technical Account Manager at Hewlett Packard Enterprise, Wireless Network Engineer, and Cybersecurity Specialist based in Tunis, Tunisia.

## About

This is a modern, zero-dependency personal portfolio site built with pure HTML, CSS, and vanilla JavaScript. No frameworks, no build tools, no npm packages — just clean code that loads fast and works everywhere.

## Design

- **Aesthetic:** Bold streetwear-inspired dark monochrome theme with red (#ff2d2d) accents
- **Typography:** Space Grotesk (headings) + IBM Plex Mono (body text) via Google Fonts
- **Features:** Custom animated cursor, scroll-triggered reveal animations, noise texture overlay, responsive mobile layout

## Sections

| Section | Description |
|---------|-------------|
| Hero | Name, current role at HPE, and call-to-action |
| About | Professional summary with contact details |
| Experience | Full timeline from 2019–present (HPE TAM, Aruba Networking, 3S Standard Sharing Software, OXAHOST, BIAT) |
| Skills & Expertise | Account Management, Wireless Network Design, Wireless Mobility, Cybersecurity, System Administration, Software Development |
| Certifications | Palo Alto Networks CIC NIST/NICE Framework certifications |
| Education | ESPRIT — Engineer's Degree in Network Infrastructure and Data Security (2017–2022) |
| Contact | Email, LinkedIn, and location |

## Project Structure

```
faresamir7.github.io/
├── index.html          # Single-page site with all sections
├── css/styles.css      # All styles (~15KB) — dark theme, animations, responsive breakpoints
├── js/main.js          # Custom cursor + scroll reveal + mobile nav toggle
└── README.md           # This file
```

## Tech Stack

- **HTML5** — semantic markup with accessibility attributes
- **CSS3** — CSS Grid, Flexbox, custom properties, `@media` responsive breakpoints, `prefers-reduced-motion` support
- **Vanilla JavaScript** — Intersection Observer pattern for scroll reveals, smooth cursor tracking via `requestAnimationFrame`

## Browser Support

Modern browsers (Chrome, Firefox, Safari, Edge). Graceful degradation on older versions. Touch devices automatically disable the custom cursor and use native touch interaction.

## Deployment

Hosted on GitHub Pages at [faresamir7.github.io](https://faresamir7.github.io) — push to `master` branch triggers automatic deployment.

---

Built by Fares Amir Hassen · © 2026
