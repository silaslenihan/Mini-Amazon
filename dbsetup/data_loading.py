import pandas as pd
import numpy as np
import psycopg2
from random import random
from random import seed

seed(23)
itemDataFrame = pd.read_csv('amazon_data_trimmed.csv')
userDataFrame = pd.read_csv('amazon_users.csv')

def generateReviewTable(total_items,buyer_list):

	rev_username = []
	rev_item = []
	rev_date_time = []
	rev_content = []
	rev_content = []
	rev_rating = []

	review_list = ["good","bad","terrible","meh","absolutely lovely!","confused","pretty nice","awesome","cool","super!","wow","astonishing","crazy","great","phenomenal","wasteful","best money ive spent","couldve been better","nothing wrong","could be worse","so so","would buy again","wouldnt buy again"]
	buyer_list = ["user1","user2","user3"]
	for count in range(1,total_items):
		num_reviews = int((random() * 3) + 1)
		for curr_rev in range(num_reviews):
			random_buyer = buyer_list[int(random()*len(buyer_list))]
			rand_review = review_list[int(random()*len(review_list))]
			rand_rating = round((random() * 4) + 1,2)

			rev_username.append(random_buyer)
			rev_item.append(count)
			rev_date_time.append('2020-01-0' + str(curr_rev))
			rev_content.append(rand_review)
			rev_rating.append(rand_rating)

def generateItemTable(itemDataFrame):
	item_ids = []
	cat_name = []
	item_name = []
	avg_rate = []
	total_rates = []
	descrip = []

	for count in range(1,len(itemDataFrame)):
		item_ids.append(count)
		if type(itemDataFrame['amazon_category_and_sub_category'][count]) is float:
			cat_name.append('Misc Toy/Item')
		else:
			cat_name.append(itemDataFrame['amazon_category_and_sub_category'][count].split(">")[-1][1:])
		item_name.append(itemDataFrame['product_name'][count])
		avg_rate.append(2.5)
		total_rates.append(0)
		if type(itemDataFrame['description'][count]) is float:
			descrip.append("this is an item")
		else:
			descrip.append(itemDataFrame['description'][count])

	item_table = {}
	item_table["item_id"] = item_ids
	item_table["cat_name"] = cat_name
	item_table["item_name"] = item_name
	item_table["avg_rate"] = avg_rate
	item_table["total_rates"] = total_rates
	item_table["descrip"] = descrip
	return item_table

def generateCategories(allCats,cur, conn):
	cat_name = []
	cat_descrip = []
	cat_name.append('Misc Toy/Item')
	cat_descrip.append('This is a category of item that fit based on category name')
	for descrip in allCats:
		if type(descrip) is not float:
			currCat = descrip.split(">")[-1][1:]
			if currCat not in cat_name:
				cat_name.append(currCat)
				cat_descrip.append('This is a category of item that fit based on category name')
	for index in range(len(cat_name)):
		category = cat_name[index]
		if "'" in cat_name[index]:
			dex= cat_name[index].index("'")
			category = cat_name[index][:dex]+cat_name[index][dex+1:]
		currCatName = "'" + str(category) + "'"
		currDescrip = "'" + str(cat_descrip[index]) + "'"
		insertCategory = "INSERT INTO Category VALUES (%s, %s);" % (currCatName, currDescrip)
		cur.execute(insertCategory)
	conn.commit()

def generateBuyersAndSellers(userDataFrame):
	usernames = userDataFrame['username']
	buyers = []
	sellers = []
	count = 0
	for user in usernames:
		if count%5 == 0:
			sellers.append(user)
		else:
			buyers.append(user)
		count = count+1
	split_users = {}
	split_users["buyers"] = buyers
	split_users["sellers"] = sellers
	return split_users

def generateSellsItems(item_table,seller_list):
	item_ids = item_table["item_id"]
	cat_names = item_table["cat_name"]

	seller_username = []
	item_id = []
	cat_name = []
	price = []
	stock = []

	for index in range(len(item_ids)):
		seller_username.append(seller_list[int(random()*len(seller_list))])
		item_id.append(item_ids[index])
		cat_name.append(cat_names[index])
		price.append(round(random()*100+5,2))
		stock.append(int(random() * 25 + 5))

'''
split_users = generateBuyersAndSellers(userDataFrame)
buyer_list = split_users["buyers"]
seller_list = split_users["sellers"]
generateReviewTable(len(itemDataFrame),buyer_list)
item_table = generateItemTable(itemDataFrame)
generateCategories(itemDataFrame['amazon_category_and_sub_category'],cur)
generateSellsItems(item_table, seller_list)
'''

conn = psycopg2.connect(
user="hshgoekz",
password="0-_hWpr8BBMyZe-EO1A0iwRTOEfZzGY8",
host="hattie.db.elephantsql.com",
port="5432"
)
cur = conn.cursor()

generateCategories(itemDataFrame['amazon_category_and_sub_category'],cur, conn)