import csv
import requests

product_crawled_count = 0

# header
with open(f"data.csv" , "w" , encoding="UTF-8" , newline="") as file:
	writer = csv.writer(file)
	writer.writerow([
     	"name",
		"min_price",
		"max_price",
		"online_store_count",
		"physical_store_count",
		"product_client_url",
		"product_more_info_api"
  	])

def store_data(
	name,
	min_price,
	max_price,
	online_store_count,
	physical_store_count,
	product_client_url,
	product_more_info_api
):
	with open(f'data.csv', 'a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([
      		name,
            min_price,
            max_price,
            online_store_count,
            physical_store_count,
            product_client_url,
            product_more_info_api
        ])
    
def crawl_data(search_page_url):
	search_response = requests.get(search_page_url)
	search_response_json = search_response.json()
	search_results = search_response_json["results"]
 
	for post in search_results:
		global product_crawled_count
		product_client_url = "https://torob.com" + post["web_client_absolute_url"]
		product_more_info_api = post["more_info_url"]
		product_response = requests.get(product_more_info_api)
		product_results = product_response.json()
		name = product_results["name1"]
		min_price = product_results["min_price"]
		max_price = product_results["max_price"]
		online_store_count = len(product_results["products_info"]["result"])
		physical_store_count = len(product_results["products_in_store_info"]["result"])

		store_data(
			name,
			min_price,
			max_price,
			online_store_count,
			physical_store_count,
			product_client_url,
			product_more_info_api
		)
		product_crawled_count += 1
		print(product_crawled_count)

	next_search_page_url = search_response_json["next"]
	return next_search_page_url


def main(search_page_url):
	next_search_page_url = crawl_data(search_page_url)

	while next_search_page_url:
		next_search_page_url = crawl_data(search_page_url)

category_id = 175
category_api = f"https://api.torob.com/v4/base-product/search/?page=0&sort=popularity&size=24&category={category_id}"

main(category_api)