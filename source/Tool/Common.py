import sys

sys.path.append("..")
import random
import re

from datetime import datetime

from lxml import etree
import requests

from source.Tool.StoredProcedure import StoredPd
from source.Tool.RedisPro import RedisControl

RC = RedisControl()
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68"
]
cookies = [
    "BIDUPSID=F1A79E0CD42FEB47C44C9E2A07236422; PSTM=1610345810; BAIDUID=F1A79E0CD42FEB47A529D6DD44B930CB:FG=1; bdshare_firstime=1610355090204; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33425_33441_33272_33570_33584_26350_33266; wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1613697712,1613722697,1613722884,1613781450; st_key_id=17; BCLID=10082525747833442867; BDSFRCVID=JY0OJeC62ClZPone-3v8M3d6vhHQZzrTH6aoVp6FM5vqegToj7muEG0P8x8g0Kub6S2qogKKQgOTHRtF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tb4toK--tKt3jt-kKn7jKtI-MUCX5-CsJgKj2hcH0KLKbJ6GK5L-bt_sDtouJ-0qbJrB_JjSbfb1MRjv34j6XqK9yPD8h6vH3IrrKl5TtUJ48DnTDMRh-R-u-NJyKMniLCv9-pn4bpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuDjtBD5b0jGRabK6aKC5bL6rJabC3ox-9XU6q2bDeQNbpLRbI5C6q0xjztb--fxDxj4jPjp0vWtvJWbbvLT7johRTWqR48xFGMMonDh83b4RHelTJHCOOVp5O5hvvhb3O3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_Et5tttbCH_KvjbRj_jRTpqRQaq4tehHRqWxc9WDTm_DoTBInHhPQNqfckMxrybajqapRW-Nrq-pPKKR7jqPnv5j3rbtnBKp5i0UvH3mkjbpbGfn02OpDzMM8We-4syPRIKMRnWNrJKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFaMIIxjT_-ePDyqx5Ka43tHD7yWCkaQMJcOR59K4nnDpKA5nQ-e4vaW2De0IQKLCt-elL63MOZXb0g5n7Tbb8eBgvZ2UQkyD5ssq0x0bOtynjDWl8L2bkO3COMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyDG0etjDqJn32XPF85nRtDbogqROoK5PpWH39BtQmJJrmWUcxabrqKDOCeMF5b5KBM-7IXJTHQg-q3R7C-IQP8D5CKtoJ3-4qjUct0x-jLnbOVn0MW-5DMx84KtnJyUPubPnnBpjJ3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CcJ-J8XMC8Cej5P; BCLID_BFESS=10082525747833442867; BDSFRCVID_BFESS=JY0OJeC62ClZPone-3v8M3d6vhHQZzrTH6aoVp6FM5vqegToj7muEG0P8x8g0Kub6S2qogKKQgOTHRtF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tb4toK--tKt3jt-kKn7jKtI-MUCX5-CsJgKj2hcH0KLKbJ6GK5L-bt_sDtouJ-0qbJrB_JjSbfb1MRjv34j6XqK9yPD8h6vH3IrrKl5TtUJ48DnTDMRh-R-u-NJyKMniLCv9-pn4bpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuDjtBD5b0jGRabK6aKC5bL6rJabC3ox-9XU6q2bDeQNbpLRbI5C6q0xjztb--fxDxj4jPjp0vWtvJWbbvLT7johRTWqR48xFGMMonDh83b4RHelTJHCOOVp5O5hvvhb3O3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_Et5tttbCH_KvjbRj_jRTpqRQaq4tehHRqWxc9WDTm_DoTBInHhPQNqfckMxrybajqapRW-Nrq-pPKKR7jqPnv5j3rbtnBKp5i0UvH3mkjbpbGfn02OpDzMM8We-4syPRIKMRnWNrJKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFaMIIxjT_-ePDyqx5Ka43tHD7yWCkaQMJcOR59K4nnDpKA5nQ-e4vaW2De0IQKLCt-elL63MOZXb0g5n7Tbb8eBgvZ2UQkyD5ssq0x0bOtynjDWl8L2bkO3COMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTyDG0etjDqJn32XPF85nRtDbogqROoK5PpWH39BtQmJJrmWUcxabrqKDOCeMF5b5KBM-7IXJTHQg-q3R7C-IQP8D5CKtoJ3-4qjUct0x-jLnbOVn0MW-5DMx84KtnJyUPubPnnBpjJ3H8HL4nv2JcJbM5m3x6qLTKkQN3T-PKO5bRh_CcJ-J8XMC8Cej5P; delPer=0; PSINO=3; ZD_ENTRY=empty; BA_HECTOR=24052k2h80800h01dr1g318sl0r; BAIDUID_BFESS=BF3B3DCC37724BFCA25A9760F2B5812F:FG=1; tb_as_data=fd871a4bd286787472774118298b4ed929c70c8b1ff8db42c8361e72b5f7fd1c0703d949893c8c6161806ddf21d1cda085a22b6c4eeb8630acd8e18e42f0ccecf4a880e771368a6d9825ea584c8df719db265b8254724711df889a774d5526666596fa911499df1c0fd8a083869d863a; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1613801053; st_data=c309361a031754d5ddc35101f7bfa41dcea3f17f15b42f07078ebb68748fdf10980f7ce188a4eccf95396e3202bae7c689905b4101a5decbb86f0aba52778c0c18650dfe9c829e2d5c6f3393b229d6906067637766740a1edc78c0a3e4a7eeebcdd68e59adc4b05e7247387f4276c8697b60314a62eae4dc9c2e09a2b961e18f69f92538e3933c07f8da442fad4b5a5e; st_sign=8e0f8296",
    "BIDUPSID=F1A79E0CD42FEB47C44C9E2A07236422; PSTM=1610345810; BAIDUID=F1A79E0CD42FEB47A529D6DD44B930CB:FG=1; BDUSS=2U0Q3NOampUdXNVQWo1dUk4VElZd0EwNkFubjQwTlNEb3JBRVJ5Y2UzV2g5enBnRVFBQUFBJCQAAAAAAAAAAAEAAAAbepKiu-G3ybXExdbX07rcx78AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKFqE2ChahNgV; BDUSS_BFESS=2U0Q3NOampUdXNVQWo1dUk4VElZd0EwNkFubjQwTlNEb3JBRVJ5Y2UzV2g5enBnRVFBQUFBJCQAAAAAAAAAAAEAAAAbepKiu-G3ybXExdbX07rcx78AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKFqE2ChahNgV; __yjs_duid=1_f8069424467d3d28982dc56bc4c0a8201613179173897; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=33425_33441_33272_33570_33584_26350_33266; delPer=0; PSINO=3; BCLID=10268246537482939884; BDSFRCVID=CdkOJexroG3VpUnea0piM3dmiqcmDscTDYLtOwXPsp3LGJLVN4vIEG0PtD6Z1_F-2ZlgogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF35hJbXP6-hnjy3b7pKfOF5RD2Jl7EDPOVMJtfXpoy2q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJbI8DK40MHl51fbbvbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtI0hMCvnh-nhbKC3bfT2K46JHD7yWCvE3pOcOR59K4nnDpKA5Nb-56OE0mDe0n6VWnb0DJF63MOZXMLn0p6aq60D55cNaxQkyD5ssq0x0bO1-4uv3M4L2bkO3COMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTLea_8JTLDfR32Wn7a5TrMeJrnbtTMq4tehHRL5639WDTm_D_K0Db1ODON-j30MfrybMc0BpkJ-mnH-pPKKR7SKtIzbq8a0bKfMMJptnvH3mkjbpnDfn02OpjPhTJOD-4syPRIKMRnWNrJKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFabKKwD5_aejPShMntKI6J5Co20Rr2HJOoDDvChfjcy4LdjGKq3j37WRT-3CJxahC5eb6Yy-6F5lLq3-Aq54Rx2m38bxFb3q3fsJ3Kjb7GQfbQ0-7hqP-jW26aWK3otn7JOpvhbUnxyhD3QRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IqJb-qoDKbfbo5KRopMtOhq4tehHRmKPn9WDTOQJ7TtMQ2SJrN-j32MfrybMc0b4JL3T72-pbwBPbcfUnMKn05XM-pXbjwtn5A3mkjbPbgJfFa_pLzDl6SbP4syP4jKMRnWnciKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCcjqR8ZD6t5DT5P; BCLID_BFESS=10268246537482939884; BDSFRCVID_BFESS=CdkOJexroG3VpUnea0piM3dmiqcmDscTDYLtOwXPsp3LGJLVN4vIEG0PtD6Z1_F-2ZlgogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR3aQ5rtKRTffjrnhPF35hJbXP6-hnjy3b7pKfOF5RD2Jl7EDPOVMJtfXpoy2q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJbI8DK40MHl51fbbvbURvD--g3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoC0XtI0hMCvnh-nhbKC3bfT2K46JHD7yWCvE3pOcOR59K4nnDpKA5Nb-56OE0mDe0n6VWnb0DJF63MOZXMLn0p6aq60D55cNaxQkyD5ssq0x0bO1-4uv3M4L2bkO3COMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTLea_8JTLDfR32Wn7a5TrMeJrnbtTMq4tehHRL5639WDTm_D_K0Db1ODON-j30MfrybMc0BpkJ-mnH-pPKKR7SKtIzbq8a0bKfMMJptnvH3mkjbpnDfn02OpjPhTJOD-4syPRIKMRnWNrJKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCFabKKwD5_aejPShMntKI6J5Co20Rr2HJOoDDvChfjcy4LdjGKq3j37WRT-3CJxahC5eb6Yy-6F5lLq3-Aq54Rx2m38bxFb3q3fsJ3Kjb7GQfbQ0-7hqP-jW26aWK3otn7JOpvhbUnxyhD3QRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IqJb-qoDKbfbo5KRopMtOhq4tehHRmKPn9WDTOQJ7TtMQ2SJrN-j32MfrybMc0b4JL3T72-pbwBPbcfUnMKn05XM-pXbjwtn5A3mkjbPbgJfFa_pLzDl6SbP4syP4jKMRnWnciKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJzJCcjqR8ZD6t5DT5P; ab_sr=1.0.0_ZWYyZGM5MGFhZDQ1NTE0ODNjYjMwYzAyN2NhMGI1NDlkNjUwMDgyMzNkNzVlOWVjYTBkODZhMmU5ZDY4YTkwNzU0MjAyNTE1ZTQ5ZDY2Y2NkMGZlZWJjNzZlYzE3MmU2NjljMjQ3Y2ViMDRhOTdlNGI5OTBmMjBmZjU0NDI4Mzc="
]

