// import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

// https://vitepress.dev/reference/site-config
export default withMermaid({
  title: "INTELMO",
  description: "Interface Toolkit for Extensible Language Models",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Documentation", link: "/start/quick-start" },
      { text: "EMNLP 2023 Demo", link: "/emnlp-demo" },
      { text: "Playground", link: "/playground" },
    ],

    sidebar: [
      {
        text: "Getting Started",
        items: [{ text: "Quick Start", link: "/start/quick-start" }],
      },
      {
        text: "Basic Concepts",
        items: [
          { text: "Block", link: "/concepts/block" },
          { text: "Task", link: "/concepts/task" },
        ],
      },
      {
        text: "Built-in Tasks",
        items: [
          { text: "Insertion", link: "/tasks/insertion" },
          { text: "Modification", link: "/tasks/modification" },
          { text: "Generation", link: "/tasks/generation" },
        ],
      },
      {
        text: "Customization",
        items: [{ text: "Custom Tasks", link: "/customization/custom-tasks" }],
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
