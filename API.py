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

    A,B,current_temperature = utils.nextTemperature(data)
    next_temp = round(A*current_temperature + B,1)
    return jsonify({'current':current_temperature ,"next":next_temp})


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ đưa vào bởi người dùng """
@app.route('/iot/<float:temperature>',methods=['GET'])
def getNext(temperature):

    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print('ít',len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print("all")
   
    A,B,current_temperature = utils.nextTemperature(data)
    next_temp = round(A*temperature + B,1)
    return jsonify({'next':next_temp})


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ hiện tại"""
@app.route('/iot/after60',methods=['GET'])
def getAfter():

    print(config.keyGet)
    if config.keyGet != None:
        data = db.child('DHT22').order_by_child("timestamp").start_at(config.keyGet).get().val()
        print(len(data))
    else:
        data = db.child('DHT22').order_by_child("timestamp").get().val()
        print(len(data))
    A,B,current_temperature = utils.TemperatureAfterXSeconds(data)
    # A=B=1
    next_temp = round(A*current_temperature + B,1)
    return jsonify({'current':current_temperature ,"next":next_temp})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
