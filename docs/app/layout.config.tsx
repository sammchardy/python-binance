import type { BaseLayoutProps } from "fumadocs-ui/layouts/shared";

export const baseOptions: BaseLayoutProps = {
  nav: {
    title: "python-binance",
  },
  links: [
    {
      text: "Documentation",
      url: "/docs",
      active: "nested-url",
    },
    {
      text: "GitHub",
      url: "https://github.com/sammchardy/python-binance",
    },
    {
      text: "PyPI",
      url: "https://pypi.org/project/python-binance/",
    },
  ],
};
