import json
import sys

sys.path.append("..")
import scrapy

from source.Spider.Spider.items import PostPageItem, CommentItem
from source.Tool import helper, Common
from urllib.parse import unquote


class PostSpider(scrapy.Spider):
    name = 'PostSpider'
    allowed_domains = ['tieba.baidu.com']

    def start_requests(self):
        for url in Common.GetPostPagesUrls():
            yield scrapy.Request(
                url="https://tieba.baidu.com/f?kw=" + str(url) + "&ie=utf-8&pn=1",
                callback=self.parse
            )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def parse(self, response):

        NextPage = "https:" + str(
            response.xpath(
                '//*[@id="frs_list_pager"]/a[contains(@class,"next")]/@href').extract_first())
        # //*[@id="frs_list_pager"]/a[10]
        # /html/body/div[2]/div/div[2]/div/div/div[1]/div/div/div/div[4]/div/div[1]/a[10]
        # /html/body/div[2]/div/div[2]/div/div/div[1]/div/div/div/div[4]/div/div[1]/a[12]
        PostBarID = unquote(response.url.split("=", 4)[1].split("&", 2)[0])
        PageNum = 0
        for sel in response.xpath('//li[contains(@class, "j_thread_list")]'):
            data = json.loads(sel.xpath('@data-field').extract_first())
            # //*[@id="thread_list"]/li[5]/div/div[2]/div[2]/div[2]/span[1]
            item = PostPageItem()
            PostPageID = data['id']
            item['PostPageID'] = PostPageID

            item['PostPageTitle'] = sel.xpath(
                './/div[contains(@class, "threadlist_title")]/a/@title').extract_first()
            item['UserID'] = data["author_portrait"]
            item['PostBarID'] = PostBarID
            item["ReplyNum"] = data['reply_num']
            item['PostPageTitle'] = sel.xpath(
                './/div[contains(@class, "threadlist_title")]/a/@title').extract_first()
            yield item
            PageNum += 1
            url = "https://tieba.baidu.com/p/{}".format(PostPageID)
            meta = {"PostPageID": item['PostPageID']}
            yield scrapy.Request(url, callback=self.parse_comment, meta=meta,
                                 headers=Common.getHeader())

        if NextPage is not None:
            yield scrapy.Request(NextPage, callback=self.parse, headers=Common.getHeader())

    def parse_comment(self, response):
        meta = response.meta.copy()
        PostPageID = meta["PostPageID"]
        has_comment = False
        for floor in response.xpath("//div[contains(@class, 'l_post')]"):
            if not helper.is_ad(floor):
                data = json.loads(floor.xpath("@data-field").extract_first())
                item = CommentItem()
                commentNum = data['content']['comment_num']
                if commentNum > 0:
                    has_comment = True
                item['CommentID'] = data['content']['post_id']
                item['UserID'] = data['author']['portrait'].split("?", 2)[0]
                item['UserName'] = data['author']["user_name"]
                item['UserLeveL'] = floor.xpath('.//div[@class="d_badge_lv"]/text()').extract_first()
                content = floor.xpath(".//div[contains(@class,'j_d_post_content')]").extract_first()
                # 以前的帖子, data-field里面没有content
                item['Content'] = helper.parse_content(content)
                # 以前的帖子, data-field里面没有thread_id
                item['PostPageID'] = PostPageID
                # 只有以前的帖子, data-field里面才有date
                if 'date' in data['content'].keys():
                    item['Time'] = data['content']['date']
                    # 只有以前的帖子, data-field里面才有date
                else:
                    item['Time'] = floor.xpath(".//span[@class='tail-info']") \
                        .re_first(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

                yield item

                if has_comment:
                    json_pid = floor.xpath('.//div[@class="j_lzl_r p_reply"]/@data-field').extract_first()
                    if json_pid is not None:
                        pid = json.loads(json_pid)["pid"]
                        url = "https://tieba.baidu.com/p/comment?tid=" + str(PostPageID) + "&pid=" + str(pid) + "&pn=1"
                        metac = {"PostPageID": PostPageID, "pid": pid}
                        yield scrapy.Request(url, callback=self.parse_lzl, meta=metac,
                                             headers=Common.getHeader())

        temp = response.xpath(
            '//*[@id="thread_theme_5"]/div[1]/ul/li[1]/a[text()="下一页"]/@href').extract_first()
        # /html/body/div[4]/div/div[2]/div/div[5]/div[1]/div[1]/ul/li[1]/a[6]
        # /html/body/div[4]/div/div[2]/div/div[5]/div[1]/div[1]/ul/li[1]/a[8]
        # /html/body/div[4]/div/div[2]/div/div[5]/div[1]/div[1]/ul/li[1]/a[6]
        if temp is not None:
            NextPage = temp.split("=", 2)[1]
            url = "https://tieba.baidu.com/p/{}?pn={}".format(PostPageID, NextPage)

            meta = {"PostPageID": PostPageID}
            yield scrapy.Request(url, callback=self.parse, meta=meta,
                                 headers=Common.getHeader())

    def parse_lzl(self, response):
        meta = response.meta.copy()
        temp = response.xpath('//p[@class="j_pager l_pager pager_theme_2"]/a[text()="下一页"]/@href').extract_first()
        if temp is not None:
            NextPage = temp[1:]
        else:
            NextPage = None
        for floor in response.xpath("//li[contains(@class,'lzl_single_post')]"):
            item = CommentItem()
            data = json.loads(floor.xpath('./@data-field').extract_first())
            item['CommentID'] = data['spid']
            item['UserID'] = data['portrait']
            item['UserName'] = data["user_name"].split("?", 2)[0]
            item['Content'] = \
                floor.xpath('.//span[@class="lzl_content_main"]').xpath('string(.)').extract_first().split(":", 2)[
                    -1].strip()
            item['UserLeveL'] = "0"
            item['PostPageID'] = meta["PostPageID"]
            item['Time'] = floor.xpath('.//div[@class="lzl_content_reply"]/span[3]/text()').extract_first()
            yield item
        if NextPage is not None:
            url = "https://tieba.baidu.com/p/comment?tid=" + str(meta["PostPageID"]) + "&pid=" + str(
                meta["pid"]) + "&pn=" + str(NextPage)
            yield scrapy.Request(url, callback=self.parse_lzl, meta=meta,
                                 headers=Common.getHeader())
