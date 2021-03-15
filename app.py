import threading
import sys
import time

from source.DataAnalysis.AnalsisByPostBar import AnalsisPostBar
from source.Tool import Common

sys.path.append('./')
from source.Tool.RedisPro import RedisControl
from source.Tool.StoredProcedure import StoredPd
import json
from urllib.parse import unquote
from source.Starter.Start import StartSpider, StartTrainModel
from flask import Flask, request
from flask_cors import CORS
import Config
RC = RedisControl()
stp = StoredPd()

analsis = AnalsisPostBar()


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

        self.begin_job()

    def begin_job(self):
        def initConfig():
            PostBars = stp.GetAllPostBar()
            for PostBar_ in PostBars:
                RC.setData(PostBar_[0], "0")
            RC.setData("SpiderFlag", "0")
            RC.setData("TrainModelFlag", "0")
            print("Config inited")

        threading.Thread(target=initConfig).start()


app = FlaskApp(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/PostBar')
def PostBar():
    PostBarID = request.values.get("PostBar")

    url = "https://tieba.baidu.com/f?kw={}".format(PostBarID)
    # request.values.get(" PostBar")
    re = Common.getRespon(url)
    if url == re.url.split("&", 2)[0]:
        bo = stp.insertPostBar(PostBarID)
        if bo:
            return json.dumps({"code": 1})
        else:
            return json.dumps({"code": 2})
    else:
        return json.dumps({"code": 0})


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/PostBarList')
def PostBarList():
    PostBars = stp.GetAllPostBar()
    data = {"PostBars": []}
    for PostBar in PostBars:
        row = {
            "PostBarID": unquote(PostBar[0]),
        }
        data["PostBars"].append(row)
    return json.dumps(data)


@app.route("/GetFlag")
def GetFlag():
    Flag = request.values.get("Config")
    print(Flag)
    value = RC.getData(Flag)
    print(value)
    return json.dumps({"ValueConfig": value})


@app.route("/Start", methods=['POST', 'GET'])
def Start():
    data = {}
    if request.method == 'GET':
        Name = request.values.get("Name")
    else:
        data = json.loads(request.get_data())
        Name = data["Name"]

    if Name == "Spider":
        PostBarIDs = data["PostBarIDs"]
        Common.PostBarRedis(PostBarIDs, "1")
        RC.setData("SpiderFlag", "1")
        Common.GetPostPagesUrls()
        StartSpider()

        RC.setData("SpiderFlag", "0")
        Common.PostBarRedis(PostBarIDs, "0")
        return json.dumps({"Code": 1})
    elif Name == "TrainModel":
        RC.setData("TrainModelFlag", "1")
        StartTrainModel()
        RC.setData("TrainModelFlag", "0")
        return json.dumps({"Code": 1})


@app.route("/test")
def test():
    flags = 1


# @app.route("/PostBarIDs")
# def PostBarIDs():
#     data = []
#     PostBarID_data = stp.GetAllPostBar()
#     for PostBarID in PostBarID_data:
#         value = RC.getData(PostBarID[0])
#         data.append({"PostBarID": unquote(PostBarID[0]), "flag": value})
#     return json.dumps({"PostBarIDs": data})


@app.route("/UserLevelChart")
def UserLevelChart():
    PostBarID = request.values.get("PostBarID")
    rows = analsis.AnalsisUserByLevel(PostBarID)
    columns = ["UserLevel", "Num"]
    return json.dumps({"columns": columns, "rows": rows})


@app.route("/PosOrNegChart")
def PosOrNegChart():
    PostBarID = request.values.get("PostBarID")
    print(PostBarID)
    rows = analsis.AnalsisPosOrNeg(PostBarID)
    columns = ["PosOrNeg", "Num"]
    return json.dumps({"columns": columns, "rows": rows})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
