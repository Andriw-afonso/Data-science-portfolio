<img src = "imgs/capa.png" alt = "desenho" largura = "100%" />

# Introdução:
## Problema de negócio:
A House Rocket  é  uma empresa do setor imobiliário, o seu modelo de negócio consiste  na compra, reforma e venda de casas com seu valor de mercado depreciado.
O CEO precisa encontrar as melhores oportunidades de negócio em sua base de dados, pensando nisso, ele pediu ao cientista de dados  as seguintes tarefas:
### Relatório respondendo as seguintes perguntas: 

- Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
- Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?
- A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?
- Qual é o registro mais antigo?
- Quantas propriedades têm o número máximo de andares?
- Crie uma classificação de imóveis, separando-os em baixo e alto padrão, de acordo com o preço.
- Desejo um relatório ordenado por preço e com as seguintes informações:
    - ID de propriedade
    - Data em que a propriedade ficou disponível para compra
    - Numero de quartos
    - Tamanho total do lote
    - Preço
    - Classificação (padrão alto e baixo)
- Qual é a quantidade de imóveis por ano de construção?
- Qual é o menor número de cômodos por ano de construção de um imóvel?
- Qual é o preço de compra mais alto para cada número de quartos?
- Qual é a soma de todos os preços de compra por número de quartos?
- Qual é o tamanho médio da sala de estar nos edifícios por ano de construção?
- Qual é o tamanho mediano da sala de estar do imóvel por ano de construção?
- Qual é o desvio padrão da sala de estar em edifícios por ano de construção?
- Qual é o crescimento médio dos preços de compra de um imóvel, por ano, mês, dia e semana do ano?
- Gostaria de olhar no mapa e conseguir identificar as casas com o preço mais alto.

## Informações dos dados
### Features disponíveis:
- Id : Identificador do cliente
- Date : Data da avaliação do imóvel
- Price: Preço
- Bedrooms: Número de quartos
- Bathrooms: Número de banheiros
- SqftLiving: Área da sala de estar
- SqftLot: Área externa
- Floors: Número de andares
- Waterfront: Se a casa tem vista para o lago
- View: Se o cliente visitou a casa
- Condition: Estado de conservação do imóvel
- Grade: Nível de qualidade do imóvel
- SqftAbove: Área superior
- SqftBasement: Área do porão
- YrBuilt: Ano de construção
- YrRenovated: Ano de reforma
- Zipcode: Código de localização
- Lat : Latitude
- Long: Longitude
- SqftLiving15: Área atualizada da sala de estar
- SqftLot15: Área externa atualizada
<img src = "imgs/mindmap.png" alt = "desenho" largura = "100%" />

### Data Dimensions:
- Número de linhas: 21613
- Número de colunas: 21
### Estatística descritiva dos dados:
#### Numéricos:
<img src = "imgs/numericos.png" alt = "desenho" largura = "100%" />

#### Categóricos:
<img src = "imgs/categoricos.png" alt = "desenho" largura = "100%" />

# Proposta de solução:
## Definição da entrega:
-  Modelo de machine learning que realize o agrupamento das casas.
-  Relatório respondendo as perguntas do CEO. 
-  Dashboard com as features que possuem maior correlação com o fenômeno.


## Tecnologias empregadas:
- Linguagem: Python 3.7.12
- Principais bibliotecas: sklearn, seaborn, pandas, e numpy.
- Ide: Google colab
- Mapas mentais: Google coggle
- Dashboard: PowerBI
- Imagens: Canva
- Versão de código: GitHub
- Modelo escolhido: K- means

## Desafios enfrentados:
- A medida  de área no dataset é pés quadrados, foi convertido para metrôs quadrados.

# Resultados:
## Produto de Machine learning:
### Métricas atingidas:
- Silhouette: 0.603
- DaviesBouldin: 0.632	
- CalinskiHarabasz : 39760.069
<img src = "imgs/agrupamento.png" alt = "desenho" largura = "100%" />

## Respondendo as peguntas do CEO:

- Quais casas o CEO da House Rocket deveria comprar e por qual preço de compra?
<img src = "imgs/1.png" alt = "desenho" largura = "100%" />

- Uma vez a casa em posse da empresa, qual o melhor momento para vendê-las e qual seria o preço da venda?
<img src = "imgs/r2.png" alt = "desenho" largura = "100%" />

- A House Rocket deveria fazer uma reforma para aumentar o preço da venda? Quais seriam as sugestões de mudanças? Qual o incremento no preço dado por cada opção de reforma?
<img src = "imgs/r3.png" alt = "desenho" largura = "100%" />

- Qual é o registro mais antigo?
    - Id: 5101405331
- Quantas propriedades têm o número máximo de andares?
    - 567
- Crie uma classificação de imóveis, separando-os em baixo e alto padrão, de acordo com o preço.
<img src = "imgs/intervalo.png" alt = "desenho" largura = "100%" />
- Desejo um relatório ordenado por preço e com as seguintes informações:
    - ID de propriedade
    - Data em que a propriedade ficou disponível para compra
    - Numero de quartos
    - Tamanho total do lote
    - Preço
    - Classificação (padrão alto e baixo)
<img src = "imgs/h4.png" alt = "desenho" largura = "100%" />    

- Qual é a quantidade de imóveis por ano de construção?
<img src = "imgs/quantidade_anoconstrucao.png" alt = "desenho" largura = "100%" /> 

- Qual é o menor número de cômodos por ano de construção de um imóvel?
<img src = "imgs/quartos_ano.png" alt = "desenho" largura = "100%" /> 

- Qual é o preço de compra mais alto para cada número de quartos?
<img src = "imgs/precomaisalto_quartos.png" alt = "desenho" largura = "100%" /> 

- Qual é a soma de todos os preços de compra por número de quartos?
<img src = "imgs/somaprecos_quartos.png" alt = "desenho" largura = "100%" /> 

- Qual é o tamanho médio da sala de estar nos edifícios por ano de construção?
<img src = "imgs/saladeestra_anodeconstrucao.png" alt = "desenho" largura = "100%" /> 

- Qual é o tamanho mediano da sala de estar do imóvel por ano de construção?
<img src = "imgs/median.png" alt = "desenho" largura = "100%" /> 

- Qual é o desvio padrão do tamanho da sala em edifícios por ano de construção?
<img src = "imgs/padrao.png" alt = "desenho" largura = "100%" /> 

- Qual é o crescimento médio dos preços de compra de um imóvel, por ano, mês, dia e semana do ano?
<img src = "imgs/h12.png" alt = "desenho" largura = "100%" /> 

- Gostaria de olhar no mapa e conseguir identificar as casas com o preço mais alto.
<img src = "imgs/mapa.png" alt = "desenho" largura = "100%" />


## Dashboard com as features que possuem maior correlação com o fenômeno:
<img src = "imgs/dashboard.png" alt = "desenho" largura = "100%" /> 
<img src = "imgs/numerical_correlations.png" alt = "desenho" largura = "100%" />

# Próximos passos:
- Testar outros modelos de agrupamento como :
    - Optics, Mini-Batch K-Means,  Mean Shift,  Gaussian Mixture ,  BIRCH,  Agglomerative Clustering.
- Desenvolver um modelo que faça a precificação dos futuros imóveis para encontrar  propriedades com seu valor depreciado.
- Criar um dashboard interativo que resume as melhores oportunidades para o time de negócio.
# Referências:
- Os 5 Projetos de Data Science Que Fará o Recrutador Olhar para Você!, Meigarom Lopez, https://sejaumdatascientist.com/os-5-projetos-de-data-science-que-fara-o-recrutador-olhar-para-voce/

