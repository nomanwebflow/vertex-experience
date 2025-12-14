# Vertex Experience

A premium web design and development agency website built with Webflow, featuring smooth animations with GSAP and Lenis smooth scrolling.

## Features

- 🎨 Modern, responsive design
- ⚡ Optimized performance with AVIF images
- 🎭 Smooth GSAP animations
- 📱 Mobile-first approach
- 🚀 Fast loading with optimized assets
- 🔒 Security headers configured

## Tech Stack

- HTML5, CSS3, JavaScript
- GSAP 3.13.0 for animations
- ScrollTrigger for scroll-based animations
- Lenis for smooth scrolling
- jQuery 3.5.1
- Swiper for carousels

## Project Structure

```
vertex/
├── case-studies/          # Case study pages
│   ├── melbourne.html
│   ├── trusty.html
│   └── studio-des-iles.html
├── css/                   # Stylesheets
│   └── combined.min.css
├── js/                    # JavaScript files
│   ├── webflow.js
│   └── lenis.js
├── images/                # Optimized images (AVIF)
├── videos/                # Video assets
├── fonts/                 # Web fonts
├── /             # Homepage
├── branding.html          # Branding page
├── free-audit.html        # Free audit page
├── 404.html               # 404 error page
└── privacy-policy.html    # Privacy policy

```

## Deployment

This site is deployed on Cloudflare Pages.

### Deploy via Wrangler CLI

```bash
npm install -g wrangler
wrangler login
wrangler pages deploy . --project-name=vertex-experience
```

### Deploy via Git

Push to your repository and Cloudflare Pages will automatically deploy.

## Performance

- ✅ Minified CSS and JavaScript
- ✅ Optimized images (AVIF format)
- ✅ Browser caching configured
- ✅ CDN delivery via Cloudflare
- ✅ HTTP/3 support

## License

All rights reserved © 2025 Vertex Experience

## Contact

For inquiries, visit [vertexexperience.com](https://vertexexperience.com)
