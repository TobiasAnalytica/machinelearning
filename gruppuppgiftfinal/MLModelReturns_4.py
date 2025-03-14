import jsonschema
import numpy as np
from FullRSSList_1_2 import MyTheFinalList
from MLModelMLC_3 import categories, vectorizer, best_clf_pipeline
from prettytable import PrettyTable

# 1. Ta den slutliga texten från 'MyTheFinalList' (title + summary)
text_data = [entry[0] + " " + entry[1] for entry in MyTheFinalList]

# 2. Ta bort tomma strängar
filtered_text_data = [text for text in text_data if text.strip() != ""]

# 3. Transformera texten med samma vectorizer som användes under träningen
text_transformed = vectorizer.transform(filtered_text_data)

# 4. Förutsäg kategorier med modellen
predictions_proba = best_clf_pipeline.predict_proba(text_transformed)

# 5. Använd tröskelvärde för att bestämma kategorier
threshold = 0.3
predicted_labels = (predictions_proba >= threshold).astype(int)

# 6. Kombinera resultaten med MyTheFinalList
final_results = []
for idx, entry in enumerate(MyTheFinalList):
  categories_predicted = [categories[i] for i in range(len(categories)) if predicted_labels[idx][i] == 1]
  final_results.append({
    "title": entry[0],
    "summary": entry[1],
    "link": entry[2],
    "published": entry[3],
    "topic": ", ".join(categories_predicted)
  })

# 7. Validera strukturen
schema = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "summary": {"type": "string"},
    "link": {"type": "string"},
    "published": {"type": "string"},
    "topic": {"type": "string"}
  },
  "required": ["title", "summary", "link", "published", "topic"]
}

valid_results = []
for item in final_results:
  try:
    jsonschema.validate(instance=item, schema=schema)
    valid_results.append(item)
  except jsonschema.ValidationError:
    pass

validDict = valid_results

# 8. Skriv ut i tabellform
table = PrettyTable()
table.field_names = ["Title", "Summary", "Link", "Published", "Topic"]

for item in validDict:
  table.add_row([item["title"], item["summary"], item["link"], item["published"], item["topic"]])

print(table)














"""
MLModelReturns_4.py

This script will:
  - Import 'MyTheFinalList' from FullRSSList_1_2.py
  - Import the trained model (best_clf_pipeline) + supporting objects (categories, vectorizer, etc.) 
    from MLModelMLC_3.py
  - Use the model to predict categories for the newly fetched RSS articles.
  - Combine the predictions with the final list from 'MyTheFinalList' and possibly produce a
    validated dictionary (validDict).

Students:
 - Complete the pseudo code to transform text, get predictions,
   and merge them with the 'MyTheFinalList'.


# 1) Imports
# from FullRSSList_1_2 import MyTheFinalList
# from MLModelMLC_3 import categories, vectorizer, best_clf_pipeline
# from RssFeedNewArticle_2 import printdepositlist

import jsonschema

def main():
    # Pseudo code steps:

    # 1. Take the final text from 'printdepositlist' (title+summary).
    #    If your "MyTheFinalList" has its own text, decide which you want to feed to the model.
    #    For instance:
    #       my_text = printdepositlist

    # 2. Clean up or filter empty strings from 'my_text' if necessary.
    #       my_text_no_empty = [t for t in my_text if t.strip() != ""]

    # 3. Transform text with the same vectorizer used during training:
    #       my_text_transformed = vectorizer.transform(my_text_no_empty)

    # 4. Use best_clf_pipeline to get probabilities:
    #       predictions = best_clf_pipeline.predict_proba(my_text_transformed)

    # 5. Compare each probability to a threshold to decide which categories apply:
    #       threshold = 0.3
    #       results = {}  # dict of text -> list of predicted categories
    #       for idx, pvector in enumerate(predictions):
    #           text = my_text_no_empty[idx]
    #           # results[text] = ...
    #           # loop through each category probability in pvector

    # 6. Combine 'results' with 'MyTheFinalList'.
    #    Typically, you want to match each text to the corresponding item in MyTheFinalList.
    #    That might mean using indexes if the order is guaranteed to match.

    # 7. Create a final list of dicts (e.g., key_list = ['title','summary','link','published','topic'])
    #    Each dict must have the correct shape (like in your example).
    #    finalDict = [dict(zip(key_list, v)) for v in combinedList]

    # 8. (Optional) Validate the final dictionaries with a JSON schema:
    #     schema = {
    #       "type": "object",
    #       ...
    #     }
    #     valid_list = []
    #     for item in finalDict:
    #         try:
    #             jsonschema.validate(instance=item, schema=schema)
    #             valid_list.append(item)
    #         except:
    #             pass
    # 
    #     validDict = valid_list
    #
    # 9. Print or return 'validDict' so it can be imported in DbTransfer_5.py

    pass  # Remove this line when you implement the logic


# Ensure the script runs if executed directly
if __name__ == "__main__":
    main()
"""