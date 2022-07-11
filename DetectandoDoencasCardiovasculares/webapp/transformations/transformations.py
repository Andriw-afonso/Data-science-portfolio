import pandas as pd
import numpy  as np
import pickle


class transformations (object):  
     
  def data_cleaning(self,df1):  
    df1=df1.copy()
    #Change types    
    df1['Cholesterol']=df1['Cholesterol'].astype(str)

    #Rewriting the variables
    niveis={'1':'medium','2':'high','3':'very_high'} 
    estado={'1':'yes','0':'no'}    

    #Cholesterol
    df1['Cholesterol']=df1['Cholesterol'].map(niveis)   
    
    return df1
  
  
  def feature_engeneering(self,df2):
    df2=df2.copy()

    #ApHiLevel
    df2['ApHiLevel']=df2['ApHi'].apply(lambda x:'level1' if x<80 else 'level2' if (x>=80)&(x<140) else 'level3')

    #ApLoLevel
    df2['ApLoLevel']=df2['ApLo'].apply(lambda x:'level1' if x<70 else 'level2' if (x>=75)&(x<100) else 'level3')
    
    #AgeLevel
    df2['AgeLevel']=df2['Age'].apply(lambda x : 'level1' if x<45 else'level2' if (x>=45)&(x<60) else 'level3')
   
    #ApHi
    aphi_mean=df2['ApHi'].mean()
    df2['ApHi']=df2['ApHi'].apply(lambda x: aphi_mean if x<100 else  aphi_mean if x>200 else x)

    #ApLo
    aplo_mean=df2['ApLo'].mean()
    df2['ApLo']=df2['ApLo'].apply(lambda x: aplo_mean if x<75 else  aplo_mean if x>100 else x)
    

    return df2  
  

  def data_preparation(self,df5):
    df5=df5.copy()
    
    #Age
    df5['Age']=np.log1p(df5['Age'])
    
    #ApLo
    df5['ApLo']=np.log1p(df5['ApLo'])
            
    #ApHi
    df5['ApHi']=np.log1p(df5['ApHi'])     
    
             
    #Cholesterol
    assortment_dict={'medium':1,'high':2,'very_high':3}
    df5['Cholesterol']=df5['Cholesterol'].map(assortment_dict)    

    #ApLoLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['ApLoLevel']=df5['ApLoLevel'].map(assortment_dict)
  
    #AgeLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['AgeLevel']=df5['AgeLevel'].map(assortment_dict)

    #ApHiLevel
    assortment_dict={'level1':1,'level2':2,'level3':3}
    df5['ApHiLevel']=df5['ApHiLevel'].map(assortment_dict)
    
    
    df5=df5[['ApHiLevel','Cholesterol','ApLo','ApHi','AgeLevel','Age']]    
    
    return df5

  
  def get_prediction(self, model, dado_original, data_transforme):

    #prediction
    pred=model.predict(data_transforme)

    #join pred into the original data
    dado_original['Predictions']=pred 

    return  dado_original.to_json(orient='records',date_format='iso')