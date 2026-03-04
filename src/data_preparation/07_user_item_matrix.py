#Use the ai-recommendation-engine as project root folder as links are all relative to that
#Creating the user-item matrix from interactions_clean.csv using pandas

import pandas as pd

print("Creating user-item matrix...")

#Reading the interactions_clean.csv and storing it on a DataFrame
interactions_clean = pd.read_csv("../ai-recommendation-engine/data/processed/interactions_clean.csv")

# print(interactions_clean.value_counts("interaction_type"))

#Creating weight_map to map with interaction_type
weight_map = {
    "view" : 1,
    "wishlist": 2,
    "cart": 3,
    "purchase" : 5

}

interactions_clean['weight'] = interactions_clean["interaction_type"].map(weight_map)
#If any values left to add in weight_map it fills NaN with 0
interactions_clean["weight"] = interactions_clean["weight"].fillna(0)
# print(interactions_clean)

#Dropping the redudant col. interaction_type
interactions_clean = interactions_clean.drop(columns="interaction_type")
# print(interactions_clean.head())

#Similar user_id, pr_id pairs may exists, so we are using group-by to combine all those pairs and view max among all weight as we are using suprise library it prefers rating type values 1-5 instead of agg sum.
#Ex: a userA might have viewed a product 10 times (weight: 10) but a userB might have viewed and directly bought that same product (1+5=6), in the sum the userA is given more priority, viewer>buyer so to avoid this we are using max
#Grouping user_id and pr_id and converting multi-index as single index by using as_index=False, adding the columns weights and renaming it as total_weight
grouped_interactions = interactions_clean.groupby(["user_id", "pr_id"], as_index=False).agg(total_weight=("weight", "max"))
# print(grouped_interactions.head())


#Converting the user_id and pr_id as rows and cols respectively and total_weight as cell values using pandas pivot 
grouped_interactions = grouped_interactions.pivot(index="user_id", columns="pr_id", values="total_weight")
grouped_interactions = grouped_interactions.fillna(0)
# print(grouped_interactions)

print("User-item matrix created successfully!\n")
print(f"Users, Products: {grouped_interactions.shape} items")

#Saving the user-item matrix dataframe as .csv file
#In this user_item matrix the user_id is the index itself -> pivot (item CF based) 
grouped_interactions.to_csv("../ai-recommendation-engine/data/processed/user_item_matrix_full.csv")

print("File saved as user_item_matrix_full.csv under ai-recommendation-engine/data/processed")