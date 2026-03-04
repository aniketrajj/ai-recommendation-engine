#File used earlier in Item-based Collaborative Filtering Model to generate item-similarity matrix from user-item matrix 

#Use the ai-recommendation-engine as project root folder as links are all relative to that
#We are using item collaborative filtering recommendation algorithm which recommends similar products

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity #Using cosine_similarity to find similarity b/w two items

DATA_MODE = "train" # "full" or "train" 
print("Generating item-item similarity matrix...")
#Reading user-item matrix, index_col=0 replaces the default_index during read making user_id from a column to index
user_matrix = pd.read_csv(f"../ai-recommendation-engine/data/processed/user_item_matrix_{DATA_MODE}.csv", index_col=0)

#Transpose the matrix as we are using item-based CF and cosine similarity works on rows
transpose_user = user_matrix.T

#Used function cosine_similarity from sklearn.metrics.pairwise that compares two vectors and returns a value based on similarity, the more similar closer to 1 not-similar closer to 0
#EX: think of it a vector with 7 values and second vector with 7 values cosine_sim compares all values of both vectors & returns a single similarity value ranging 0-1
#cosine_similarity returns a numpy array(labels removed)

similarity_matrix = cosine_similarity(transpose_user)
# print(similarity_matrix)
# print(similarity_matrix.shape)

#Converting numpy array to dataframe re-attaching the labels
pr_similarity = pd.DataFrame(similarity_matrix, index=transpose_user.index, columns=transpose_user.index)

print("Item-item similarity matrix generation successful!\n")

#Storing the product-product similarity matrix under data/processed
pr_similarity.to_csv(f"../ai-recommendation-engine/data/processed/item_similarity_matrix_{DATA_MODE}.csv")
print(f"File saved as item_similarity_matrix_{DATA_MODE}.csv under ai-recommendation-engine/data/processed")

