<img src = "imgs/capa.png" alt = "desenho" largura = "100%" />


# Objetivo:
Prever a demanda de vendas das lojas nas próximas 6 semanas.

## Problema de negócio:
O CFO da empresa fez uma reunião com todos os Gerentes de loja e pediu para que cada um deles trouxesse uma previsão  das próximas 6 semanas de vendas, o motivo do pedido é porque ele quer administrar o melhor possível o budget para a reforma das lojas.
Depois dessa reunião, todos os gerentes entraram em contato com você, e requisitaram uma previsão de vendas de sua loja.

## Mapa das dimensões do problema (Features):
<img src = "imgs/DAYLE_STORE_SALES.png" alt = "desenho" largura = "100%" />

# Proposta de solução:
- Dashboard com os insights mais relevantes para o negócio.
- Aplicação Web, onde o gerente irá inserir o número da loja e verificar a previsão de vendas.
- Demonstração de melhoria das métricas.

# Execução do projeto
## Tecnologias empregadas:
- Linguagem : Python 3.7.12
- Principais bibliotecas: sklearn, xgboost, flask,
seaborn, requests, pandas, e numpy.
- Ide: Google colab
- Backend da aplicação : Streamlit
- Cloud da aplicação (ML) : Heroku
- Mapas mentais: Google coggle
- Dashboard: PowerBI
- Imagens: Canva
- Versionamento de código: GitHub
- Modelo escolhido : XGBoost Regressor

## Insights:
### Features com maiores impactos no fenômeno :
- Número de clientes, lojas abertas, dias da semana, promoções.

### Features que existem correlação entre si (Escala de 0,0 há 1,0):
- Número de clientes  e Lojas abertas (0,65)
- Tipo da loja e o assortment (0,52)
- Promoções e Número de clientes (0,32)


### Quebra de paradigmas:
#### Lojas vendem:
- Menos aos finais de semana.
- Mais depois do dia 10 de cada mês.
- Mais no primeiro semestre do ano.
- Menos nos feriados de natal.
- Mais com competidores mais próximos.
<img src = "imgs/dashboard.png" alt = "desenho" largura = "100%" />

## Produto de Machine learning:
### Métricas atingidas:
- MAE:   889.07
- MAPE:  0.13
- RMSE:  1263.10

<img src = "imgs/metrics.png" alt = "desenho" largura = "100%" />

### Desempenho de negócio:
<img src = "imgs/negocio.png" alt = "desenho" largura = "100%" />



### Demonstração da aplicação:
 - Através do fornecimento de um link ,o  gerente é levado a uma página web onde é possível a inserção do número da loja, após o clique no botão "predict", é gerada a previsão de vendas para os próximos 30 dias.


<img src = "imgs/appstreamlit.png" alt = "desenho" largura = "100%" />


