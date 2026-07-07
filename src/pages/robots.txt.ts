// =============================================================================
// robots.txt.ts — 自动生成 crawler 规则
// =============================================================================

import type { APIRoute } from 'astro';

const siteUrl = 'https://aiternatives.com';

export const GET: APIRoute = () => {
  const robots = `User-agent: *
Allow: /
Disallow: /go/

Sitemap: ${siteUrl}/sitemap.xml
`;

  return new Response(robots, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
