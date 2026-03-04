#Use the ai-recommendation-engine as project root folder as links are all relative to that
#Cleaning products_raw.csv using pandas

import pandas as pd

print("Starting product data cleaning...\n")

#Reading the file and storing it in a variable as DataFrame
raw_products = pd.read_csv("../ai-recommendation-engine/data/raw/products_raw.csv")
clean_products = raw_products.copy()

# print(clean_products.info())

#Cleaning data by columns 

#Cleaning column: pr_id
clean_products = clean_products.drop_duplicates(subset="pr_id")
clean_products = clean_products.dropna(subset=["pr_id"])
# print(clean_products.value_counts("pr_id", dropna=False))
# print(clean_products.info())

#Cleaning column: pr_category
# print(clean_products.value_counts("pr_category", dropna=False))
clean_products["pr_category"] = clean_products["pr_category"].str.lower().str.strip().str.replace(" ","_").replace("groceries","grocery")
# print(clean_products.value_counts("pr_category", dropna=False))

#Cleaning column: pr_label
# print(clean_products.value_counts("pr_label", dropna=False))
clean_products["pr_label"] = clean_products["pr_label"].fillna("missing")
# print(clean_products.value_counts("pr_label", dropna=False))

#Cleaning column: pr_cost
# print(clean_products.value_counts("pr_cost", dropna=False))
clean_products = clean_products.dropna(subset=["pr_cost"])

#Cleaning column: pr_rating
# print(clean_products.value_counts("pr_rating", dropna=False))
#Giving the least rating(3.0) by default for missing values
clean_products["pr_rating"] = clean_products["pr_rating"].fillna(3.0)

print(clean_products.info())
print("\nProduct data cleaned successfully!")

# print(clean_products.value_counts(subset="pr_category", dropna=False))
#Saving this clean_products dataframe into a new products_clean.csv file
clean_products.to_csv("../ai-recommendation-engine/data/processed/products_clean.csv", index=False)

print("File saved as products_clean.csv under ai-recommendation-engine/data/processed/")