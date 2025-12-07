// source.config.ts
import { defineConfig, defineDocs } from "fumadocs-mdx/config";
var source_config_default = defineConfig({
  docs: defineDocs({
    dir: "content/docs"
  })
});
export {
  source_config_default as default
};
