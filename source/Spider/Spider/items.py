# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import sys
sys.path.append("..")
import scrapy


class PostPageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = "PostPageItem"
    PostPageID = scrapy.Field()
    PostPageTitle = scrapy.Field()
    UserID = scrapy.Field()
    PostBarID = scrapy.Field()
    ReplyNum = scrapy.Field()


class CommentItem(scrapy.Item):
    name = "CommentItem"
    CommentID = scrapy.Field()
    PostPageID = scrapy.Field()
    Content = scrapy.Field()
    UserLeveL = scrapy.Field()
    Time = scrapy.Field()
    UserID = scrapy.Field()
    UserName = scrapy.Field()
