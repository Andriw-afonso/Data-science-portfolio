from flask                           import Flask,request,Response
from transformations.transformations import transformations
import os
import pickle
import pandas              as pd


#Loading model
model=pickle.load(open('model/model_xgb.pkl','rb'))

#Initialize API
app=Flask(__name__)

@app.route('/oi',methods=['POST'])
def diagnostico_predict():
  test_json=request.get_json()

  if test_json:
    if isinstance (test_json,dict):
      numero_da_loja=pd.DataFrame(test_json,index=[0])

    else:
      numero_da_loja=pd.DataFrame(test_json,columns=test_json[0].keys())

    #numero da loja
    loja=numero_da_loja['numero_da_loja'][0]
    
    #Isntantiate transformations
    pipeline=transformations() 

    #dataset test 
    test_raw=pipeline.dataset (loja) 
    if test_raw.shape[0] != 0:    

      #data cleaning
      df1=pipeline.data_cleaning(test_raw)  

      #feature engeneering
      df2=pipeline.feature_engeneering(df1)

      #data preparation
      df3=pipeline.data_preparation(df2)

      #predict
      df4=pipeline.get_prediction(model,test_raw,df3) 

      #prediction_calculator
      df5=pipeline.prediction_calculator(df4)   
        
      return df5

    else:
      df={'Predictions':['Nao existe essa loja !']}
      df=pd.DataFrame(data=df,columns=['Predictions'])
      
      return  df.to_json(orient='records',date_format='iso')    

  else:
    return Response('{}',status=200,mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)