Spd = StoredPd()


def getHeader():
    return {'User-Agent': random.choice(USER_AGENTS),
            'Cookie': random.choice(cookies)}


def getRespon(url):
    req = requests.get(url, getHeader())
    return req


def getSelector(url):
    req = requests.get(url, getHeader())
    selector = etree.HTML(req.text)
    return selector


def insertLog(Content):
    logtime = datetime.now()
    log = [Content, logtime]
    Spd.insertlog(log)


def textFilter(text):
    pattern = re.compile('<.*?>')
    listStr = pattern.findall(text)
    for i in listStr:
        text = text.replace(i, "")
    return text


def UpdatePostBar(PostBar):
    url = "https://tieba.baidu.com/f?kw=" + PostBar[0] + "&ie=utf-8"
    selector = getSelector(url)
    PostPageNum = selector.xpath('//span[@class="red_text"]/text()')
    PostBar[1] = PostPageNum[1]
    PostBar[2] = PostPageNum[2]
    Spd.insertPostBar(PostBar)


def GetPostPagesUrls():
    PostBars = Spd.GetAllPostBar()
    urls = []
    for PostBar in PostBars:
        value = RC.getData(PostBar[0])
        print(value)
        if value == "1":
            urls.append(PostBar[0])
    return urls





def PostBarRedis(PostBars, ValueConfig):
    for PostBar in PostBars:
        print("{}:{}".format(PostBar, ValueConfig))
        RC.setData(PostBar, ValueConfig)
