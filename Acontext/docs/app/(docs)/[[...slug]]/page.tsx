import { source, getLLMText } from '@/lib/source';
import {
  DocsBody,
  DocsPage,
  PageLastUpdate,
} from 'fumadocs-ui/layouts/docs/page';
import { getMDXComponents } from '@/mdx-components';
import { APIPage } from '@/components/api-page';
import { NotFound } from '@/components/not-found';
import { LLMCopyButton, ViewMarkdownLink } from '@/components/llm-copy-button';
import {
  HoverCard,
  HoverCardTrigger,
  HoverCardContent,
} from '@/components/hover-link';
import Link from 'fumadocs-core/link';
import { PathUtils } from 'fumadocs-core/source';
import type { Metadata } from 'next';

export const revalidate = false;

const baseUrl = 'https://docs.acontext.io';

interface PageProps {
  params: Promise<{ slug?: string[] }>;
}

export default async function Page(props: PageProps) {
  const params = await props.params;
  const page = source.getPage(params.slug);

  if (!page) {
    return <NotFound slug={params.slug} />;
  }

  if ('getAPIPageProps' in page.data) {
    return (
      <DocsPage toc={page.data.toc} full tableOfContent={{ style: 'clerk' }}>
        <h1 className="text-[1.75em] font-semibold">{page.data.title}</h1>
        <DocsBody>
          <APIPage {...page.data.getAPIPageProps()} />
        </DocsBody>
      </DocsPage>
    );
  }

  const data = await page.data.load();
  const MDX = data.body;
  const markdownUrl = `/llms.mdx${page.url}`;

  return (
    <DocsPage
      toc={data.toc}
      full={page.data.full}
      tableOfContent={{ style: 'clerk' }}
    >
      <h1 className="text-[1.75em] font-semibold">{page.data.title}</h1>
      <p className="text-lg text-fd-muted-foreground mb-2">
        {page.data.description}
      </p>
      <div className="flex flex-row flex-wrap gap-2 items-center border-b pb-4 mb-4">
        <LLMCopyButton markdownUrl={markdownUrl} />
        <ViewMarkdownLink
          markdownUrl={markdownUrl}
          githubUrl={`https://github.com/memodb-io/Acontext/blob/main/docs/content/docs/${page.path}`}
        />
      </div>
      <DocsBody>
        <MDX
          components={getMDXComponents({
            a: ({ href, ...props }) => {
              const found = source.getPageByHref(href ?? '', {
                dir: PathUtils.dirname(page.path),
              });

              if (!found) return <Link href={href} {...props} />;

              return (
                <HoverCard>
                  <HoverCardTrigger
                    href={
                      found.hash
                        ? `${found.page.url}#${found.hash}`
                        : found.page.url
                    }
                    {...props}
                  >
                    {props.children}
                  </HoverCardTrigger>
                  <HoverCardContent className="text-sm">
                    <p className="font-medium">{found.page.data.title}</p>
                    <p className="text-fd-muted-foreground">
                      {found.page.data.description}
                    </p>
                  </HoverCardContent>
                </HoverCard>
              );
            },
          })}
        />
      </DocsBody>
      {data.lastModified && <PageLastUpdate date={data.lastModified} />}
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(props: PageProps): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug);
  if (!page) {
    return { title: 'Not Found' };
  }

  const ogImage = {
    url: `${baseUrl}/og/${page.slugs.join('/')}`,
    width: 1200,
    height: 630,
  };

  return {
    title: page.data.title,
    description: page.data.description,
    openGraph: {
      title: page.data.title,
      description: page.data.description ?? undefined,
      url: `${baseUrl}/${page.slugs.join('/')}`,
      images: [ogImage],
    },
    twitter: {
      card: 'summary_large_image',
      title: page.data.title,
      description: page.data.description ?? undefined,
      images: [ogImage],
    },
  };
}
