import pandas as pd
import numpy  as np
import pickle


class transformations (object):  
  def __init__(self):
    self.Active=                   pickle.load(open('parameters/Active_scaler.pkl','rb'))
    self.Age=                      pickle.load(open('parameters/Age_scaler.pkl','rb'))
    self.Alco=                     pickle.load(open('parameters/Alco_scaler.pkl','rb'))
    self.ApHi=                     pickle.load(open('parameters/ApHi_scaler.pkl','rb'))
    self.ApLo=                     pickle.load(open('parameters/ApLo_scaler.pkl','rb'))
    self.Gender=                   pickle.load(open('parameters/Gender_scaler.pkl','rb'))
    self.Height=                   pickle.load(open('parameters/Height_scaler.pkl','rb'))
    self.Imc=                      pickle.load(open('parameters/Imc_scaler.pkl','rb'))
    self.Smoke=                    pickle.load(open('parameters/Smoke_scaler.pkl','rb'))
    self.Weight=                   pickle.load(open('parameters/Weight_scaler.pkl','rb'))
     


  def data_cleaning(self,data):
    

    columns={  'id':'Id','age':'Age','gender':'Gender','height':'Height',
               'weight':'Weight','ap_hi':'ApHi','ap_lo':'ApLo',
               'cholesterol':'Cholesterol','gluc':'Gluc','smoke':'Smoke',
               'alco':'Alco','active':'Active','cardio':'Cardio'}

    data=data.rename(columns=columns)  

    #Change types
    aux=['Active','Cholesterol']
    data[aux]=data[aux].astype(str)

    #Rewriting the variables
    niveis={'1':'medium','2':'high','3':'very_high'} 
    estado={'1':'yes','0':'no'}    

    #Cholesterol
    data['Cholesterol']=data['Cholesterol'].map(niveis)   
    
    return data
  
  
  def feature_engeneering(self,data):

    #Age
    data['Age']=data['Age']/365 
    #Imc
    data['Imc']=data['Weight']/(data['Height']**2)

    return data  
  

  def data_preparation(self,data):
    
    #Age
    data['Age']=self.Age.fit_transform(data[['Age']].values)
    
    #ApLo
    data['ApLo']=self.ApLo.fit_transform(data[['ApLo']].values)
    
    #Height
    data['Height']=self.Height.fit_transform(data[['Height']].values)

    #Weight
    data['Weight']=self.Weight.fit_transform(data[['Weight']].values)

    #ApHi
    data['ApHi']=self.ApHi.fit_transform(data[['ApHi']].values)
    
    #Imc
    data['Imc']=self.Imc.fit_transform(data[['Imc']].values)      

    #Gender
    data['Gender']=self.Gender.fit_transform(data['Gender'])
    
    #Smoke
    data['Smoke']=self.Smoke.fit_transform(data['Smoke'])
    
    #Alco
    data['Alco']=self.Alco.fit_transform(data['Alco'])
    
    #Active
    data['Active']=self.Active.fit_transform(data['Active'])      

    #Cholesterol
    r=0.33
    assortment_dict={'medium':1*r,'high':2*r,'very_high':3*r}
    data['Cholesterol']=data['Cholesterol'].map(assortment_dict)

    #Gluc
    r=0.33
    assortment_dict={'medium':1*r,'high':2*r,'very_high':3*r}
    data['Gluc']=data['Gluc'].map(assortment_dict)
    data=data[['Age', 'Active', 'ApHi', 'Cholesterol']]
    return data
  
  def get_prediction(self, model, dado_original, data_transforme):

    #prediction
    pred=model.predict(data_transforme)

    #join pred into the original data
    dado_original['Predictions']=pred 

    return dado_original.to_json(orient='records',date_format='iso')