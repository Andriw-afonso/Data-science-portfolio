import streamlit as st 
import json
import requests
import pandas as pd

@st.cache()
  
# function input
def prediction(loja):

  #Create dataframe
  df={'numero_da_loja':[loja]}
  df=pd.DataFrame(data=df,columns=['numero_da_loja'])
  
  #converter em json
  df1=json.dumps(df.to_dict(orient='records'))

  #API call
  path='https://sajhnfdcccccc.herokuapp.com/'
  url=path +'oi'
  headers={'content-type':'application/json'}  
  r=requests.post(url,data=df1,headers=headers)

  #Prediction
  df2=pd.DataFrame(r.json(),columns=r.json()[0].keys())
        
  return df2
      
  
# webapp  
def main():       
    # Config web
    html_temp = """ 
    <div style ="background-color:gray;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Previsão de vendas</h1> 
    </div> 
    """
      
    # display 
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # Imput    
    loja =st.number_input('Número da loja')       
     
    result =""
      
    # Predict 
    if st.button("Predict"):        
        result = prediction(loja) 
        st.success('Previsão: {}'.format(result))
        
     
if __name__=='__main__': 
    main()
