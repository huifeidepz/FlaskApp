# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from urllib.parse import unquote
from source.Tool.StoredProcedure import StoredPd
import sys
sys.path.append("..")

class PostSpiderPipeline(object):
    def __init__(self):
        self.StorePd = StoredPd()

    def process_item(self, item, spider):
        if item.name == "PostPageItem":
            self.StorePostPage(item)
        else:
            self.StoreComment(item)

    def StoreComment(self, item):
        Comment = [item['CommentID'], item['UserID'], item['PostPageID'], item['Content'], item['UserLeveL'],
                   item['Time']]
        User = [item['UserID'], item['UserName']]
        self.StorePd.insertComment(Comment)
        self.StorePd.insertUser(User)

    def StorePostPage(self, item):
        PostBarID = unquote(item["PostBarID"])
        PostPage = [item["PostPageID"], item["PostPageTitle"], item["UserID"], PostBarID, item["ReplyNum"]]
        bo = self.StorePd.insertPostPage(PostPage)
        if bo > 0:
            self.StorePd.UpdateTurePostPageisUpdate(PostPage[0])
