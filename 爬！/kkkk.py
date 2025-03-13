import scrapy
# 以京东大米为例（需安装Scrapy+Selenium）
class JDPriceSpider(scrapy.Spider):
    name = 'jd_price'
    start_urls = ['https://www.jd.com/']

    def parse(self, response):
        # 解析商品列表页
        for product in response.css('div.product-item'):
            yield {
                'province': product.xpath('.//div[@class="location"]/text()').get(),
                'price': product.css('span.price::text').get().replace('￥', ''),
                'spec': product.xpath('.//div[@class="spec"]/text()').get()
            }
        # 翻页处理（需模拟浏览器行为）
        if next_page := response.css('a.next-page::attr(href)').get():
            yield response.follow(next_page, self.parse)