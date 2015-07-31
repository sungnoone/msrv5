import sys, os
from flask import Flask, Request, Response, redirect, url_for, jsonify, request
from flask_cors import *
from pymongo import *
from werkzeug import utils
import json
import bson.json_util
import datetime
import conf
import simplejson
import csv

##custom function class


APP_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_PATH_LOG = APP_PATH+"/msrv5.log"
FILE_PATH_JSON_DATA = APP_PATH+"/data1.json"


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


##=============================== test for connect =========================================


@app.route('/srv/')
@cross_origin()
def hello_world():
    return 'Hello World!'


##=============================== test for auto save =========================================


##Receiving post update from jqgrid client
@app.route("/srv/auto/save/",methods=["GET","POST"])
@cross_origin()
def srv_auto_save():
    log = open(FILE_PATH_LOG, 'a+')
    log.write(">>>...MODULE:srv_auto_save >>>"+str(datetime.datetime.now())+"\r\n")
    try:
        request_data = request.form
        log.write(str(request_data["id"])+"\r\n")
        ##read json file content
        json_file = open(FILE_PATH_JSON_DATA,"r")
        data = json_file.read()
        json_data = json.loads(data,encoding="utf-8")
        for item in json_data["rows"]:
            if item["id"]==request_data["id"]:
                item["full_name"]=request_data["full_name"]
                item["branch"]=request_data["branch"]
                item["department"]=request_data["department"]
        log.write(str(json_data["rows"])+"\r\n")
        json_file.close()
        ##write back
        json_file = open(FILE_PATH_JSON_DATA,"w")
        log.write(str(str(json_data))+"\r\n")
        json.dump(json_data,json_file)
        #json_file.write(str(json_data))
        json_file.close()
    except Exception as ex:
        log.write("Request fail: "+str(ex)+"\r\n")
        log.close()
        json_file.close()
    return ""

## for jqgrid query
@app.route("/srv/get/all/",methods=["GET"])
@cross_origin()
def srv_get_all():
    log = open(FILE_PATH_LOG, 'a+')
    log.write(">>>...MODULE:srv_get_all >>>"+str(datetime.datetime.now())+"\r\n")
    try:
        f = open(FILE_PATH_JSON_DATA,"r")
        data = f.read()
        log.write(str(data)+"\r\n")

    except Exception as ex:
        log.write("Read json file fail: "+str(ex)+"\r\n")
        log.close()

    log.close()
    return str(data)


##========================================================================


if __name__ == '__main__':
    app.run(host=conf.HOST_IP, port=conf.HOST_PORT)
