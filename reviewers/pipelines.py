from datetime import datetime
import mysql.connector as MS

# Credentials of your db
HOSTNAME = '<YOUR_HOSTNAME>' # If running locally, its localhost.
USERNAME = '<YOUR_USERNAME>'
PASSWORD = '<YOUR_PASSWD>'
DB_NAME = '<YOUR_DB_NAME>'
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MySQLStorePipeline(object):
    def __init__(self):
        # create an object to check whether the book has been added
        # self.ids_seen = set()
        # create a connection object to the database
        self.conn = MS.connect(host= HOSTNAME, user= USERNAME, passwd= PASSWORD, db= DB_NAME)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        insert_book = (
        "INSERT INTO reviewers (reviewer_id, asin, reviewer_name, total_reviews_count, top_ranking,total_helpful_votes,review_link,review_id, "
        "rating, title, text, helpful_votes, total_votes, comments_count, verified, images_count, has_video, updated)"
        "VALUES (%(reviewer_id)s, %(asin)s, %(reviewer_name)s, %(total_reviews_count)s, "
        "%(top_ranking)s,%(total_helpful_votes)s,%(review_link)s,%(review_id)s,%(rating)s,%(title)s,%(text)s,%(helpful_votes)s,"
        "%(total_votes)s,%(comments_count)s,%(verified)s,%(images_count)s,%(has_video)s, %(updated)s)")
        # data object
        data_book = {'reviewer_id': item['reviewer_id'],
                     'asin': item['asin'],
                     'reviewer_name': item['reviewer_name'],
                     'total_reviews_count': item['total_reviews_count'],
                     'top_ranking': item['top_ranking'],
                     'total_helpful_votes': item['total_helpful_votes'],
                     'review_link': item['review_link'],
                     'review_id': item['review_id'],
                     'rating': item['rating'],
                     'title': item['title'],
                     'text': item['text'],
                     'helpful_votes': item['helpful_votes'],
                     'total_votes': item['total_votes'],
                     'verified': item['verified'],
                     'comments_count': item['comments_count'],
                     'images_count': item['images_count'],
                     'has_video': item['has_video'],
                     'updated': now,
                     }
        # execute the insert query
        try:
            self.cursor.execute(insert_book, data_book)
            self.conn.commit()
            print bcolors.OKGREEN + "success, inserted into database" + bcolors.ENDC
        except Exception as e:
            print bcolors.FAIL + "error, not inserted" + bcolors.ENDC
            print e
            print data_book
