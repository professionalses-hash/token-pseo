import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  output: "static",
  site: "https://cryptdoctor52.xyz",
  integrations: [sitemap()],
});
