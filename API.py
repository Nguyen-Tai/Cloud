"""
Created on Thu Jun 25 18:40:21 2020

@author: trantrong
"""

from flask import Flask, jsonify
import json,time
import utils
import urllib3

app = Flask(__name__)
app.config["DEBUG"] = True
http = urllib3.PoolManager()


"""Trả về nhiệt độ hiện tại"""
@app.route('/',methods=['GET'])
def home():
    last_record = db.child('DHT22').order_by_child("timestamp").limit_to_last(1).get().val()
    for key,value in last_record.items():
        return value


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ hiện tại"""
@app.route('/iot',methods=['GET'])
def getNextFromCurrent():
    # start = time.time()
    req = http.request('GET', 'https://doan-cloud.firebaseio.com/DHT22.json?orderBy="timestamp"')
    data = json.loads(req.data.decode('utf-8'))
    # print('time get data',time.time() - start)
    A,B,C,LastTemperature,LastHumidity = utils.nextTemperature(data)
    next_temperature = A*LastTemperature + B*LastHumidity+ C
    return jsonify({'current':LastTemperature ,"next":round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán tiếp theo dựa trên nhiệt độ đưa vào bởi người dùng """
@app.route('/iot/<float:temperature>/<float:humidity>',methods=['GET'])
def getNextFrom(temperature,humidity):
    req = http.request('GET', 'https://doan-cloud.firebaseio.com/DHT22.json?orderBy="timestamp"')
    data = json.loads(req.data.decode('utf-8'))
    A,B,C,LastTemperature,LastHumidity = utils.nextTemperature(data)
    next_temperature = A*temperature + B*humidity+ C
    return jsonify({'next':round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán sau 60' dựa trên nhiệt độ hiện tại"""
@app.route('/iot/after60',methods=['GET'])
def getAfterFromCurrent():
    req = http.request('GET', 'https://doan-cloud.firebaseio.com/DHT22.json?orderBy="timestamp"')
    data = json.loads(req.data.decode('utf-8'))
    A,B,C,LastTemperature,LastHumidity = utils.TemperatureAfterXSeconds(data)
    next_temperature = A*LastTemperature + B*LastHumidity + C 
    return jsonify({'current':LastTemperature ,"next":round(next_temperature,2)})


"""Trả về nhiệt độ dự đoán sau 60' dựa trên nhiệt độ hiện tại"""
@app.route('/iot/after60/<float:temperature>/<float:humidity>',methods=['GET'])
def getAfterFrom(temperature,humidity):
    req = http.request('GET', 'https://doan-cloud.firebaseio.com/DHT22.json?orderBy="timestamp"')
    data = json.loads(req.data.decode('utf-8'))
    A,B,C,LastTemperature,LastHumidity = utils.TemperatureAfterXSeconds(data)
    next_temperature = A*temperature + B*humidity + C 
    return jsonify({"next":round(next_temperature,2)})

if __name__ == '__main__':
    app.run("0.0.0.0", port=80)

    