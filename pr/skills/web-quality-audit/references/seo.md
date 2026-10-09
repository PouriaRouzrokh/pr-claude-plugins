# Technical SEO

Read this reference when Lighthouse reports failing SEO audits, or when checking metadata, crawlability, sitemaps, canonical URLs, or structured data.

## Contents

- [What Lighthouse checks](#what-lighthouse-checks)
- [HTTP-level checks](#http-level-checks)
- [Page metadata](#page-metadata)
- [Next.js Metadata API](#nextjs-metadata-api)
- [Robots and sitemap](#robots-and-sitemap)
- [Structured data (JSON-LD)](#structured-data-json-ld)
- [AI crawlers and agentic browsing](#ai-crawlers-and-agentic-browsing)
- [Checklist](#checklist)
- [Sources](#sources)

## What Lighthouse checks

The Lighthouse 13 SEO category covers a narrow technical subset:

| Audit id | Checks |
|----------|--------|
| `is-crawlable` | Page is not blocked by `noindex` (meta tag or `X-Robots-Tag` header) |
| `http-status-code` | Page returns a successful status |
| `document-title`, `meta-description` | Title and description exist |
| `link-text`, `crawlable-anchors` | Links have descriptive text and real `href` values |
| `image-alt` | Images have alt text |
| `hreflang` | Language alternates are valid |
| `robots-txt` | `robots.txt` parses |
| `canonical` | `rel=canonical` is valid and consistent |
| `structured-data` | Manual: validate JSON-LD yourself |

A passing SEO score says nothing about content quality, rankings, or indexing. Never promise ranking changes; report technical findings and leave indexing outcomes to Search Console.

## HTTP-level checks

Lighthouse sees one rendered page. Check the site-level files and headers directly:

```bash
BASE=http://localhost:3000
curl -sI "$BASE/" | grep -iE '^(HTTP|x-robots-tag|location|content-type)'
curl -s "$BASE/robots.txt"
curl -s "$BASE/sitemap.xml" | head -40
curl -s "$BASE/" | grep -ioE '<link[^>]+rel="canonical"[^>]*>|<meta[^>]+name="robots"[^>]*>'
```

Watch for:

- A production deployment that still sends `noindex` or `Disallow: /` (common when staging settings leak).
- Canonical URLs pointing to `localhost`, a staging host, or `http://`.
- Sitemap entries that redirect, return 404, or are not canonical.
- Redirect chains on the home page or key routes.

Staging environments *should* send `noindex`; report it only if the audited target is production.

## Page metadata

| Element | Requirement |
|---------|-------------|
| `<title>` | Unique per page; describes the page first, brand second. About 50–60 characters is a rough guide, not a limit. |
| `<meta name="description">` | Unique, accurate summary of the page. Search engines may show different text. |
| `<link rel="canonical">` | Absolute URL of the preferred version, usually self-referencing. |
| `<meta name="viewport">` | `width=device-width, initial-scale=1` |
| `<html lang>` | The page's primary language |
| Open Graph / Twitter | `og:title`, `og:description`, `og:image` (1200×630), `og:url` for link previews |
| Headings | One descriptive primary heading and a logical hierarchy |
| `hreflang` | On multilingual sites, every language version lists all alternates plus `x-default` |

## Next.js Metadata API

Define metadata in Server Components; Next.js renders it into `<head>`. Set `metadataBase` once in the root layout so relative URLs in canonical and Open Graph fields resolve to absolute ones.

```tsx
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: { default: 'Example', template: '%s | Example' },
  description: 'What the site offers, in one sentence.',
  openGraph: { type: 'website', siteName: 'Example' },
};
```

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  return {
    title: post.title,
    description: post.summary,
    alternates: { canonical: `/blog/${slug}` },
    openGraph: { title: post.title, description: post.summary, images: [post.coverImage] },
  };
}
```

Social images can be generated with an `opengraph-image.tsx` file in the route segment.

## Robots and sitemap

Generate both from code so they stay in sync with routes and environments:

```ts
// app/robots.ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  const isProduction = process.env.VERCEL_ENV === 'production' || process.env.APP_ENV === 'production';
  return {
    rules: isProduction ? { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/'] } : { userAgent: '*', disallow: '/' },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPosts();
  return [
    { url: 'https://example.com', lastModified: new Date() },
    ...posts.map((post) => ({ url: `https://example.com/blog/${post.slug}`, lastModified: post.updatedAt })),
  ];
}
```

Adapt the environment check to however the project distinguishes production. Sitemap rules: list only canonical, indexable URLs; at most 50,000 URLs or 50 MB per file (use a sitemap index beyond that); keep `lastModified` truthful. Do not block CSS or JavaScript that pages need to render.

## Structured data (JSON-LD)

- Describe only content that is visible on the page; never add types or claims just to win rich results.
- Use the most specific applicable type (`Article`, `Product`, `Organization`, `BreadcrumbList`, `SoftwareApplication`).
- Validate the rendered output with the [Rich Results Test](https://search.google.com/test/rich-results) or the [Schema.org validator](https://validator.schema.org/). Valid syntax does not guarantee a rich result.
- Google limits FAQ rich results to authoritative government and health sites, so `FAQPage` markup rarely changes how other sites appear.

In Next.js, render JSON-LD as a `<script>` in the page or layout and escape `<` to prevent script injection from content fields:

```tsx
export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    description: product.description,
    offers: { '@type': 'Offer', price: product.price, priceCurrency: 'USD', availability: 'https://schema.org/InStock' },
  };
  return (
    <section>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c') }}
      />
      {/* page content */}
    </section>
  );
}
```

Other common shapes:

```json
{ "@context": "https://schema.org", "@type": "Organization",
  "name": "Example", "url": "https://example.com", "logo": "https://example.com/logo.png",
  "sameAs": ["https://github.com/example", "https://www.linkedin.com/company/example"] }
```

```json
{ "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com" },
  { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog" } ] }
```

## AI crawlers and agentic browsing

Lighthouse 13 adds an **Agentic Browsing** category (`agent-accessibility-tree`, optional `llms-txt`, WebMCP checks). It measures whether agents can understand and operate the rendered page; it is not evidence of search ranking or AI citation. Fix `agent-accessibility-tree` failures as accessibility defects. Treat `llms.txt` and WebMCP as optional unless the user wants them.

AI crawler controls are product-specific. Search and user-fetch agents (for example `OAI-SearchBot`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`) are separate from training crawlers (`GPTBot`, `ClaudeBot`), and `Google-Extended` does not affect Google Search. Confirm current user-agent names in each vendor's documentation before editing `robots.txt`, and change them only when the user asks.

## Checklist

- [ ] Production pages return 200 and are indexable; staging sends `noindex`
- [ ] Every page has a unique title and meta description
- [ ] Canonical URLs are absolute, use the production host, and match the sitemap
- [ ] `robots.txt` exists, allows rendering assets, and points to the sitemap
- [ ] Sitemap lists only canonical, indexable URLs
- [ ] JSON-LD matches visible content and validates
- [ ] Open Graph image and text render correctly in a link preview
- [ ] Links use descriptive text and real `href` values
- [ ] `lang` is set; multilingual sites have reciprocal `hreflang`

## Sources

- [Google Search Central documentation](https://developers.google.com/search/docs)
- [Next.js Metadata and OG images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images), [robots.ts](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots), [sitemap.ts](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap), [JSON-LD guide](https://nextjs.org/docs/app/guides/json-ld)
- [Schema.org](https://schema.org/)
