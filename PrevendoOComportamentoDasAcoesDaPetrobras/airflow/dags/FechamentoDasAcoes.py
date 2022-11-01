# Imports
from airflow                            import DAG
from minio                              import Minio
from airflow.operators.python_operator  import PythonOperator
from airflow.operators.bash             import BashOperator
from airflow.models                     import Variable
from datetime                           import datetime,date, timedelta
from pandas_datareader                  import data as          web
import statsmodels.api                  as sm
import pandas                           as pd
import                                  pickle
import numpy                            as np

# Declarando as variaveis
data_lake_server   = Variable.get("data_lake_server")
data_lake_login    = Variable.get("data_lake_login")
data_lake_password = Variable.get("data_lake_password")

# Chave de acesso ao datalake
client = Minio(   data_lake_server,
                  access_key=      data_lake_login,
                  secret_key=      data_lake_password,
                  secure=          False )

# Argumentos
DEFAULT_ARGS = {  'owner':           'Airflow',
                  'depends_on_past': False,
                  'start_date':      datetime(2022, 10, 20)}


# Função que calcula o MAPE
def mean_absolute_percentage_error(y,yhat):
  return np.mean(np.abs((y-yhat)/y))


# Cria a função que faz a diferenciação
def difference( dataset, interval=1):
  diff = list()
  for i in range(interval, len(dataset)):
    value = dataset[i] - dataset[i - interval]
    diff.append(value)
  return diff


# Cria a função que reverte o valor diferenciado para o original
def inverse_difference( history, previsao, interval=1):
  return previsao + history[-interval]


# Função que carrega os modelos
def carregando_o_modelo(modelo):

    # Extraindo os dados do datalake
    client.fget_object("processing", "dataset.parquet","temp_.parquet")
    df = pd.read_parquet("temp_.parquet").set_index('Date')
    
    # Criando a series
    series = df['Close'].copy()

    # Cria a variável history
    history = [x for x in series]

    # Extraindo o modelo do datalake
    nome_do_modelo = modelo + ".pkl"
    client.fget_object("curated",modelo,"temp_.pkl")   
    model_fit = pickle.load(open("temp_.pkl",'rb'))

    # A variável valor_predito recebe o valor previsto pelo modelo
    valor_predito = model_fit.forecast()[0] 

    # valor_predito recebe o valor revertido (escala original)
    valor_predito = inverse_difference(history, valor_predito, 12)  

    return valor_predito 


# Função de extração
def extract ():

    # Carregando os dados das cotações
    data_inicial = f'20-10-2021'   
    df_raw = web.DataReader(f'PETR4.SA', data_source='yahoo', start=data_inicial)
    
    # Persiste os arquivos na área de Staging.
    df_raw.to_csv( "/tmp/dataset.csv", index=True)

    # Carregando o dataset no datalake
    df_raw.to_csv("dataset.csv",index=False)
    client.fput_object("landing","dataset.csv","dataset.csv")


# Função que transforma o dataset para parquet
def load():

    # Carrega os dados a partir da área de staging.
    df_ = pd.read_csv("/tmp/dataset.csv")

    # Converte os dados para o formato parquet.
    df_.to_parquet("/tmp/dataset.parquet" ,index=True)

    # Carrega os dados para o Data Lake.
    client.fput_object( "processing", "dataset.parquet","/tmp/dataset.parquet")


# Função que realiza o treino do modelo_close
def treino_do_modelo_close():    

    # Extraindo os dados do datalake
    client.fget_object( "processing","dataset.parquet","temp_.parquet")
    df = pd.read_parquet("temp_.parquet").set_index('Date')
    
    # Criando a series
    series = df['Close'].copy()

    # Cria a variável history
    history = [x for x in series]

    # Difference data
    meses_no_ano = 12
    diff = difference(history, meses_no_ano)

    # Best parameters
    best_params = {'AR': 1, 'I': 1, 'MA': 1, 'so1': 1, 'so2': 1, 'so3': 1, 'so4': 12}

    # Training
    order = (best_params['AR'],best_params['I'],best_params['MA'])
    seasonal_order = (best_params['so1'],best_params['so2'],best_params['so3'],best_params['so4'])

    # Cria um modelo com os dados de history
    model = sm.tsa.statespace.SARIMAX(diff, order=order, seasonal_order=seasonal_order)

    # Treina o modelo ARIMA
    model_fit = model.fit()

    # Salvando o modelo treinado 
    pickle.dump(model_fit, open('/tmp/model_close.pkl','wb'))

    # Salvando o modelo treinado no datalake
    client.fput_object("curated","model_close.pkl","/tmp/model_close.pkl")


