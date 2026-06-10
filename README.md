# Token PSEO

Micro-token security audit and scam check platform. Statically generated with Astro, powered by DexScreener + GoPlus data.

## Structure

- `scraper/` — Python data pipeline
- `src/` — Astro site
- `data/tokens.json` — token data consumed at build time
- `.github/workflows/scrape-and-deploy.yml` — CI/CD

## Local dev

```bash
npm install
npm run dev
```

## Scraper

```bash
pip install -r scraper/requirements.txt
python scraper/main.py
```
