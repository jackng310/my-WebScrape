from scrapy import Spider, Request
from whiskyadvocate.items import WhiskyadvocateItem
import re
import math

class WhiskyAdvocateSpider(Spider):
	name = 'whiskyadvocate_spider'
	allowed_urls = ['https://www.whiskyadvocate.com']
	start_urls = ['https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=+&brand_id=0&rating=95-100&price=0&category=0&styles_id=0&issue_id=0']

	def parse(self, response):
		page_sort = ['95-100','90-94++', '80-89', '70-79', '60-69']
		result_urls = ['https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=+&brand_id=0&rating={}&price=0&category=0&styles_id=0&issue_id=0'.format(x) for x in page_sort]
		
		# num_items_str = response.xpath('//div[@class="wrap"]/text()').extract()
		# groups = re.search('Your search returned (\d+) results.', text)
		# num_items = int(groups.group(1))


		for url in result_urls:
			yield Request(url = url, callback = self.parse_result_page)

	def parse_result_page(self, response):
		blocks = response.xpath('//div[@class="m-all t-1of3 d-1of3 col cf align-items-stretch showmore"]')
		
		for block in blocks:
			brand= block.xpath('.//h1[@itemprop="name"]/text()').extract_first()
			rating = int(block.xpath('.//h2/span[@itemprop="ratingValue"]/text()').extract_first())
			category = block.xpath('.//span/span[@itemprop="category"]/text()').extract_first()
			if ',' in block.xpath('.//span/span[@content="50.00"]/text()').extract_first():
				price = float(re.findall('\d+', block.xpath('.//span/span[@content="50.00"]/text()').extract_first().replace(',',''))[0])
			elif '\d+.[\d+]' in block.xpath('.//span/span[@content="50.00"]/text()').extract_first():
				price = float(re.findall('\d+.[\d+]',block.xpath('.//span/span[@content="50.00"]/text()').extract_first())[0])
			else:
				price = float(re.findall('\d+', block.xpath('.//span/span[@content="50.00"]/text()').extract_first())[0])
			review = block.xpath('.//div[@itemprop="description"]/p/text()').extract_first() or block.xpath('.//div/p/span[@style="font-weight: 400;"]/text()').extract_first() or block.xpath('.//span[@class="s1"]/text()').extract_first() or block.xpath('.//span[@style="letter-spacing: .05pt;"]/text()').extract_first()
			reviewer = block.xpath('.//div/p/span[@itemprop="author"]/text()').extract_first()

			item = WhiskyadvocateItem()
			item['brand'] = brand
			item['rating'] = rating
			item['category'] = category
			item['price'] = price
			item['review'] = review
			item['reviewer'] = reviewer

			yield item