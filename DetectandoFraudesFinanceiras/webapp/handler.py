from flask                         import Flask,request,Response
from transformacoes.transformacoes import transformacoes
from transformacoes.transformacoes import get_prediction
import os
import pickle
import pandas              as pd


#Loading model
model=pickle.load(open('model/model_rfc_train.pkl','rb'))

#Initialize API
app=Flask(__name__)

@app.route('/oi',methods=['POST'])
def diagnostico_predict():
  test_json=request.get_json()

  if test_json:
    if isinstance (test_json,dict):
      test_raw=pd.DataFrame(test_json,index=[0])

    else:
      test_raw=pd.DataFrame(test_json,columns=test_json[0].keys())
    
    #transformacoes    
    data=transformacoes(test_raw)
    
    #predict
    df_response=get_prediction(model,test_raw,data)
    return df_response

  else:
    return Response('{}',status=200,mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)