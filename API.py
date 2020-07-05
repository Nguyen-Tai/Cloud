"""
Created on Thu Jun 25 18:40:21 2020

@author: trantrong
"""

from flask import Flask, jsonify
import pyrebase
import json
from datetime import datetime
import utils
import config
configFirebase = {
  "apiKey": "AIzaSyCLNFdZ4UM9BH2-3i42ehIgU90gra0AFN0",
  "authDomain": "doan-cloud.firebaseapp.com",
  "databaseURL": "https://doan-cloud.firebaseio.com",
  "storageBucket": "doan-cloud.appspot.com"
}

firebase = pyrebase.initialize_app(configFirebase)
db = firebase.database()

app = Flask(__name__)
app.config["DEBUG"] = True


"""Trả về nhiệt độ hiện tại"""
@app.route('/',methods=['GET'])
def home():
    last_record = db.child('DHT22').order_by_child("timestamp").limit_to_last(1).get().val()
    for key,value in last_record.items():
        return value


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ hiện tại"""
@app.route('/iot',methods=['GET'])
def getNextFromCurrent():
    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print(len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print(len(data))
    A,B,C,LastTemperature,LastHumidity = utils.nextTemperature(data)
    next_temperature = A*LastTemperature + B*LastHumidity+ C
    return jsonify({'current':LastTemperature ,"next":round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ đưa vào bởi người dùng """
@app.route('/iot/<float:temperature>/<float:humidity>',methods=['GET'])
def getNextFrom(temperature,humidity):
    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print(len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print(len(data))
   
    A,B,C,LastTemperature,LastHumidity = utils.nextTemperature(data)
    next_temperature = A*temperature + B*humidity+ C
    return jsonify({'next':round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán sau 60' dựa trên nhiệt độ hiện tại"""
@app.route('/iot/after60',methods=['GET'])
def getAfterFromCurrent():

    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print(len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print(len(data))
    A,B,C,LastTemperature,LastHumidity = utils.TemperatureAfterXSeconds(data)

    next_temperature = A*LastTemperature + B*LastHumidity + C 

    return jsonify({'current':LastTemperature ,"next":round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán sau 60' dựa trên nhiệt độ hiện tại"""
@app.route('/iot/after60/<float:temperature>/<float:humidity>',methods=['GET'])
def getAfterFrom(temperature,humidity):

    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print(len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print(len(data))
    A,B,C,LastTemperature,LastHumidity = utils.TemperatureAfterXSeconds(data)

    next_temperature = A*temperature + B*humidity + C 
    # A=B=1
    return jsonify({"next":round(next_temperature,2)})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)