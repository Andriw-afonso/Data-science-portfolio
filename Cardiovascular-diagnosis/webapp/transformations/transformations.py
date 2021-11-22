import pandas as pd
import numpy  as np
import pickle


class transformations (object):  
  def __init__(self):
    
    self.Age=                      pickle.load(open('parameters/Age_scaler.pkl','rb'))    
    self.ApHi=                     pickle.load(open('parameters/ApHi_scaler.pkl','rb'))
    self.ApLo=                     pickle.load(open('parameters/ApLo_scaler.pkl','rb'))    
    self.Height=                   pickle.load(open('parameters/Height_scaler.pkl','rb'))
    self.Imc=                      pickle.load(open('parameters/Imc_scaler.pkl','rb'))    
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
  
  
  def feature_engeneering(self,df2):

    #ApHiLevel
    df2['ApHiLevel']=df2['ApHi'].apply(lambda x:'level1' if x<80 else 'level2' if (x>=80)&(x<140) else 'level3')

    #ApLoLevel
    df2['ApLoLevel']=df2['ApLo'].apply(lambda x:'level1' if x<70 else 'level2' if (x>=75)&(x<100) else 'level3')

    #WeightLevel
    df2['WeightLevel']=df2['Weight'].apply(lambda x: 'level1' if x<50 else 'level2'if (x>=50)&(x<=80) else 'level3')

    #AgeLevel
    df2['AgeLevel']=df2['Age'].apply(lambda x : 'level1' if x<45 else'level2' if (x>=45)&(x<60) else 'level3')

    #Imc
    df2['Imc']=df2['Weight']/(df2['Height']**2)

    #ApHi
    aphi_mean=df2['ApHi'].mean()
    df2['ApHi']=df2['ApHi'].apply(lambda x: aphi_mean if x<100 else  aphi_mean if x>200 else x)

    #ApHi
    aplo_mean=df2['ApLo'].mean()
    df2['ApLo']=df2['ApLo'].apply(lambda x: aplo_mean if x<75 else  aplo_mean if x>100 else x)

    #Weight
    weight_mean=df2['Weight'].mean()
    df2['Weight']=df2['Weight'].apply(lambda x: weight_mean if x<40 else  x)

    #Height
    height_mean=df2['Height'].mean()
    df2['Height']=df2['Height'].apply(lambda x: height_mean if x<1.25  else x)
    #df2=df2.reset_index()

    return df2  
  

  def data_preparation(self,df5):
    
    #Age
    df5['Age']=self.Age.fit_transform(df5[['Age']].values)
    
    #ApLo
    df5['ApLo']=self.ApLo.fit_transform(df5[['ApLo']].values)
       
    #Height
    df5['Height']=self.Height.fit_transform(df5[['Height']].values)
    
    #Weight
    df5['Weight']=self.Weight.fit_transform(df5[['Weight']].values)
    
    #ApHi
    df5['ApHi']=self.ApHi.fit_transform(df5[['ApHi']].values)
    
    #Imc
    df5['Imc']=self.Imc.fit_transform(df5[['Imc']].values) 
    
    #Gender
    df5=pd.get_dummies(df5,prefix=['Gender'],columns=['Gender'])

    #Smoke
    df5=pd.get_dummies(df5,prefix=['Smoke'],columns=['Smoke'])

    #Alco
    df5=pd.get_dummies(df5,prefix=['Alco'],columns=['Alco'])

    #Active
    df5=pd.get_dummies(df5,prefix=['Active'],columns=['Active'])   
        
    #Cholesterol
    assortment_dict={'medium':1,'high':2,'very_high':3}
    df5['Cholesterol']=df5['Cholesterol'].map(assortment_dict)

    #Gluc
    assortment_dict={'medium':1,'high':2,'very_high':3}
    df5['Gluc']=df5['Gluc'].map(assortment_dict)

    #ApLoLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['ApLoLevel']=df5['ApLoLevel'].map(assortment_dict)

    #WeightLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['WeightLevel']=df5['WeightLevel'].map(assortment_dict)

    #AgeLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['AgeLevel']=df5['AgeLevel'].map(assortment_dict)

    #ApHiLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['ApHiLevel']=df5['ApHiLevel'].map(assortment_dict)
    

    df5=df5[['ApHiLevel','Cholesterol','ApLo','ApHi','Smoke_1','AgeLevel','Age']]
    columns={'ApHiLevel':'ApHiLevel','Cholesterol':'Cholesterol',
             'ApLo':'ApLo','ApHi':'ApHi','Smoke_1':'Smoke_yes',
             'AgeLevel':'AgeLevel','Age':'Age'}
    df5=df5.rename(columns=columns)
    return df5

  
  def get_prediction(self, model, dado_original, data_transforme):

    #prediction
    pred=model.predict(data_transforme)

    #join pred into the original data
    dado_original['Predictions']=pred 

    return dado_original.to_json(orient='records',date_format='iso')