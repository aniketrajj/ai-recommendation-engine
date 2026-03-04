#File used for earlier Item-based Collaborative Filtering model to split train and test data.

#Use the ai-recommendation-engine as project root folder as links are all relative to that
#With this file the purpose is to split the complete user_item_matrix_full.csv into training and testing data
#Here from each user_id we are just hiding one interaction to keep it simple
import random
import pandas as pd

print("Starting the splitting process...\n")

#Read the complete user_item_matrix and store it in df
user_matrix = pd.read_csv("../ai-recommendation-engine/data/processed/user_item_matrix_full.csv", index_col=0)

#Create a copy of the df to make changes here
train_user_matrix = user_matrix.copy()

hidden_interactions = []

#Iterate over each user in matrix
for u_id in train_user_matrix.index:
    pr_ids = train_user_matrix.loc[u_id] #Returns a series with pr_id as index and interaction_weights as values for each u_id
    
    valid_interactions = pr_ids[pr_ids>0] #Only store those pr_ids where weight>0, valid_interactions is a series
    
    #To check if there are more than 2 interactions, if there are too few interactions for a u_id do not perform splitting as there is very few info.
    if valid_interactions.count() < 2:
        continue
    
    pr_id = random.choice(valid_interactions.index) #Choose a random p_id from valid_interactions series
    value = valid_interactions[pr_id] #Extract the real weight in value
    train_user_matrix.loc[u_id,pr_id] = 0 #Set the interaction as 0
    
    #Dictionary containing the real details for the changed interactions
    item = {
        "user_id" : u_id,
        "pr_id" : pr_id,
        "interaction_weight" : value
    }
    
    hidden_interactions.append(item)

#Converting list of dictionaries to pandas Dataframe with keys as column names
test_interactions = pd.DataFrame(hidden_interactions)

train_user_matrix.to_csv("../ai-recommendation-engine/data/processed/user_item_matrix_train.csv")
print("Training data stored as user_item_matrix_train.csv under ai-recommendation-engine/data/processed")

test_interactions.to_csv("../ai-recommendation-engine/data/processed/test_interactions.csv", index=False)
print("Testing data stored as test_interactions.csv under ai-recommendation-engine/data/processed")

#If len used with DataFrame it returns the total number of rows
print(f"Total hidden interactions: {len(test_interactions)}")
print("\nSplitting completed successfully!")
