# Imports
import pandas as pd
import streamlit as st
from minio import Minio
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Chave de acesso ao datalake
client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )


# Extraindo o dataset de predições
client.fget_object("curated","df_predictions.csv","df_predictions.csv")
var_predictions = 'df_predictions.csv'
df_predictions = pd.read_csv(var_predictions)[['Date','High','Low','Close']]

# Extraindo o dataset de métricas
client.fget_object("curated","df_metricas.csv","df_metricas.csv")
df_metricas = pd.read_csv('df_metricas.csv')

# Apresentações
st.title("Acompanhamento de desempenho dos modelos.")
st.markdown("Este app tem a função de prover as informações de controle de desempenho dos modelos .")

# Demonstrando as predições realizadas
st.markdown("Predições:")
st.dataframe(df_predictions.tail(5))

# Demonstrando as métricas alcançadas
st.markdown('Métricas:')
st.dataframe(df_metricas[['HighMAPE','LowMAPE','CloseMAPE']].head(1))

# Criando os graficos de predições
st.markdown('Acompanhamento gráfico:')
fig = plt.figure(figsize=(15, 6))

# HighPredict
plt.subplot(1,3,1)
plt.plot(df_metricas['Date'], df_metricas['High'])
plt.plot(df_metricas['Date'], df_metricas['HighPredict'])
plt.xlabel('Date')
plt.ylabel('Preço')
plt.legend(["Real", "Predict"], loc ="upper right")
plt.title('Modelo High')

# LowPredict
plt.subplot(1,3,2)
plt.plot(df_metricas['Date'], df_metricas['Low'])
plt.plot(df_metricas['Date'], df_metricas['LowPredict'])
plt.xlabel('Date')
plt.ylabel('Preço')
plt.legend(["Real", "Predict"], loc ="upper right")
plt.title('Modelo Low')

# ClosePredict
plt.subplot(1,3,3)
plt.plot(df_metricas['Date'], df_metricas['Close'])
plt.plot(df_metricas['Date'], df_metricas['ClosePredict'])
plt.xlabel('Date')
plt.ylabel('Preço')
plt.legend(["Real", "Predict"], loc ="upper right")
plt.title('Modelo Close')

plt.show()
st.pyplot(fig)