# Função que realiza o treino do modelo_high
def treino_do_modelo_high():    

    # Extraindo os dados do datalake
    client.fget_object( "processing","dataset.parquet","temp_.parquet")
    df = pd.read_parquet("temp_.parquet").set_index('Date')
    
    # Criando a series
    series = df['High'].copy()

    # Cria a variável history
    history = [x for x in series]

    # Difference data
    meses_no_ano = 12
    diff = difference(history, meses_no_ano)

    # Best parameters
    best_params = {'AR': 1, 'I': 1, 'MA': 1, 'so1': 1, 'so2': 1, 'so3': 1, 'so4': 12}

    # Training
    order = (best_params['AR'],best_params['I'],best_params['MA'])
    seasonal_order = (best_params['so1'],best_params['so2'],best_params['so3'],best_params['so4'])

    # Cria um modelo com os dados de history
    model = sm.tsa.statespace.SARIMAX(diff, order=order, seasonal_order=seasonal_order)

    # Treina o modelo ARIMA
    model_fit = model.fit()

    # Salvando o modelo treinado 
    pickle.dump(model_fit, open('/tmp/model_high.pkl','wb'))

    # Salvando o modelo treinado no datalake
    client.fput_object("curated","model_high.pkl","/tmp/model_high.pkl")


# Função que realiza o treino do modelo_low
def treino_do_modelo_low():    

    # Extraindo os dados do datalake
    client.fget_object( "processing","dataset.parquet","temp_.parquet")
    df = pd.read_parquet("temp_.parquet").set_index('Date')
    
    # Criando a series
    series = df['Low'].copy()

    # Cria a variável history
    history = [x for x in series]

    # Difference data
    meses_no_ano = 12
    diff = difference(history, meses_no_ano)

    # Best parameters
    best_params = {'AR': 1, 'I': 1, 'MA': 1, 'so1': 1, 'so2': 1, 'so3': 1, 'so4': 12}

    # Training
    order = (best_params['AR'],best_params['I'],best_params['MA'])
    seasonal_order = (best_params['so1'],best_params['so2'],best_params['so3'],best_params['so4'])

    # Cria um modelo com os dados de history
    model = sm.tsa.statespace.SARIMAX(diff, order=order, seasonal_order=seasonal_order)

    # Treina o modelo ARIMA
    model_fit = model.fit()

    # Salvando o modelo treinado 
    pickle.dump(model_fit, open('/tmp/model_low.pkl','wb'))

    # Salvando o modelo treinado no datalake
    client.fput_object("curated","model_low.pkl","/tmp/model_low.pkl")


# Realiza as predições
def predictions():

    # Extraindo os dados do datalake
    client.fget_object( "processing","dataset.parquet","temp_.parquet")
    df = pd.read_parquet("temp_.parquet").set_index('Date')

    # Carregando os modelos e realizado as predições
    valor_predito_modelo_high  = carregando_o_modelo("model_high.pkl")
    valor_predito_modelo_low   = carregando_o_modelo("model_low.pkl")
    valor_predito_modelo_close = carregando_o_modelo("model_close.pkl")

    # Verificando se existe o df_predictions no datalake
    try:
        # Extraindo os dados do datalake
        client.fget_object("curated","df_predictions.csv","temp_.csv")
        estado = True
    except:
        estado = False

    # Inserindo as novas prediçõe no dataframe existente
    if estado == True:
        df_predictions = pd.read_csv('temp_.csv')
        data_atual     = list(df.reset_index().tail(1)['Date'])[0]
        data = {    'Date':          [data_atual],
                    'High': [valor_predito_modelo_high],
                    'Low':  [valor_predito_modelo_low],
                    'Close':[valor_predito_modelo_close]}
        aux = pd.DataFrame(data)        
        estado2        = data_atual in list(df_predictions['Date'])

        if estado2 == False:

            # Concatenando as novas predições no df_predictions
            df_predictions = pd.concat([df_predictions, aux],axis=0)

            # Persiste oas predições na área de Staging.
            df_predictions.to_csv( "/tmp/df_predictions.csv" ,index=True)       

            # Carregando as predições no datalake
            client.fput_object("curated","df_predictions.csv","/tmp/df_predictions.csv")
    
    else:
        # Caregando as predições no dataframe
        columns                                 = ['Date','High','Low','Close']
        df_predictions                          = pd.DataFrame(columns=columns)
        data_atual                              = list(df.reset_index().tail(1)['Date'])[0]
        df_predictions.loc[len(df_predictions)] = [data_atual, valor_predito_modelo_high,valor_predito_modelo_low ,valor_predito_modelo_close]

        # Persiste oas predições na área de Staging.
        df_predictions.to_csv( "/tmp/df_predictions.csv" ,index=True)       

        # Carregando as predições no datalake
        client.fput_object("curated","df_predictions.csv","/tmp/df_predictions.csv")

