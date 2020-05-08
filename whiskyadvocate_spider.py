from spider import Spider, Request
from whiskyadvocate.items import WhiskyadvocateItem
import re
import math

class WhiskyAdvocateSpider(Spider):
	name = 'whiskyadvocate_spider'
	allowed_urls = ['https://www.whiskyadvocate.com']
	start_urls = ['https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=+&brand_id=0&rating=0&price=0&category=0&styles_id=0&issue_id=0']

	def parse(self, response):
		page_sort = ['95-100','90-94', '80-89', '70-79', '60-69']
		result_urls = ['https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=+&brand_id=0&rating={}&price=0&category=0&styles_id=0&issue_id=0'.format(x) for x in page_sort]
		
		# num_items_str = response.xpath('//div[@class="wrap"]/text()').extract()
		# groups = re.search('Your search returned (\d+) results.', text)
		# num_items = int(groups.group(1))


		for url in result_urls:
			yield Request(url = url, callback = self.parse_result_page)

	def parse_result_page(self, response):
		blocks = response.xpath('//div[@class="m-all t-1of3 d-1of3 col cf align-items-stretch showmore"]')

		for block in blocks:
			brand, abv = response.xpath('//h1[@itemprop="name"]/text()').extract().split(', ')
			abv = float(round(abv, 1))
			rating = int(response.xpath('//h2/span[@itemprop="ratingValue"]/text()').extract())
			style = response.xpath('//span/span[@itemprop="category"]/text()').extract()
			price = int(response.xpath('//span/span[@content="USD"]/text()').extract())
			review =  response.xpath('//div[@itemprop="description"]/p/text()').extract()
			reviewer = response.xpath('//div/p/span[@itemprop="author"]/text()').extract()

			item = WhiskyadvocateItem()
			item['brand'] = brand
			item['abv'] = abv
			item['rating'] = rating
			item['style'] = style
			item['price'] = price
			item['review'] = review
			item['reviewer'] = reviewer

			yield item