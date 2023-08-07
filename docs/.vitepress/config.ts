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
    ],

    sidebar: [
      {
        text: "Documentation",
        items: [{ text: "Quick Start", link: "/documentation/quick-start" }],
      },
    ],

    // socialLinks: [
    //   { icon: "github", link: "https://github.com/vuejs/vitepress" },
    // ],
  },
});