# Cria o dataset com as métricas do modelo
def dataset_de_metricas():     

    # Carregando os dados originais
    client.fget_object("processing","dataset.parquet","temp_.parquet")
    df_real = pd.read_parquet("temp_.parquet")[['Date','High','Low','Close']]

    # Carregando as predições
    client.fget_object("curated","df_predictions.csv","df_predictions.csv")
    df_predictions = pd.read_csv("df_predictions.csv")[['Date','High','Low','Close']]
    columns = {'Date':'Date','High':'HighPredict','Low':'LowPredict','Close':'ClosePredict'}
    df_predictions.rename(columns=columns, inplace=True)

    # Merge de df_real e df_predictions
    df_metricas = pd.merge(df_real,df_predictions, how='left',on='Date' )
    df_metricas = df_metricas[df_metricas['HighPredict'].isna()==False]

    # Calculando o MAPE
    df_metricas['HighMAPE']  = mean_absolute_percentage_error(df_metricas['High'],df_metricas['HighPredict'])
    df_metricas['LowMAPE']   = mean_absolute_percentage_error(df_metricas['Low'],df_metricas['LowPredict'])
    df_metricas['CloseMAPE'] = mean_absolute_percentage_error(df_metricas['Close'],df_metricas['ClosePredict'])
    df_metricas['TotalMAPE'] = (df_metricas['HighMAPE']+df_metricas['LowMAPE']+df_metricas['CloseMAPE'])/3
       
    
    # Carregando o dataset de metricas no datalake
    df_metricas.to_csv('/tmp/df_metricas.csv')
    client.fput_object("curated","df_metricas.csv","/tmp/df_metricas.csv")



# Declarando a DAG
dag = DAG('FechamentoDasAcoes', 
          default_args=DEFAULT_ARGS,
          start_date=datetime(2022, 10, 28),
          schedule_interval="@once")

# Task extract
extract_task = PythonOperator( task_id=         'extraindo_os_dados_da_api',
                               provide_context= True,
                               python_callable= extract,
                               dag=             dag)

# Task load
load_task = PythonOperator(   task_id=          'transformando_para_formato_parquet',
                              provide_context=  True,
                              python_callable=  load,
                              dag=              dag)

# Task treino_modelo_high
treino_modelo_high_task = PythonOperator( task_id=          'treinando_o_modelo_high',
                                          provide_context=  True,
                                          python_callable=  treino_do_modelo_high,
                                          dag=              dag)

# Task treino_modelo_low
treino_modelo_low_task = PythonOperator( task_id=          'treinando_o_modelo_low',
                                         provide_context=  True,
                                         python_callable=  treino_do_modelo_low,
                                         dag=              dag)

# Task treino_modelo_close
treino_modelo_close_task = PythonOperator( task_id=          'treinando_o_modelo_close',
                                           provide_context=  True,
                                           python_callable=  treino_do_modelo_close,
                                           dag=              dag)

# Task predictions
predictions_task = PythonOperator(  task_id =         'realizando_as_predições',
                                    provide_context = True,
                                    python_callable = predictions,
                                    dag =             dag)

# Task metricas
metricas_task = PythonOperator(  task_id =           'criando_o_dataset_de_metricas',
                                 provide_context =   True,
                                 python_callable =   dataset_de_metricas,
                                 dag =               dag)

extract_task >> load_task >> [treino_modelo_high_task ,treino_modelo_low_task,treino_modelo_close_task]>> predictions_task >> metricas_task 
