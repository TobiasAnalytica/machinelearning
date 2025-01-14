# Detta script hämtar RSS-flöden från nyhetssajter

# Det är strukturerat för att enkelt kunna importeras i ett annat script


# Importera paket
import feedparser

############################# RSS-FEED Parser ##############################

# Lista med RSS-URL:er
RSS_URLS = ['http://www.dn.se/nyheter/m/rss/',
            'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', 'https://feeds.expressen.se/nyheter/',
            'http://www.svd.se/?service=rss', 'http://api.sr.se/api/rss/program/83?format=145',
            'http://www.svt.se/nyheter/rss.xml'
              ]

# Skapa en tom lista för att lagra artiklar
posts = []

# Loopar genom varje URL i RSS_URLS och hämtar artiklar
for url in RSS_URLS:
    # Hämta och analysera RSS-flödet
    feed = feedparser.parse(url)
    
    # Iterera genom varje post i flödet
    for entry in feed.entries:
        # Strukturera artikeldata och lägg till i listan
        post = {
            'title': entry.title,
            'link': entry.link,
            'published': entry.published if 'published' in entry else None,
            'summary': entry.summary if 'summary' in entry else None
        }
        posts.append(post)

# Kontrollera att artiklar har hämtats
print(f"Hämtade {len(posts)} artiklar från RSS-flöden.")
