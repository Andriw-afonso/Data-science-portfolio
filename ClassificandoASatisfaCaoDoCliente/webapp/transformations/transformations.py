import pandas as pd
import numpy  as np
import pickle


class transformations (object):  
  def __init__(self):
    self.Age=               pickle.load(open('parameters/Age_scaler.pkl','rb'))  
    self.Class=             pickle.load(open('parameters/Class_scaler.pkl','rb'))   
    self.CustomerType=      pickle.load(open('parameters/CustomerType_scaler.pkl','rb'))   
    self.FlightDistance=    pickle.load(open('parameters/FlightDistance_scaler.pkl','rb'))   
    self.InflightService=   pickle.load(open('parameters/In-flightService_scaler.pkl','rb'))   
    self.TypeOfTravel=      pickle.load(open('parameters/TypeOfTravel_scaler.pkl','rb'))   
           


  def data_cleaning(self,data): 

    columns=columns={  'Unnamed: 0'                       :'Unnamed: 0',
                       'id'                               :'Id',
                       'Gender'                           :'Gender',
                       'Customer Type'                    :'CustomerType',
                       'Age'                              :'Age',
                       'Type of Travel'                   :'TypeOfTravel',
                       'Class'                            :'Class',
                       'Flight Distance'                  :'FlightDistance',
                       'Inflight wifi service'            :'InflightWifiService',
                       'Departure/Arrival time convenient':'Departure/ArrivalTimeConvenient',
                       'Ease of Online booking'           :'EaseOfOnlineBooking',
                       'Gate location'                    :'GateLocation',
                       'Food and drink'                   :'FoodAndDrink',
                       'Online boarding'                  :'OnlineBoarding',
                       'Seat comfort'                     :'SeatComfort',
                       'Inflight entertainment'           :'InflightEntertainment',
                       'On-board service'                 :'On-boardService',
                       'Leg room service'                 :'LegRoomService',
                       'Baggage handling'                 :'BaggageHandling',
                       'Checkin service'                  :'CheckinService',
                       'Inflight service'                 :'InflightService',
                       'Cleanliness'                      :'Cleanliness',
                       'Departure Delay in Minutes'       :'DepartureDelayInMinutes',
                       'Arrival Delay in Minutes'         :'ArrivalDelayInMinutes'}
    data=data.rename(columns=columns)

    #to str
    aux=[ 'InflightWifiService','Departure/ArrivalTimeConvenient',
          'EaseOfOnlineBooking','GateLocation','Cleanliness',
          'FoodAndDrink','OnlineBoarding','SeatComfort',
          'InflightEntertainment','On-boardService',
          'LegRoomService','BaggageHandling',
          'CheckinService','InflightService']
    data[aux]=data[aux].astype(str)

    #to float
    data['DepartureDelayInMinutes']=data['DepartureDelayInMinutes'].astype(float)     

    return data
  
  
  def feature_engeneering(self,data):  

    #TotalScore
    lista=['InflightWifiService','Departure/ArrivalTimeConvenient','EaseOfOnlineBooking',
           'GateLocation','FoodAndDrink','OnlineBoarding','SeatComfort',
           'InflightEntertainment','On-boardService','LegRoomService',
           'BaggageHandling','CheckinService','InflightService','Cleanliness']

    data[lista]=data[lista].astype(int)
    data['TotalScore']=data[lista].sum(axis=1)

    #In-flightService
    data['In-flightService']=round((data['On-boardService']+data['InflightService'])/2,2)
    data[lista]=data[lista].astype(str)

    #SumOfDelays
    data['SumOfDelays']=data['DepartureDelayInMinutes']+data['ArrivalDelayInMinutes']  

    data=data.drop(['Unnamed: 0'],axis=1)

    return data  
  

  def data_preparation(self,data):  
    
    #MinMaxScaler
    #Age
    data['Age']=self.Age.fit_transform(data[['Age']].values)    

    #FlightDistance
    data['FlightDistance']=self.FlightDistance.fit_transform(data[['FlightDistance']].values)  

    #In-flightService
    data['In-flightService']=self.InflightService.fit_transform(data[['In-flightService']].values)


    #Ordinal Encoding
    r=0.166
    assortment_dict={'0':0*r,'1':1*r,'2':2*r,'3':3*r,'4':4*r,'5':5*r}

    #InflightWifiService   
    data['InflightWifiService']=data['InflightWifiService'].map(assortment_dict)

    #Departure/ArrivalTimeConvenient 
    data['Departure/ArrivalTimeConvenient']=data['Departure/ArrivalTimeConvenient'].map(assortment_dict) 

    #EaseOfOnlineBooking  
    data['EaseOfOnlineBooking']=data['EaseOfOnlineBooking'].map(assortment_dict) 

    #GateLocation
    data['GateLocation']=data['GateLocation'].map(assortment_dict)

    #FoodAndDrink  
    data['FoodAndDrink']=data['FoodAndDrink'].map(assortment_dict)

    #OnlineBoarding 
    data['OnlineBoarding']=data['OnlineBoarding'].map(assortment_dict) 

    #SeatComfort  
    data['SeatComfort']=data['SeatComfort'].map(assortment_dict)

    #InflightEntertainment
    data['InflightEntertainment']=data['InflightEntertainment'].map(assortment_dict) 

    #On-boardService
    data['On-boardService']=data['On-boardService'].map(assortment_dict)

    #LegRoomService
    data['LegRoomService']=data['LegRoomService'].map(assortment_dict)  

    #BaggageHandling 
    data['BaggageHandling']=data['BaggageHandling'].map(assortment_dict) 

    #CheckinService 
    data['CheckinService']=data['CheckinService'].map(assortment_dict) 

    #InflightService 
    data['InflightService']=data['InflightService'].map(assortment_dict)  

    #Cleanliness  
    data['Cleanliness']=data['Cleanliness'].map(assortment_dict) 

    #labelEncoder
    #CustomerType
    data['CustomerType']=self.CustomerType.fit_transform(data['CustomerType'])    

    #TypeOfTravel
    data['TypeOfTravel']=self.TypeOfTravel.fit_transform(data['TypeOfTravel'])    

    #Class
    data['Class']=self.Class.fit_transform(data['Class'])  
      
   
    return data[[     'CustomerType', 'Age', 'TypeOfTravel', 'Class', 'FlightDistance',
                    'InflightWifiService', 'GateLocation', 'OnlineBoarding', 'SeatComfort',
                    'InflightEntertainment', 'BaggageHandling', 'CheckinService',
                    'InflightService', 'Cleanliness', 'In-flightService']]
  


  def get_prediction( self,model, dado_original, data_transforme):

    #prediction
    pred=model.predict(data_transforme)

    #join pred into the original data
    dado_original['Predictions']=pred 

    return dado_original.to_json(orient='records',date_format='iso')