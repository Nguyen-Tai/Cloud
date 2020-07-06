
import time
from sklearn import linear_model
import numpy as np

minutes = 60
seconds = minutes*60

def nextTemperature(data):
   Timestamp=[]
   Temperature=[]
   Humidity=[]
   # start_time = time.time()
   for key, value in data.items():
      Timestamp.append(value["timestamp"]//1000)
      Temperature.append(value["Temperature"])
      Humidity.append(value["Humidity"])
   # print("--- %s seconds convert data ---" % (time.time() - start_time))
   dt_modelTemperatureCurrent = Temperature[:-1]  # Loại phần tử cuối
   dt_modelTemperatureNext = Temperature[1:] # Loại phần tử đầu
   dt_modelHumidityCurrent = Humidity[:-1] # Loại phần tử cuối

   x = np.column_stack((dt_modelTemperatureCurrent,dt_modelHumidityCurrent))

   regr = linear_model.LinearRegression()
   regr.fit(x,dt_modelTemperatureNext)

   return regr.coef_[0], regr.coef_[1], regr.intercept_,Temperature[-1],Humidity[-1]


def getListValueAfter(Timestamp,Temperature,TemperatureAfter):  # Data cần xử lý , maxTimestamp
   Length = len(Timestamp)
   for index, value in enumerate(Timestamp):
      planIndex = index +  seconds // 5
      TimeAfter = value + seconds
      if TimeAfter > Timestamp[-1]: 
         return index     # trả về index max có thể tìm được after
      TemperatureAfter.append(BinarySearch(index,planIndex,TimeAfter,Timestamp,Temperature,Length-1))


def BinarySearch(index,planIndex,TimeAfter,Timestamp,Temperature,Length):  # Tìm value từ vị trí index đến planIndex
   start = index
   end = planIndex
   if end > Length - 1:
      end = Length - 1

   while(1):
      mid = (start + end) // 2
      if  Timestamp[mid] == TimeAfter:
         return Temperature[mid]
      elif end - start  ==  1:
         if Timestamp[end] == TimeAfter:
            return Temperature[end]
         if Timestamp[start] == TimeAfter:
            return Temperature[start]
         return (Temperature[start] + Temperature[end]) / 2
      elif  TimeAfter < Timestamp[mid]:
         end = mid
      else:
         start = mid

def TemperatureAfterXSeconds(data):
   Timestamp=[]
   Temperature=[]
   Humidity=[]
   start_time = time.time()
   for key, value in data.items():
      Timestamp.append(value["timestamp"]//1000)
      Temperature.append(value["Temperature"])
      Humidity.append(value["Humidity"])

   TemperatureAfter=[]

   limit = getListValueAfter(Timestamp,Temperature,TemperatureAfter)
   dt_modelTemperatureCurrent = Temperature[:limit]
   dt_modelHumidityCurrent = Humidity[:limit]
   dt_temperatureAfter = TemperatureAfter

   x = np.column_stack((dt_modelTemperatureCurrent,dt_modelHumidityCurrent))

   regr = linear_model.LinearRegression()
   regr.fit(x,dt_temperatureAfter)

   return regr.coef_[0], regr.coef_[1], regr.intercept_,Temperature[-1],Humidity[-1]
