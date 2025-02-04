import feedparser
import datetime
from RssArticles_1 import posts

# Funktion för att extrahera relevanta fält från RSS-inlägg
def gettingNecessaryList():
    """
    Loopar genom 'posts' och extraherar:
      - title
      - summary
      - link
      - published
    Om en nyckel saknas, ersätts den med en tom sträng.
    """
    allitems = []
    for x in posts:
        try:
            tempdict = {
                "title": x.get("title", ""),
                "summary": x.get("summary", ""),
                "link": x.get("link", ""),
                "published": x.get("published", "")
            }
            allitems.append(tempdict)
        except Exception as e:
            print(f"Error processing post: {e}")
    return allitems

# Extrahera och lagra artiklarna
AllItemsX = gettingNecessaryList()

# Funktion för att omvandla listan till en slutgiltig lista
def ThefinalList():
    """
    Konverterar AllItemsX till en lista av listor där
    publiceringsdatum hanteras och omvandlas till standardformat.
    """
    finalList = []
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %Z",  # Ex: Mon, 01 Jan 2024 12:34:56 GMT
        "%Y-%m-%dT%H:%M:%S%z",  # Ex: 2024-01-01T12:34:56+0000
        "%Y-%m-%d %H:%M:%S",  # Ex: 2024-01-01 12:34:56
        "%a, %d %b %Y %H:%M:%S %z"  # Ex: Tue, 04 Feb 2025 09:43:22 +0100
    ]
    
    for item in AllItemsX:
        try:
            published_str = item["published"]
            parsed_date = None
            
            for date_format in date_formats:
                try:
                    parsed_date = datetime.datetime.strptime(published_str, date_format)
                    break  # Om det lyckas, avbryt loopen
                except ValueError:
                    continue
            
            if parsed_date:
                published_str = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                print(f"Warning: Could not parse date format for: {published_str}")
                published_str = "Unknown Date"
            
            finalList.append([
                item["title"],
                item["summary"],
                item["link"],
                published_str
            ])
        except Exception as e:
            print(f"Error processing final list item: {e}")
    return finalList

# Slutlig lista med nyhetsartiklar
MyTheFinalList = ThefinalList()

# Skriv ut resultatet
print(MyTheFinalList)
print(f"Antal artiklar: {len(MyTheFinalList)}")













"""

FullRSSList_1_2.py

This script takes in articles (posts) from RssArticles_1.py (via `posts`),
extracts the desired fields (title, summary, link, and published),
fixes data format issues (like dates), and provides the final list as 'MyTheFinalList'.

Students: 
 - Ensure your 'RssArticles_1.py' is in the same folder (or adjust imports accordingly).
 - Examine how 'posts' is structured, and fix any date format issues carefully.


# 1) Import posts from RssArticles_1
# from RssArticles_1 import posts
import datetime

# Pseudo code: 
# - create a function 'gettingNecessaryList' that loops through posts
# - extract title, summary, link, published
# - handle errors with try/except if fields are missing
# - return the collected list

def gettingNecessaryList():
    
    This function loops through 'posts' and extracts:
      title, summary, link, published
    Then stores them in a dictionary, finally returns a list of these dictionaries.
    
    # Pseudo code:
    #  1. Initialize an empty list (allitems)
    #  2. Loop through each 'post' in 'posts'
    #  3. Create a temp dict for each 'post'
    #  4. Extract needed keys; if missing, set to empty string
    #  5. Append the dict to the list
    #  6. Return allitems
    
    allitems = []
    
    # TODO: Replace with your actual code, e.g.:
    # for x in posts:
    #     try:
    #         tempdict = {}
    #         tempdict["title"] = x["title"]
    #         tempdict["summary"] = x["summary"]
    #         ...
    #     except:
    #         ...
    #     ...
    
    return allitems


# 2) Store the list of extracted items
AllItemsX = gettingNecessaryList()


def ThefinalList():
    
    This function converts AllItemsX into a final 2D list (or list of lists),
    while ensuring that 'published' is properly formatted (YYYY-MM-DD HH:MM:SS).
    
    # Pseudo code:
    #  1. Initialize finalList = []
    #  2. For each item (dict) in AllItemsX:
    #       a) Extract title, summary, link, published
    #       b) Parse 'published' date with multiple possible formats
    #       c) Append results as a small list [title, summary, link, published_str] to finalList
    #  3. Return finalList
    
    finalList = []

    # TODO: Replace with your code that:
    # - loops over AllItemsX
    # - handles date parsing with datetime.strptime
    # - appends the processed items to finalList
    
    return finalList


# 3) Create a variable that holds the final list
MyTheFinalList = ThefinalList()


print(MyTheFinalList)
print(len(MyTheFinalList))

"""