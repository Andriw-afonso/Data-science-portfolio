import pandas as pd
from sklearn.preprocessing   import RobustScaler,MinMaxScaler,LabelEncoder

def transformacoes(data):

  columns={   'step':'etapa','type':'tipos','amount':'montante','nameOrig':'remetente',
              'oldbalanceOrg':'saldo_inicial_remetente','newbalanceOrig':'saldo_atual_remetente',
              'nameDest':'destinatario','oldbalanceDest':'saldo_inicial_destinatario',
              'newbalanceDest':'saldo_atual_destinatario','isFraud':'fraude','isFlaggedFraud':'fraude_sinalizada'}

  data=data.rename(columns=columns)

  data['fraude']=data['fraude'].apply(lambda x:'sim' if x==1.0 else 'nao')

  data=data[data.index !=42270]

  data['fraude_sinalizada']=data['fraude_sinalizada'].astype(str)

  rs=RobustScaler()
  mms=MinMaxScaler()

  #MinMaxScaler
  #etapa
  data['etapa']=mms.fit_transform(data[['etapa']].values)

  #RobustScaler
  #montante
  data['montante']=rs.fit_transform(data[['montante']].values)

  #saldo_inicial_remetente
  data['saldo_inicial_remetente']=rs.fit_transform(data[['saldo_inicial_remetente']].values)

  #saldo_atual_remetente
  data['saldo_atual_remetente']=rs.fit_transform(data[['saldo_atual_remetente']].values)

  #saldo_inicial_destinatario
  data['saldo_inicial_destinatario']=rs.fit_transform(data[['saldo_inicial_destinatario']].values)

  #saldo_atual_destinatario
  data['saldo_atual_destinatario']=rs.fit_transform(data[['saldo_atual_destinatario']].values)

  #Label Encoding
  #tipo
  le=LabelEncoder()
  data['tipos']=le.fit_transform(data['tipos'])

  #cliente_remetente
  data['remetente']=le.fit_transform(data['remetente'])

  #cliente_destinatario
  data['destinatario']=le.fit_transform(data['destinatario'])

  #One Hot Encoding 
  #fraude
  data['fraude']=data['fraude'].apply(lambda x: 1 if x=='sim' else 0)

  data=data[['etapa','tipos','montante','saldo_inicial_remetente',
             'saldo_atual_remetente','destinatario','saldo_atual_destinatario']]
  return data
 
def get_prediction(model,dado_original,data_transforme):
  #prediction
  pred=model.predict(data_transforme)

  #join pred into the original data
  dado_original['predicoes']=pred

  return dado_original.to_json(orient='records',date_format='iso')