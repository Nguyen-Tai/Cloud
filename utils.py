
import time
import config
from sklearn import linear_model
import numpy as np

minutes = 60
Timestamp = []
Temperature = []
Humidity = []
seconds = minutes*60

newTimestamp = []
newTemperature = []
newHumidity = []

TemperatureAfter = []
HumidityAfter = []

def convertNewData(data):
   for index, (key, value) in enumerate(data.items()):
      newTimestamp.append(value["timestamp"]//1000)
      newTemperature.append(value["Temperature"])
      newHumidity.append(value["Humidity"])
   del newHumidity[0]
   del newTemperature[0]
   del newTimestamp[0]

   config.keyGet = list(data.values())[-1]["timestamp"]

def saveData():
   Timestamp.extend(newTimestamp)
   Temperature.extend(newTemperature)
   Humidity.extend(newHumidity)

   newTimestamp.clear()
   newTemperature.clear()
   newHumidity.clear()

def nextTemperature(newData):
   # dt_list=[value["Temperature"] for key,value in data.items()]
   # size_train = int(len(dt_list)*0.8)
   # dt_train = dt_list[:size_train]
   # df_test  = df[size_train:]
   convertNewData(newData)

   saveData()
   dt_modelTemperatureCurrent = Temperature[:-1]  # Loại phần tử cuối
   dt_modelTemperatureNext = Temperature[1:] # Loại phần tử đầu
   dt_modelHumidityCurrent = Humidity[:-1] # Loại phần tử cuối
   # x = np.reshape(dt_modelCurrent,(-1,1))

   # slope,intercept,r,p,stderr = stats.linregress(
   # dt_modelCurrent,
   # dt_modelNext
   # ) 
   # print(intercept,slope)

   x = np.column_stack((dt_modelTemperatureCurrent,dt_modelHumidityCurrent))

   regr = linear_model.LinearRegression()
   regr.fit(x,dt_modelTemperatureNext)

   next_temperature = regr.coef_[0]*Temperature[-1]   + regr.coef_[1]* Humidity[-1] + regr.intercept_
   
   print('Intercept: \n', regr.intercept_)
   print('Coefficients: \n', regr.coef_)

   return Temperature[-1],round(next_temperature,2)

def getListValueAfter(List1,List2,ListAfter1,ListAfter2,startAt):  # Data cần xử lý , maxTimestamp
   Length = len(Timestamp)
   for index, value in enumerate(Timestamp):
      if index < startAt:
         continue
      planIndex = index +  seconds // 5
      TimeAfter = value + seconds
      if TimeAfter > Timestamp[-1]: 
         return index     # trả về index max có thể tìm được after
      ListAfter1.append(BinarySearch(index,planIndex,TimeAfter,List1,Length-1))
      ListAfter2.append(BinarySearch(index,planIndex,TimeAfter,List2,Length-1))


def BinarySearch(index,planIndex,TimeAfter,List,Length):  # Tìm value từ vị trí index đến planIndex
   start = index
   end = planIndex
   if end > Length - 1:
      end = Length - 1

   while(1):
      mid = (start + end) // 2
      if  Timestamp[mid] == TimeAfter:
         return List[mid]
      elif end - start  ==  1:
         if Timestamp[end] == TimeAfter:
            return List[end]
         if Timestamp[start] == TimeAfter:
            return List[start]
         return (List[start] + List[end]) / 2
      elif  TimeAfter < Timestamp[mid] :
         end = mid
      else:
         start = mid

def TemperatureAfterXSeconds(newData):
   convertNewData(newData)
   saveData()
   limit = getListValueAfter(Temperature,Humidity,TemperatureAfter,HumidityAfter,config.startAt) #+ len(Temperature) 
   config.startAt = limit
   dt_modelTemperatureCurrent = Temperature[:limit]
   dt_temperatureAfter = TemperatureAfter
   dt_modelHumidityCurrent = Humidity[:limit]

   # print(len(dt_temperatureAfter),"   ",len(dt_humidityAfter))
   # regr.fit([np.reshape(dt_temperatureAfter, (-1, 2)),np.reshape(dt_humidityAfter, (-1, 2))], dt_temperature)

   # print('Intercept: \n', regr.intercept_)
   # print('Coefficients: \n', regr.coef_)

   # np.reshape(A, (-1, 2))

   x = np.column_stack((dt_modelTemperatureCurrent,dt_modelHumidityCurrent))

   regr = linear_model.LinearRegression()
   regr.fit(x,dt_temperatureAfter)

   next_temperature = regr.coef_[0]*Temperature[-1]   + regr.coef_[1]* Humidity[-1] + regr.intercept_
   
   print('Intercept: \n', regr.intercept_)
   print('Coefficients: \n', regr.coef_)

   return Temperature[-1],round(next_temperature,2)

   # slope,intercept,r,p,stderr = stats.linregress(
   # dt_temperature,
   # dt_temperatureAfter
   # ) 
  # y= Ãx+B
  #  print(slope)#A
  #  print(intercept)#B
  #  print(stderr)#sai số 
   # return round(slope,3),round(intercept,3),Temperature[-1]