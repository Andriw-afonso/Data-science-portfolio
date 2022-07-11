import streamlit as st 
import json
import requests
import pandas as pd

@st.cache()
  
# function input
def prediction(Cholesterol,ApLo,ApHi,Age):
  #Create dataframe
  d = {'Cholesterol':[Cholesterol],'ApLo':[ApLo],'ApHi':[ApHi],'Age':[Age]}
  df = pd.DataFrame(data=d)

  #converter em json
  df=json.dumps(df.to_dict(orient='records'))

  #API call
  path='https://sdbfsdfbqqqqq.herokuapp.com/'
  url=path +'oi'
  headers={'content-type':'application/json'}  
  r=requests.post(url,data=df,headers=headers)

  #Prediction
  df=pd.DataFrame(r.json(),columns=r.json()[0].keys())

  a=df['Predictions'][0]
  if a==1:
    b='Sick'
  elif a==0:
    b='Healthy'
  else: 
    b='ERRO DE PREDICAO'
        
  return b
      
  
# webapp  
def main():       
    # Config web
    html_temp = """ 
    <div style ="background-color:gray;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Diagnóstico precoce cardiovascular</h1> 
    </div> 
    """
      
    # display 
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # Imput
    Cholesterol = st.selectbox('Nível de colesterol',('1','2','3'))
    ApLo =        st.number_input('Pressão diastólica')
    ApHi =        st.number_input('Pressão sistólica')      
    Age =         st.number_input('Idade') 

    result =""
      
    # Predict 
    if st.button("Predict"):        
        result = prediction(Cholesterol,ApLo,ApHi,Age) 
        st.success('Estado de saúde: {}'.format(Cholesterol,ApLo,ApHi,Age))
        
     
if __name__=='__main__': 
    main()