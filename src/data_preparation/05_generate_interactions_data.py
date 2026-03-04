#Use the ai-recommendation-engine as project root folder as links are all relative to that
#Creating interactions taking user data and product data from clean csv files
import random
import pandas as pd

print("Starting Interaction data generation...")
#Reads users and product clean data from csv and store it in form of DataFrame
users = pd.read_csv("../ai-recommendation-engine/data/processed/users_clean.csv") 
products = pd.read_csv("../ai-recommendation-engine/data/processed/products_clean.csv")

product_catalog = {}

#Split product_ids based on categories of products and store that categories as keys of product_catalog
#Ex: product_catalog = {"electronics":['P101',...],...}
for _,row in products.iterrows():
    p_id = row["pr_id"]
    category = row["pr_category"]

    if category not in product_catalog:
        product_catalog[category] = []
    product_catalog[category].append(p_id)

#Created an order and then defined probability for each group of users based on employement on what they are likely to buy
categories_order = ["daily_essential","fashion","grocery","electronics","luxury"]

# Students: Love Fashion & Tech
weights_student = [0.05, 0.40, 0.05, 0.45, 0.05] 
# Employed: Love Luxury & Tech
weights_employed = [0.05, 0.20, 0.05, 0.30, 0.40] 
# Not Employed: Focus on Essentials/Grocery
weights_unemployed = [0.40, 0.10, 0.40, 0.05, 0.05] 
# Default: Equal spread
weights_default = [0.20, 0.20, 0.20, 0.20, 0.20]


interactions = []

#Creating a list ambigious interactions consisting of 4 unique interaction types: view, cart, wishlist, purchase
interaction_type = ["view","View","VIEW","Cart ","cart","Wishlist ","WISHLIST","wishlist","purchase","Purchase ",None]

#Optimisation used dict to directly find user_id and employement labels instead of searching in df which is slow
#Dictionary format: {'U1': 'student', 'U2': 'employed'...}
user_lookup = pd.Series(users.employment_status.values, index=users.user_id).to_dict() #made a series then converted to dict
all_user_ids = list(user_lookup.keys())

#Creating popular products that sells the most(creating overlapping)
popular_products = {}

for cat,item_list in product_catalog.items():

    limit = max(1, int(len(item_list)*0.2)) #20% of all items are popular products in each category, max for if 20% of any category < 1, then it will choose atleast 1

    popular_products[cat] = item_list[:limit] #Append 20% of products inside respective category in popular products

#Creating 16000 interactions data
for i in range(16000):

    u_id = random.choice(all_user_ids) 
    
    #Check their Status (Student? Employed?) "missing" is for safety if value is not present for certain "user_id" it takes missing
    status = user_lookup.get(u_id, "missing")
    
    #Set Probabilities based on Status
    if status == "student":
        current_weights = weights_student
    elif status == "employed":
        current_weights = weights_employed
    elif status == "not_employed":
        current_weights = weights_unemployed
    else:
        current_weights = weights_default

    #Pick a Category using those weights (The "Bias") used choices that works with weights ex 5% of choosing one category 40% of another, random.choice is fair(does not take weights) this is the core of choosing pr_id with categories for user_ids
    #It is like a roulette wheel, k=1 says spin 1 time, choices always return a list [0] says to extract the first element
    #This ensures a Student is 5x more likely to pick Electronics than Grocery
    chosen_cat = random.choices(categories_order, weights=current_weights, k=1)[0]
    
    # E. Pick a random Product from that SPECIFIC category
    # (Safety check: if category is empty, pick random to avoid crash)
    if chosen_cat in product_catalog and len(product_catalog[chosen_cat]) > 0:
        
        #random.random() chooses a number between 0.0 to 1.0 so 70% chance of being true and if there are products inside chosen category in popular products then choose a random product label
        if random.random() < 0.7 and len(popular_products[chosen_cat]) > 0:
            p_id = random.choice(popular_products[chosen_cat])
        
        #If if does not exexute choose any product from chosen category
        else:
            p_id = random.choice(product_catalog[chosen_cat])
    else:
        p_id = random.choice(products["pr_id"].to_list())

    interactions_data = {

        "user_id" : u_id,
        "pr_id" : p_id,
        "interaction_type" : random.choice(interaction_type)
    }
    interactions.append(interactions_data)

#Converting list of dictionaries to dataframes and storing it in df
df = pd.DataFrame(interactions)
print("Interaction data generation success!\n")

#Converting dataframe to .csv file
df.to_csv("../ai-recommendation-engine/data/raw/interactions_raw.csv",index=False)

print("File saved as interactions_raw.csv under ai-recommendation-engine/data/raw/")

#Note: we have created synthetic data using random so we explicitly created overlapping(commoness/clusters) between things so that model learns from it, but if we have used public datasets overlapping naturally exists due to human nature in that scenario we do the opposite remove rare items like items sold only once or few because it confuses the model.