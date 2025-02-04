# Detta script hämtar RSS-flöden från nyhetssajter
# Det är strukturerat för att enkelt kunna importeras i ett annat script

# Importera paket
import feedparser

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

only_titles_summaries_and_dates = []

# Fyll i logiken för att extrahera "title", "summary" och "published"
# från varje ordbok i 'posts', och hantera saknade nycklar.

for x in posts:
    tempdict = {}
    try:
        tempdict["title"] = x["title"]
    except KeyError:
        tempdict["title"] = ""
    
    try:
        tempdict["summary"] = x["summary"]
    except KeyError:
        tempdict["summary"] = ""
    
    try:
        tempdict["published"] = x["published"]
    except KeyError:
        tempdict["published"] = ""
    
    only_titles_summaries_and_dates.append(tempdict)

# print(only_titles_summaries_and_dates)
# return only_titles_summaries_and_dates

title_summary_and_date_list = []

# Fyll i logiken för att kombinera title, summary och published,
# och lägg sedan till dem som nästlade listor.

for item in only_titles_summaries_and_dates:
    combined = item["title"] + " " + item["summary"] + " " + item["published"]
    title_summary_and_date_list.append([combined])

print(title_summary_and_date_list)

def flatten_list(nested_list):
    flattened_list = []
    
    # Fyll i logiken för att platta ut den nästlade listan.
    for item in nested_list:
        for value in item:
            flattened_list.append(value)
    
    return flattened_list

flattened_list = flatten_list(title_summary_and_date_list)
print(flattened_list)