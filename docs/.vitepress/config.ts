import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "INTELMO",
  description: "Interface Toolkit for Extensible Language Models",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Documentation", link: "/documentation/quick-start" },
      { text: "EMNLP 2023 Demo", link: "/emnlp-demo" },
      { text: "Playground", link: "/playground" },
    ],

    sidebar: [
      {
        text: "Documentation",
        items: [{ text: "Quick Start", link: "/documentation/quick-start" }],
      },
      {
        text: "Paper",
        items: [{ text: "EMNLP 2023 Demo", link: "/emnlp-demo" }],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/INTELMO/intelmo" },
    ],
  },
});
