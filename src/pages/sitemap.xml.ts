// =============================================================================
// sitemap.xml.ts — 动态生成站点地图
// =============================================================================

import type { APIRoute } from 'astro';

// 所有需要被 Google 索引的页面路径
const pages = [
  { path: '/', priority: 1.0, changefreq: 'daily' },
  { path: '/alternatives/', priority: 0.9, changefreq: 'daily' },
  { path: '/deals/', priority: 0.8, changefreq: 'daily' },
  // 5 个标杆替代方案页
  { path: '/alternatives/chatgpt/', priority: 0.85, changefreq: 'daily' },
  { path: '/alternatives/midjourney/', priority: 0.85, changefreq: 'daily' },
  { path: '/alternatives/jasper/', priority: 0.85, changefreq: 'daily' },
  { path: '/alternatives/copy-ai/', priority: 0.85, changefreq: 'daily' },
  { path: '/alternatives/notion-ai/', priority: 0.85, changefreq: 'daily' },
];

const siteUrl = 'https://aiternatives.com';

export const GET: APIRoute = () => {
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${pages
  .map(
    (page) => `  <url>
    <loc>${siteUrl}${page.path}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
