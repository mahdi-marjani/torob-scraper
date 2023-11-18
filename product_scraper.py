import csv
import requests

input_query = input("product : ")


def get_data(page_url):
	data = []
	response = requests.get(page_url)
	results = response.json()["results"]
	for post in results:
		name = post["name1"]
		price =  post["price"]
		url = "https://torob.com" +post["web_client_absolute_url"]

		if price != 0 :
			data.append([name, price , url])
		
	next_page = response.json()["next"]
	while next_page :
		
		response = requests.get(next_page)
		results = response.json()["results"]
		
		for post in results:
			name = post["name1"]
			price =  post["price"]
			url = "https://torob.com" +post["web_client_absolute_url"]
			
			if price != 0 :
				data.append([name, price , url])
		
		next_page = response.json()["next"]
		print(len(data))
			
	return data


suggest_url = f'https://api.torob.com/suggestion2/?q={input_query}'
suggest_res = requests.get(suggest_url)
suggest_res_json = suggest_res.json()
category_list = []
for suggest in suggest_res_json:
	if 'category' in suggest.keys():
		category_list.append(suggest)
count = 0
for category in category_list:
	print(f"{count} - {category['category']['title']}")
	count+=1
category_index = int(input('Which category? : '))
category_id = category_list[category_index]['category']['id']

url = f"https://api.torob.com/v4/base-product/search/?page=0&sort=popularity&size=24&q={input_query}&discover_method=search_autocomplete&category={category_id}&source=next_desktop"

full_data = get_data(url)
if full_data :
	with open(f"{input_query}.csv" , "w+" , encoding="UTF-8" , newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["title" , "price", "url"])
		writer.writerows(full_data)		
else:
	print("nothing")
