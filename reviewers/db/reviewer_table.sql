DROP TABLE IF EXISTS amazon_crawl.reviewers;
CREATE TABLE amazon_crawl.reviewers (
reviewer_id varchar(255),
asin varchar(255),
reviewer_name text,
total_reviews_count varchar(255),
top_ranking varchar(255),
total_helpful_votes varchar(255),
review_link varchar(255),
review_id varchar(255),
title text,
rating double,
helpful_votes varchar(45),
total_votes varchar(45),
verified int,
comments_count varchar(45),
images_count varchar(45),
has_video int,
text text,
updated datetime,
PRIMARY KEY(reviewer_id, asin)
) DEFAULT CHARSET=utf8;
