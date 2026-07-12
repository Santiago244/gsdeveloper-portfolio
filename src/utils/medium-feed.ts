export interface MediumArticle {
  title: string;
  url: string;
  date: Date;
  excerpt: string;
  thumbnail?: string;
  categories: string[];
}

interface MediumFeedOptions {
  enabled: boolean;
  username?: string;
  feedUrl?: string;
  maxPosts?: number;
}

function getFeedUrl({ username, feedUrl }: MediumFeedOptions) {
  if (feedUrl?.trim()) return feedUrl.trim();

  const normalizedUsername = username?.trim().replace(/^@/, '');
  if (!normalizedUsername) return '';

  return `https://medium.com/feed/@${normalizedUsername}`;
}

function decodeXml(value: string) {
  return value
    .replace(/^<!\[CDATA\[/, '')
    .replace(/\]\]>$/, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'");
}

function stripHtml(value: string) {
  return decodeXml(value)
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function truncate(value: string, maxLength = 180) {
  if (value.length <= maxLength) return value;
  return `${value.slice(0, maxLength).trimEnd()}...`;
}

function readTag(source: string, tagName: string) {
  const escapedTag = tagName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = source.match(new RegExp(`<${escapedTag}[^>]*>([\\s\\S]*?)<\\/${escapedTag}>`, 'i'));
  return match ? decodeXml(match[1].trim()) : '';
}

function readAllTags(source: string, tagName: string) {
  const escapedTag = tagName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return Array.from(
    source.matchAll(new RegExp(`<${escapedTag}[^>]*>([\\s\\S]*?)<\\/${escapedTag}>`, 'gi')),
    (match) => decodeXml(match[1].trim()),
  ).filter(Boolean);
}

function readThumbnail(source: string) {
  const mediaThumbnail = source.match(/<media:thumbnail[^>]+url=["']([^"']+)["'][^>]*>/i)?.[1];
  if (mediaThumbnail) return decodeXml(mediaThumbnail);

  const content = readTag(source, 'content:encoded') || readTag(source, 'description');
  return decodeXml(content).match(/<img[^>]+src=["']([^"']+)["'][^>]*>/i)?.[1];
}

function parseMediumFeed(xml: string, maxPosts: number) {
  return Array.from(xml.matchAll(/<item\b[\s\S]*?<\/item>/gi))
    .map((match): MediumArticle | undefined => {
      const item = match[0];
      const title = stripHtml(readTag(item, 'title'));
      const url = readTag(item, 'link');
      const date = new Date(readTag(item, 'pubDate'));
      const description = readTag(item, 'description') || readTag(item, 'content:encoded');
      const excerpt = truncate(stripHtml(description));

      if (!title || !url || Number.isNaN(date.getTime())) return undefined;

      return {
        title,
        url,
        date,
        excerpt,
        thumbnail: readThumbnail(item),
        categories: readAllTags(item, 'category').slice(0, 3),
      };
    })
    .filter((article): article is MediumArticle => Boolean(article))
    .slice(0, maxPosts);
}

export async function getMediumArticles(options: MediumFeedOptions) {
  if (!options.enabled) return [];

  const feedUrl = getFeedUrl(options);
  if (!feedUrl) return [];

  try {
    const response = await fetch(feedUrl, {
      headers: {
        Accept: 'application/rss+xml, application/xml, text/xml',
        'User-Agent': 'gsdeveloper.dev Astro portfolio',
      },
    });

    if (!response.ok) return [];

    const xml = await response.text();
    return parseMediumFeed(xml, options.maxPosts ?? 6);
  } catch {
    return [];
  }
}
