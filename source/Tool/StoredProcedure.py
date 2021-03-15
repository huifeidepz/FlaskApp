# -*- coding:utf8 -*-
import sys

sys.path.append("..")
from source.Tool import DBconn


class StoredPd(object):
    def __init__(self):
        self.DB = DBconn.DBconn()

    def insertPostBar(self, PostBar):  # 保存贴吧
        sql = "INSERT INTO `tiebaspider`.`postbar` (`PostBarID`) VALUES ('{}');".format(
            PostBar)
        bo = self.DB.execute_insert(sql)
        return bo

    def UpdatePostBar(self,PostBar):
        sql = "UPDATE `tiebaspider`.`postbar` SET `PostpageNum`='{}',`FollowNum`='{}' WHERE `PostBarID`='{}';".format(PostBar[1],PostBar[2],PostBar[0])
        bo = self.DB.execute_insert(sql)
        return bo

    def insertPostPage(self, PostPage):  # 保存帖子
        insertSql = "INSERT  INTO `postpage` (`PostPageID`, `PostPageTitle`, `UserID`, `PostBarID`, `ReplyNum`) VALUES ('{}', '{}', '{}', '{}', '{}');".format(
            PostPage[0], PostPage[1], PostPage[2], PostPage[3], PostPage[4])
        bo = self.DB.execute_insert(insertSql)
        if not bo:
            sql = "UPDATE `postpage` SET `ReplyNum`={} WHERE `PostPageID`='{}'".format(PostPage[0], PostPage[4])
            bo = self.DB.execute_insert(sql)
        return bo

    def insertComment(self, Comment):  # 保存评论
        sql = "INSERT IGNORE INTO `comment` (`CommentID`, `UserID`, `PostPageID`, `Content`, `UserLeveL`, `Time`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(
            Comment[0], Comment[1], Comment[2], Comment[3], Comment[4], Comment[5])
        bo = self.DB.execute_insert(sql)
        return bo

    def insertUser(self, User):  # 保存用户
        sql = "INSERT  IGNORE INTO `user` (`UserID`, `UserName`) VALUES ('{}', '{}');".format(User[0],
                                                                                              User[1])
        bo = self.DB.execute_insert(sql)
        return bo

    def GetAllPostBar(self):
        sql = "SELECT PostBarID FROM tiebaspider.postbar;"
        PostBars = self.DB.execute_fetchall(sql)
        return list(PostBars)

    def insertlog(self, log):
        sql = "INSERT INTO `log` (`Content`, `time`) VALUES ('{}', '{}')".format(log[0], log[1])
        bo = self.DB.execute_insert(sql)
        return bo

    def UpdateLastPage(self, PageNum, PageID):
        sql = "UPDATE `postpage` SET `LastPageNum`={} WHERE `PostPageID`='{}'".format(PageNum, PageID)
        bo = self.DB.execute_insert(sql)
        return bo

    def deletePostPage(self, PageID):
        sql = "DELETE FROM `postpage` WHERE `PostPageID`='{}'".format(PageID)
        bo = self.DB.execute_insert(sql)
        return bo

    def UpdatePageByComment(self):
        select = "SELECT DISTINCT PostPageID FROM comment ;"
        bo = self.DB.execute_fetchall(select)
        return bo

    def UpdateTurePostPageisUpdate(self, PostPageID):
        sql = "UPDATE `postpage` SET `isUpdate`=1 WHERE `PostPageID`='{}'".format(PostPageID)
        bo = self.DB.execute_insert(sql)
        return bo

    def UpdateFalsePostPageisUpdate(self, PostPageID):
        sql = "UPDATE `postpage` SET `isUpdate`=0 WHERE `PostPageID`='{}'".format(PostPageID)
        bo = self.DB.execute_insert(sql)
        return bo

    def GetAllUpdatePostPage(self):
        sql = "SELECT PostPageID,LastPageNum FROM postpage WHERE  isUpdate = 1"
        bo = self.DB.execute_fetchall(sql)
        return bo

    def GetAllPostBarTotal(self, PostBarID):
        pagesql = "select count(*) from postpage where PostBarID = '{}'".format(PostBarID)
        commentsql = "select count(*) from  comment where PostPageID in (select PostPageID from postpage where PostBarID = '{}')".format(
            PostBarID)
        bo1 = self.DB.execute_fetchall(pagesql)
        bo2 = self.DB.execute_fetchall(commentsql)
        return [bo1[0][0], bo2[0][0]]

    def GetAllComments(self):
        # sql = "SELECT count(*) FROM comment WHERE Content != ''"
        # sql = "SELECT CommentID,Content FROM comment WHERE Content != ''"
        clear = "DELETE  FROM `comment`  WHERE `Content` =''"
        self.DB.execute_insert(clear)
        sql = "SELECT CommentID,Content FROM comment WHERE Content != '' AND PosORNeg is NULL"
        bo = self.DB.execute_fetchall(sql)
        return bo

    def UpdatePosOrNeg(self, CommentID, PosOrNeg):
        sql = "UPDATE comment SET PosORNeg='{}' WHERE CommentID='{}'".format(PosOrNeg, CommentID)
        self.DB.execute_insert(sql)

    def GetCommetPosOrNegbyPostBar(self, PostBar):
        sql = "SELECT PosORNeg FROM comment WHERE PostPageID in (SELECT PostPageID FROM postpage WHERE PostBarID = '{}' AND PosORNeg is not NULL)".format(
            PostBar)
        bo = self.DB.execute_fetchall(sql)
        return bo

    def GetConfig(self, Config):
        sql = "SELECT * FROM tiebaspider.config where idconfig = '{}'".format(Config)
        bo = self.DB.execute_fetchall(sql)
        return bo

    def UpdateConfig(self, Config, Value):
        sql = "UPDATE `tiebaspider`.`config` SET `Valueconfig` = '{}' WHERE (`idconfig` = '{}');".format(Value, Config)
        bo = self.DB.execute_insert(sql)
        return bo

    def GetPostBarUserByLevel(self, PostBarID):
        sql = "SELECT `UserLeveL`, COUNT( `UserLeveL`)  FROM `comment`   WHERE `PostPageID` IN ( SELECT `PostPageID` FROM `postpage` WHERE `PostBarID` ='{}' )GROUP BY `UserLeveL`".format(
            PostBarID)
        bo = self.DB.execute_fetchall(sql)
        return bo

    def GetDataGroupByBar(self):
        sql = "SELECT `postpage`.`PostBarID`,COUNT(DISTINCT `postpage`.`PostPageID` ),COUNT( *) FROM `comment`, `postpage` WHERE  `postpage`.`PostPageID`= `comment`.`PostPageID`  GROUP BY `PostBarID`"
        bo = self.DB.execute_fetchall(sql)
        return bo
