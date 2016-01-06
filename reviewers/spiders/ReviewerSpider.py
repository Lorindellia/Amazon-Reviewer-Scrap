# __author__ = 'Tharun'
from reviewers.items import ReviewersItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import mysql.connector
# import csv

# with open('reviewers_links.csv', 'rU') as file:
#     rows = csv.reader(file)
#     rows.next()
#     urls = []
#     # urls.append('http://www.amazon.com/gp/cdp/member-reviews/A10HWQ7QGU5NET')
#     for row in rows:
#         asin = row[4].csvsplit('/')[-1]
#         urls.append('http://www.amazon.com/gp/cdp/member-reviews/{asin}'.format(asin=asin))

conn = mysql.connector.connect(user='root', password='1987Kevin', database='amazon_crawl')
cursor = conn.cursor()
query = ("select author_id from reviews")
cursor.execute(query)
author_ids = [x[0] for x in cursor]
author_list = []
for i in author_ids:
    author_list.append('http://www.amazon.com/gp/cdp/member-reviews/{author_id}'.format(author_id=i))
cursor.close()
conn.close()


# urls = ['http://www.amazon.com/gp/cdp/member-reviews/A10HWQ7QGU5NET']
class ReviewsSpider(CrawlSpider):
    name = "reviewers_spider"
    handle_httpstatus_list = [404]
    download_delay = 0.1
    allowed_domains = ["www.amazon.com"]
    start_urls = list(set(author_list))
    rules = (
        # Extract next links and parse them with the spider's method parse_item
        Rule(LinkExtractor(restrict_xpaths=('//td[@align="right" and @class="small" and @rowspan=2]/b/a',)),
             follow=True, callback='parse_start_url'),
    )

    def parse_start_url(self, response):
        reviewer_id = response.url.split("?")[0].split("/")[-1]
        reviewer_name = "".join(response.xpath('//b/a/span[@class="first"]/text()').extract()).strip()
        try:
            total_reviews_count = response.xpath('//div[@class="small"]/text()').extract()[1].split(':')[1].strip()
        except:
            total_reviews_count = 0

        top_ranking = response.xpath('//td/div[@class="tiny"]/text()').extract()[0].split(':')[1].strip()
        total_helpful_votes = response.xpath('//td/div[@class="tiny"]/text()').extract()[1].split(':')[1].strip()
        tables = response.xpath('//table[2][@cellspacing="0" and @cellpadding="0" and @border="0" and @width="100%"]')
        reviews = tables.xpath('//td[@colspan=7 and @class="small" and @align="left"]')
        for review in reviews:
            item = ReviewersItem()
            item['reviewer_id'] = reviewer_id.strip().encode('utf-8')
            item['reviewer_name'] = reviewer_name
            item['total_reviews_count'] = total_reviews_count
            item['top_ranking'] = top_ranking
            item['total_helpful_votes'] = total_helpful_votes
            # product_link = ''.join(review.xpath('//td[@align="left" and @colspan="2"]/b/a/@href').extract())
            # item['product_name'] = ''.join(review.xpath('//td[@align="left" and @colspan="2"]/b/a/text()').extract())
            # item['asin'] = product_link.split('/')[-2] if product_link else "NULL"
            # item['review_link'] = ''.join(review.xpath('//div[@style="padding-top: 10px; clear: both; width: 100%;"]/a[3]/@href').extract())
            item['review_link'] = ''.join(review.xpath('.//div[@class="tiny"]/b/a/@href').extract()).strip()
            item['review_id'] = item['review_link'].split('/')[-1]
            item['rating'] = ''.join(review.xpath('.//div[@style="margin-bottom:0.5em;"]/span/img/@alt').extract()).split('out')[0].strip()
            asin = review.xpath('.//div[@style="margin-bottom:0.5em;" and @class="tiny"]/b/a/@href').extract()
            if len(asin):
                item['asin'] = asin[0].split('/')[-1].strip().encode('utf-8')
            else:
                item['asin'] = "NULL"
            item['title'] = ''.join(review.xpath('.//div[@style="margin-bottom:0.5em;"]/b/text()').extract()).strip()
            item['date'] = ''.join(review.xpath('.//div[@style="margin-bottom:0.5em;"]/nobr/text()').extract()).strip()
            item['text'] = ''.join(review.xpath('.//div[@class="reviewText"]/text()').extract()).strip().encode('utf-8')
            votes_list = review.xpath('.//div[@style="margin-bottom:0.5em;"]/text()[contains(.,"helpful")]').extract()
            if len(votes_list):
                item['helpful_votes'] = votes_list[0].split('of')[0].strip()
                item['total_votes'] = votes_list[0].split('of')[1].strip().split(" ")[0].strip()
            else:
                item['helpful_votes'] = 0
                item['total_votes'] = 0
            comments_count = ''.join(review.xpath('.//div[@style="padding-top: 10px; clear: both; width: 100%;"]/a[2]/text()').extract())
            try:
                item['comments_count'] = comments_count.text.split('(')[1].split(')')[0].strip()
            except:
                item['comments_count'] = 0

            vp = ''.join(review.xpath('.//span[@class="crVerifiedStripe"]/b/text()').extract())
            if "Verified" in vp:
                item['verified'] = 1
            else:
                item['verified'] = 0

            if len(review.xpath('.//div[@class="reviewText"]/div').extract()):
                item['has_video'] = 1
            else:
                item['has_video'] = 0

            item['images_count'] = len(review.xpath('.//div[@style="overflow-x: hidden; overflow-y: hidden;"]/img').extract())

            yield item

        pass
