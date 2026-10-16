import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  output: "hybrid",
  site: "https://cryptdoctor52.xyz",
  integrations: [sitemap()],
  adapter: cloudflare()
});