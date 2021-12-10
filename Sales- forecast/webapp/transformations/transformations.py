import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime


class transformations(object): 
  def __init__(self):    
    self.competition_distance      =pickle.load(open('parameters/competition_distance_scaler.pkl','rb'))
    self.competition_time_month    =pickle.load(open('parameters/competition_time_month_scaler.pkl','rb'))
    self.promo_time_week           =pickle.load(open('parameters/promo_time_week_scaler.pkl','rb'))
    self.store_type                =pickle.load(open('parameters/store_type_scaler.pkl','rb'))
    self.year                      =pickle.load(open('parameters/year_scaler.pkl','rb'))
    self.df10                      =pd.read_csv('dataset_test/test.csv')
    self.df_store_raw              =pd.read_csv('dataset_test/store.csv',low_memory=False)


  def data_cleaning(self,df1):
    df1=df1.copy()    

    #rename
    columns={'Store':'store', 'DayOfWeek':'day_of_week', 'Date':'date',
         'Open':'open', 'Promo':'promo', 'StateHoliday':'state_holiday',                
         'SchoolHoliday':'school_holiday', 'StoreType':'store_type',
         'Assortment':'assortment', 'CompetitionDistance':'competition_distance',
         'CompetitionOpenSinceMonth':'competition_open_since_month',
         'CompetitionOpenSinceYear':'competition_open_since_year',
         'Promo2':'promo2','Promo2SinceWeek':'promo2_since_week',
         'Promo2SinceYear':'promo2_since_year', 'PromoInterval':'promo_interval'}

    df1=df1.rename(columns=columns)

    df1['date']=pd.to_datetime(df1['date'])

    #competition_distance
    df1['competition_distance'].max()
    max_value=200000
    df1['competition_distance']=df1['competition_distance'].apply(lambda x : max_value if math.isnan(x) else x)    

    #competition_open_since_month 
    df1['competition_open_since_month']=df1.apply(lambda x : x['date'].month if math.isnan(x['competition_open_since_month']) else x['competition_open_since_month'],axis=1) 

    #competition_open_since_year 
    df1['competition_open_since_year']=df1.apply(lambda x : x['date'].year if math.isnan(x['competition_open_since_year']) else x['competition_open_since_year'],axis=1) 
        
    #promo2
    #promo2_since_week
    df1['promo2_since_week']=df1.apply(lambda x : x['date'].week if math.isnan(x['promo2_since_week']) else x['promo2_since_week'],axis=1)  

    #promo2_since_year  
    df1['promo2_since_year']=df1.apply(lambda x : x['date'].year if math.isnan(x['promo2_since_year']) else x['promo2_since_year'],axis=1)  

    #promo_interval 
    month_map={1:'Jan',2:'Fev',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dev'}   
    df1['promo_interval'].fillna(0,inplace=True) 
    df1['month_map']=df1['date'].dt.month.map(month_map)  
    df1['is_promo']=df1[['promo_interval','month_map']].apply(lambda x: 0 if x['promo_interval']==0 else 1 if x['month_map'] in x['promo_interval'].split(';') else 0,axis=1)

    #change types
    df1['competition_open_since_month']= df1['competition_open_since_month'].astype(int)
    df1['competition_open_since_year']=  df1['competition_open_since_year'].astype(int)
    df1['promo2_since_week']=            df1['promo2_since_week'].astype(int)
    df1['promo2_since_year']=            df1['promo2_since_year'].astype(int)

    return df1


  def feature_engeneering(self,df2):
    df2=df2.copy()

    #year
    df2['year']=df2['date'].dt.year

    #month
    df2['month']=df2['date'].dt.month

    #day
    df2['day']=df2['date'].dt.day

    #week of year
    df2['week_of_year']=df2['date'].dt.weekofyear

    #year week
    df2['year_week']=df2['date'].dt.strftime('%Y-%W')

    #competition since
    df2['competition_since']=df2.apply(lambda x: datetime.datetime(year=x['competition_open_since_year'],month=x['competition_open_since_month'],day=1),axis=1)
    df2['competition_time_month']=((df2['date']-df2['competition_since'])/30).apply(lambda x: x.days).astype(int)

    #promo since
    df2['promo_since']=df2['promo2_since_year'].astype(str)+'-'+df2['promo2_since_week'].astype(str)
    df2['promo_since']=df2['promo_since'].apply(lambda x: datetime.datetime.strptime(x +'-1' ,'%Y-%W-%w')-datetime.timedelta(days=7))
    df2['promo_time_week']=((df2['date']-df2['promo_since'])/7).apply(lambda x:x.days).astype(int)

    #assortment
    df2['assortment']=df2['assortment'].apply(lambda x:'basic' if x=='a' else 'extra' if x=='b' else 'extended')
    #state holiday
    df2['state_holiday']=df2['state_holiday'].apply(lambda x:'puplic_holiday' if x=='a' else 'easter_holiday' if x=='b' else 'christmas' if x=='c' else 'regular_day')
    return df2


  def data_preparation(self,df5):
    df5=df5.copy()
    #competition distance
    df5['competition_distance']=self.competition_distance.fit_transform(df5[['competition_distance']].values)    

    #competition time month
    df5['competition_time_month']=self.competition_time_month.fit_transform(df5[['competition_time_month']].values)
    
    #promo time week  
    df5['promo_time_week']=self.promo_time_week.fit_transform(df5[['promo_time_week']].values)
    
    #year
    df5['year']=self.year.fit_transform(df5[['year']].values)
    
    #state_holiday- One Hot Encoding
    df5=pd.get_dummies(df5,prefix=['state_holiday'],columns=['state_holiday'])

    #store_type- Label Encoding    
    df5['store_type']=self.store_type.fit_transform(df5['store_type'])
    
    #assortment- Ordinal Encoding
    assortment_dict={'basic':1,'extra':2,'extended':3}
    df5['assortment']=df5['assortment'].map(assortment_dict)

    #month
    df5['month_sin']=df5['month'].apply(lambda x:np.sin(x*(2.*np.pi/12)))
    df5['month_cos']=df5['month'].apply(lambda x:np.cos(x*(2.*np.pi/12)))

    #day
    df5['day_sin']=df5['day'].apply(lambda x:np.sin(x*(2.*np.pi/30)))
    df5['day_cos']=df5['day'].apply(lambda x:np.cos(x*(2.*np.pi/30)))

    #week of year
    df5['week_of_year_sin']=df5['week_of_year'].apply(lambda x:np.sin(x*(2.*np.pi/52)))
    df5['week_of_year_cos']=df5['week_of_year'].apply(lambda x:np.cos(x*(2.*np.pi/52)))

    #day of week
    df5['day_of_week_sin']=df5['week_of_year'].apply(lambda x:np.sin(x*(2.*np.pi/7)))
    df5['day_of_week_cos']=df5['week_of_year'].apply(lambda x:np.cos(x*(2.*np.pi/7))) 

    cols_selected=['store','promo','store_type','assortment','competition_distance','competition_open_since_month',
                      'competition_open_since_year','promo2','promo2_since_week','promo2_since_year','competition_time_month',
                      'promo_time_week','day_of_week_sin','day_of_week_cos','month_sin','month_cos','day_sin','day_cos','week_of_year_sin',
                      'week_of_year_cos']

    return df5[cols_selected]


  def dataset (self,loja):

    # merge test dataset + store
    # loading test dataset    
    df10 = self.df10
    df_store_raw=self.df_store_raw        

    df_test = pd.merge( df10, df_store_raw, how='left', on='Store' )

    # choose store for prediction
    df_test = df_test[df_test['Store'].isin( [loja] )]

    # remove closed days
    df_test = df_test[df_test['Open'] != 0]
    df_test = df_test[~df_test['Open'].isnull()]
    df_test = df_test.drop( 'Id', axis=1 )

    return df_test

    
      

  def get_prediction(self,model,original_data,data_transform):

    #prediction
    pred=model.predict(data_transform)
    
    #join pred into the original data
    original_data['Predictions']=np.expm1(pred)

    return original_data   

  def prediction_calculator(self,df4):

    df4=df4.copy()    
    df4=df4[['Store','Predictions']].groupby('Store').sum().reset_index()    

    return df4.to_json(orient='records',date_format='iso')  