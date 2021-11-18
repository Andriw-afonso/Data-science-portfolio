# Precificação de imóveis
Implementação de  modelo de machine learning que faça a precificação do valor dos imóveis.

<img src = "imgs/property_pricing.png" alt = "desenho" largura = "100%" />

## Descrição da solução :
    IMPORTS
        - Carregamento de bibliotecas
        - Desenvolvimento de Help Functions
            - Seletores de features, gráficos, cramerv e validação de modelos
        - Carregamento dos dados

    PASSO 1 - DESCRIPTION OF THE DATA
        -Renomeação de colunas
        -Identificação do tamanho da base de dados.
        -Identificação dos tipos das features (str,int,date e object)
        -Mudadança do tipo das features.
        -Verificação da presença de dados faltantes.
        -Separação  de atributos numéricos e categoricos.
        -Estatística descritiva de atributos numéricos (Min,Max,Range,Mean,Median,Std,Skew e kurtosis).
        -Identificação de numero de categorias por features.
        -Plote das features categoricas em relação a variavel resposta.

    PASSO 2 - FEATURE ENGINEERING
        -Desenvolvimento de mapa mental de hipoteses.
        -Criação de hipoteses.
        -Criação de features.

    PASSO 3 - VARIABLES FILTERING
        -Filtragem de linhas e outliers.
        -Exclusão de colunas que não agregam informação.

    PASSO 4 - EXPLORATORY DATA ANALYSIS
        -Univariate Analysis
            -Plote da distribuição da variavel resposta.
            -Dashboard da destribuição de variaveis numericas e categoricas.
        -Bivariate Analysis
            -Validação de 10 hipoteses
        -Report
            -Criação de relatório com perguntas de negócio com mapa interativo.

    PASSO 5 - DATA PREPARATION
        -Rescaling
            -Rescaling de features numericas com MinMaxScaler e RobustScaler.
        -Transformação
            -Encoding
                -Encoding das features categóricas em numéricas, utilizando One Hot Encoding,Label Encoding,Ordinal Encoding.
            -Transformação da variavel resposta atraves da função Log.
        -Nature transformation
            -Transformação das features temporais  com as funções de Seno e Cosseno.

    PASSO 6 - FEATURE SELECTION
        -Separaração dos dados de treino e de teste
        -Implementação do seletor de features, Boruta.

    PASSO 7 - MACHINE LEARNING MODELLING
        -Implementação e validação dos modelos:
            -BaseLine(LinearRegression)
            -Linear Regression Regularized -Model-Lasso 
            -Random Forest Regressor
            -XGBoost Regressor
            -Ridge 
            -ExtraTreesRegressor
        -Definição do modelo principal
            -O modelo escolhido foi o XGBoost Regressor.

    PASSO 8 - HYPERPARAMETER FINE TUNING
        -Definição dos melhores  parametros com Random Search.
        -Carregamento do modelo final treinado em pickel.

    PASSO 9 - TRANSLATION AND INTERPRETATION OF THE ERROR
        -Criação de  dashboard mostrando o ERRO das predições em relação a variavel resposta. 

    PASSO 10 - DEPLOY MODEL TO PRODUCTION
        -API
            -Criação da transformations class (data_cleaning,feature_engeneering,data_preparation e get_predict)
            -Criação da main do projeto (Handler.py)
            -Criação do requirements.txt (verçoes das bibliotecas)
            -Criação do arquivo Procfile (Ele que estarta o boot na cloud).
            -Deploy da API no Heroku
            -API Tester
                -Utilizando a URL para fazer as predições.

## Tecnologias utilizadas:
- Google Colab
- Python
- Heroku
- Visual Studio Code
- Canva

