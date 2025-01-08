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

url = f"https://api.torob.com/v4/base-product/search/?page=0&sort=popularity&size=24&query={input_query}&q={input_query}&source=next_desktop"

full_data = get_data(url)
if full_data :
	with open(f"{input_query}.csv" , "w+" , encoding="UTF-8" , newline="") as file:
		writer = csv.writer(file)
		writer.writerow(["title" , "price", "url"])
		writer.writerows(full_data)		
else:
	print("nothing")
