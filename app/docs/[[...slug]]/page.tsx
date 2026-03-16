import { source } from "@/lib/source";
import {
  DocsPage,
  DocsBody,
  DocsDescription,
  DocsTitle,
} from "fumadocs-ui/page";
import { notFound } from "next/navigation";
import defaultMdxComponents from "fumadocs-ui/mdx";
import { LLMCopyButton, ViewOptions } from "@/components/ai/page-actions";
import {
  PyFunction,
  PyAttribute,
  PyParameter,
  PySourceCode,
  PyFunctionReturn,
  Tab,
  Tabs,
} from "fumadocs-python/components";

const pythonComponents = {
  PyFunction,
  PyAttribute,
  PyParameter,
  PySourceCode,
  PyFunctionReturn,
  Tab,
  Tabs,
};

export default async function Page(props: {
  params: Promise<{ slug?: string[] }>;
}) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  // fumadocs-mdx adds body/toc at runtime; cast through any for type compat
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const data = page.data as any;
  const MDX = data.body;

  const markdownUrl = `${page.url}.mdx`;

  return (
    <DocsPage toc={data.toc}>
      <DocsTitle>{data.title}</DocsTitle>
      <DocsDescription>{data.description}</DocsDescription>
      <div className="flex flex-row gap-2 items-center border-b border-fd-border pt-2 pb-4">
        <LLMCopyButton markdownUrl={markdownUrl} />
        <ViewOptions
          markdownUrl={markdownUrl}
          githubUrl={`https://github.com/sammchardy/python-binance/blob/docs/content/docs/${page.slugs.join("/")}.mdx`}
        />
      </div>
      <DocsBody>
        <MDX components={{ ...defaultMdxComponents, ...pythonComponents }} />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(props: {
  params: Promise<{ slug?: string[] }>;
}) {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) notFound();

  return {
    title: page.data.title,
    description: page.data.description,
  };
}
