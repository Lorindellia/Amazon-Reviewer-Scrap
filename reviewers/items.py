# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    reviewer_id = scrapy.Field()
    reviewer_name = scrapy.Field()
    total_reviews_count = scrapy.Field()
    top_ranking = scrapy.Field()
    total_helpful_votes = scrapy.Field()
    # product_name = scrapy.Field()
    asin = scrapy.Field()
    review_link = scrapy.Field()
    review_id = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    helpful_votes = scrapy.Field()
    total_votes = scrapy.Field()
    date = scrapy.Field()
    comments_count = scrapy.Field()
    verified = scrapy.Field()
    images_count = scrapy.Field()
    has_video = scrapy.Field()
    pass
