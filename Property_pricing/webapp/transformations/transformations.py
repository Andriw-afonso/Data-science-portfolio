import pandas as pd
import numpy  as np
import pickle
import inflection


class transformations (object):  
  def __init__(self):
    self.SqftAbove=                     pickle.load(open('parameters/SqftAbove_scaler.pkl','rb'))
    self.YrBuilt=                       pickle.load(open('parameters/YrBuilt_scaler.pkl','rb'))  
    self.SqftLiving=                    pickle.load(open('parameters/SqftLiving_scaler.pkl','rb'))   
    self.TimeOfExistence=               pickle.load(open('parameters/TimeOfExistence_scaler.pkl','rb'))  
    self.SqftLot=                       pickle.load(open('parameters/SqftLot_scaler.pkl','rb'))  
    self.LivingRoomIncrease=            pickle.load(open('parameters/LivingRoomIncrease_scaler.pkl','rb'))
    self.IncreaseInLotArea=             pickle.load(open('parameters/IncreaseInLotArea_scaler.pkl','rb'))    
    self.Lat=                           pickle.load(open('parameters/Lat_scaler.pkl','rb'))   
    self.Long=                          pickle.load(open('parameters/Long_scaler.pkl','rb')) 
    self.Zipcode=                       pickle.load(open('parameters/Zipcode_scaler.pkl','rb')) 
    self.SqftLiving15=                  pickle.load(open('parameters/SqftLiving15_scaler.pkl','rb')) 
    self.SqftLot15=                     pickle.load(open('parameters/SqftLot15_scaler.pkl','rb'))          
    
  
   

  def data_cleaning(self,data):    
    #Rename  
    columns={  'id':'Id', 'date':'Date', 'bedrooms':'Bedrooms',
               'bathrooms':'Bathrooms', 'sqft_living':'SqftLiving',
               'sqft_lot':'SqftLot','floors':'Floors','waterfront':'Waterfront',
               'view':'View', 'condition':'Condition', 'grade':'Grade',
               'sqft_above':'SqftAbove','sqft_basement':'SqftBasement',
               'yr_built':'YrBuilt', 'yr_renovated':'YrRenovated',
               'zipcode':'Zipcode', 'lat':'Lat', 'long':'Long',
               'sqft_living15':'SqftLiving15', 'sqft_lot15':'SqftLot15'}
    data=data.rename(columns=columns)

    #Change types
    serie=['Condition','Grade','Id','Waterfront']
    data[serie]=data[serie].astype(str)

    data['Date']=                  pd.to_datetime(data['Date'])
    return data
      


  def feature_engeneering(self,data):
    #turning square feet into square meters
    aux=['SqftLiving','SqftLot','SqftAbove','SqftBasement','SqftLiving15','SqftLot15']
    data[aux]=data[aux]*0.0929

    #YearOfAssessment
    data['YearOfAssessment']=data['Date'].dt.year

    #EvaluationMonth
    data['EvaluationMonth']=data['Date'].dt.month

    #TimeOfExistence'
    data['TimeOfExistence']=data['YearOfAssessment']-data['YrBuilt']

    #RetirementTime
    data['RetirementTime']=data['YearOfAssessment']-data['YrRenovated']

    #Grade
    data['Grade']=data['Grade'].apply(lambda x:
                                    
                                    '1' if x=='1'  else '1' if x=='2'  else '1' if x=='3' else '1' if x=='4' else
                                    '2' if x=='5'  else '2' if x=='6'  else '2' if x=='7' else
                                    '3' if x=='8'  else '3' if x=='9'  else '3' if x=='10'else
                                    '4' if x=='11' else '4' if x=='12' else '4' if x=='13'else

                                    'no_group')

    #Waterfront
    data['Waterfront']=data['Waterfront'].apply(lambda x:'yes' if x=='1'  else 'no')  
           
    #LivingRoomIncrease
    data['LivingRoomIncrease']=data['SqftLiving15']-data['SqftLiving']

    #IncreaseInLotArea
    data['IncreaseInLotArea']=data['SqftLot15']-data['SqftLot']   
    

    return data
      

  def data_preparation(self,data):  
       
    #SqftLiving
    data['SqftLiving']=self.SqftLiving.fit_transform(data[['SqftLiving']].values)      

    #SqftAbove
    data['SqftAbove']=self.SqftAbove.fit_transform(data[['SqftAbove']].values) 

    #TimeOfExistence
    data['TimeOfExistence']=self.TimeOfExistence.fit_transform(data[['TimeOfExistence']].values)    

    #SqftLot
    data['SqftLot']=self.SqftLot.fit_transform(data[['SqftLot']].values)

    #LivingRoomIncrease
    data['LivingRoomIncrease']=self.LivingRoomIncrease.fit_transform(data[['LivingRoomIncrease']].values)

    #IncreaseInLotArea
    data['IncreaseInLotArea']=self.IncreaseInLotArea.fit_transform(data[['IncreaseInLotArea']].values)  

    #Lat
    data['Lat']=self.Lat.fit_transform(data[['Lat']].values)  

    #Long
    data['Long']=self.Long.fit_transform(data[['Long']].values) 

    #YrBuilt
    data['YrBuilt']=self.YrBuilt.fit_transform(data[['YrBuilt']].values) 
     
    #Zipcode
    data['Zipcode']=self.Zipcode.fit_transform(data['Zipcode'])    
    
    #Grade
    a=0.06
    assortment_dict={'1':1*a,'2':2*a,'3':3*a,'4':4*a,'5':5*a,'6':6*a,'7':7*a,'8':8*a,'9':9*a,'10':10*a,'11':11*a,'12':12*a,'13':13*a}
    data['Grade']=data['Grade'].map(assortment_dict) 
        

    return data[[ 'SqftLiving','SqftLot', 'Grade','SqftAbove',
                  'YrBuilt','Zipcode','Lat','Long','SqftLiving15',
                  'SqftLot15','TimeOfExistence','LivingRoomIncrease',
                  'IncreaseInLotArea']]


  def get_prediction(self, model, dado_original, data_transforme):

    #prediction
    pred=model.predict(data_transforme)

    #join pred into the original data
    dado_original['Predictions']=np.expm1(pred)    

    return dado_original.to_json(orient='records',date_format='iso')