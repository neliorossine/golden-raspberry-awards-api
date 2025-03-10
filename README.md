# Golden Raspberry Awards API

<p align="center"><img src="https://www.lacosacine.com/wp-content/uploads/2023/01/Razzie-Awards.jpg"></p>

<br><br>

## Descrição
Esta API foi desenvolvida para analisar os prêmios da categoria "Pior Filme" do Golden Raspberry Awards, destacando os intervalos entre vitórias consecutivas de produtores. Seu principal objetivo é identificar e retornar os produtores com os menores e maiores intervalos entre prêmios. Além disso, a API oferece funcionalidades adicionais, incluindo recursos baseados em inteligência artificial para previsão e recomendações personalizadas.
<br>
<br>
<br>

___


## Pré-requisitos
- Docker
- Docker Compose

<br>

<br>

___


## Tecnologias Utilizadas

<br>

O projeto foi desenvolvido utilizando as seguintes tecnologias e ferramentas:

- Python: Linguagem principal utilizada para a construção da API.
- Flask: Framework para desenvolvimento de aplicações web.
- Pandas: Biblioteca para manipulação e análise de dados, utilizada para processar o dataset de filmes.
- Scikit-learn: Utilizado para implementar funcionalidades de IA, como previsão e agrupamento de filmes.
- SQLAlchemy: ORM utilizado para interação com o banco de dados de forma mais eficiente.
- Docker: Para containerização da aplicação e garantir um ambiente de execução consistente.
- Docker Compose: Para orquestração de múltiplos containers, incluindo banco de dados.
- SQLite: Banco de dados leve utilizado para persistência de dados.
- UnitTest: Ferramenta de testes automatizados para garantir a qualidade e funcionamento correto da aplicação.
- Make: Automação de comandos frequentes, como iniciar e testar a aplicação.
- HATEOAS: Implementado nos endpoints para enriquecer as respostas com links úteis e navegáveis.


<br>

<br>

___



## Como executar

<br>

1. Clone o repositório:

   ```bash
   git clone <seu-repositorio>
   cd <seu-repositorio>

<br>

2. Para iniciar o ambiente com banco de dados persistente (Os dados permanecem salvos entre execuções):

    ```bash
     make run

<br>

3. Para iniciar o ambiente com banco de dados em memória 
(Todos os dados são apagados ao parar o ambiente) :

   ```bash
   make run-memory

<br>

4. Acesse a API e sua documentação no endereço http://localhost:5000/

<br>
<br>

___

## Limpar o ambiente
<br>

Para parar os containers e remover volumes:

   ```bash
    make clean
   ```


<br>


___


<br>

## Criar e ativar o ambiente virtual:

Se você preferir usar um ambiente virtual, pode criar um com venv. Aqui estão os passos:

<br>

Para Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

<br>

Para Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

<br>


## Testes

<br>

- Para executar os testes automatizados, use o comando:

    ```bash
    make test

<br>

Os testes cobrem os seguintes cenários e são organizados em duas categorias principais: Testes de Endpoints da API e Testes de Lógica de Negócio (Serviços).

<br>

#### Testes de Endpoints da API:
Os testes de integração validam os seguintes comportamentos:
- Banco de dados vazio: Verifica como os endpoints se comportam quando o banco de dados não possui registros.
- Prêmios (/app/awards):
  - Com banco de dados vazio: O endpoint retorna listas vazias para intervalos mínimo e máximo.
  - Com dados: Valida a identificação correta dos intervalos de vitórias mínimas e máximas entre produtores.
  - Múltiplos produtores com o mesmo intervalo: Testa o comportamento ao lidar com intervalos iguais entre diferentes produtores.
- Detalhes dos produtores (/app/details e /app/producers/<producer>):
  - Verifica se os detalhes retornam informações corretas ou um erro no caso de produtores inexistentes.
- Lista de filmes (/app/movies): Testa se o endpoint retorna corretamente uma lista de filmes.
- Vencedores por ano (/app/winners):
  - Com ano válido: Retorna os vencedores registrados para o ano informado.
  - Sem vencedores no ano: Retorna uma mensagem de erro indicando que não há vencedores para o ano especificado.
- Recomendações de filmes (/ai/recommendations):
  - Verifica se o endpoint retorna campos obrigatórios como movies_in_cluster e se a estrutura da resposta está correta.
- Previsão de "filmes ruins" (/ai/predict-bad-movie):
  - Parâmetros válidos: Retorna uma previsão indicando a probabilidade de o filme ser considerado "ruim".
  - Parâmetros ausentes ou inválidos: Verifica se retorna erro (status 400) com uma mensagem explicativa.

  

<br>

#### Testes de Lógica de Negócio (Serviços):

Os testes de unidade cobrem as funções internas que realizam cálculos importantes:



- Função calculate_awards: Essa função é responsável por calcular os intervalos de vitórias de diferentes produtores.
  - Com dados vazios: Retorna listas vazias para intervalos mínimo e máximo.
  - Com dados válidos: Calcula corretamente os menores e maiores intervalos de vitória entre produtores, incluindo anos de vitórias anteriores e subsequentes.
  - Com múltiplos intervalos iguais: Testa como a função lida com cenários onde diferentes produtores têm intervalos iguais.
  - Com um único produtor: Lida com intervalos quando um único produtor possui várias vitórias.
  - Sem vitórias consecutivas: Retorna listas vazias para intervalos mínimo e máximo, pois não há vitórias consecutivas para nenhum produtor.


<br>
<br>


#### Estrutura dos Testes

Os arquivos de teste estão organizados da seguinte maneira:
- test_routes.py: Contém os testes de integração para os endpoints da API.
- test_services.py: Contém os testes de unidade para as funções de lógica de negócio, como calculate_awards.

Esses testes garantem que a API e os serviços funcionem corretamente, cobrindo uma ampla gama de cenários, desde dados vazios até entradas específicas para cálculos de premiação.


<br>
<br>

___


## Estrutura do Projeto
O projeto segue a seguinte estrutura de diretórios:
```
.
├── app/
│   ├── app.py                  # Configuração principal do Flask.
│   ├── routes.py               # Configuração das rotas principais.
│   ├── ai_routes.py            # Configuração das rotas de IA.
│   ├── models.py               # Definição dos modelos.
│   ├── services.py             # Lógica de negócios.
│   ├── config.py               # Configurações do Flask.
│   ├── utils.py                # Funções utilitárias e helpers.
├── data/
│   ├── movielist.csv           # Arquivo CSV com dados de filmes.
│   ├── database.db             # Arquivo SQLite com dados persistidos.
├── tests/
│   ├── unit/
│   │   ├── test_services.py    # Testes unitários.
│   ├── integration/
│       ├── test_routes.py      # Testes de integração.
├── .env                        # Variáveis de ambiente.
├── .gitignore                  # Arquivos a ignorar no Git.
├── Dockerfile                  # Configuração para criar a imagem Docker.
├── docker-compose.yml          # Orquestração dos containers.
├── Makefile                    # Atalhos para rodar a aplicação e os testes.
├── requirements.txt            # Dependências do Python
└── README.md                   # Documentação do projeto
```
<br>
<br>

___


## Endpoints da API

A API possui os seguintes endpoints:

<br>

### `GET /app/awards`
Retorna os produtores com:
- O maior intervalo entre dois prêmios consecutivos.
- O menor intervalo entre dois prêmios consecutivos.

<br>


#### Exemplo de Resposta:
```json
{
  "min": [
    {
      "producer": "Producer 1",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009
    }
  ],
  "max": [
    {
      "producer": "Producer 2",
      "interval": 10,
      "previousWin": 2000,
      "followingWin": 2010
    }
  ]
}
```
<br>
<br>
<br>

### `GET /app/details`
Retorna o mesmo conteúdo do endpoint /app/awards, mas com links HATEOAS para mais informações sobre os produtores e filmes relacionados.

<br>

#### Exemplo de Resposta:
```json
{
  "min": [
    {
      "producer": "Producer 1",
      "interval": 1,
      "previousWin": 2008,
      "followingWin": 2009,
      "_links": {
        "producer_details": "/producers/Producer 1",
        "movie_details": [
          "/movies?year=2008",
          "/movies?year=2009"
        ]
      }
    }
  ],
  "max": [
    {
      "producer": "Producer 2",
      "interval": 10,
      "previousWin": 2000,
      "followingWin": 2010,
      "_links": {
        "producer_details": "/producers/Producer 2",
        "movie_details": [
          "/movies?year=2000",
          "/movies?year=2010"
        ]
      }
    }
  ]
}
```

<br>
<br>
<br>
<br>

### `GET /app/producers/<producer>`
Retorna informações detalhadas sobre um produtor específico e a lista de seus filmes vencedores.

Parâmetros:
- producer: Nome do produtor.

<br>


#### Exemplo de Resposta:
```json
{
  "producer": "Producer 1",
  "movies": [
    {
      "title": "Movie 1",
      "year": 2008
    },
    {
      "title": "Movie 2",
      "year": 2009
    }
  ]
}
```


<br>
<br>
<br>
<br>

### `GET /app/movies`
Retorna uma lista de todos os filmes registrados no banco de dados. Permite filtros opcionais.

Parâmetros Opcionais:
- year: Filtra os filmes pelo ano.
- producer: Filtra os filmes pelo produtor.
- title: Filtra os filmes pelo título.

<br>

#### Exemplo de Requisição:

```bash
  /app/movies?year=2008&title=Movie&producer=Producer
 ```
   
<br>

#### Exemplo de Resposta:
```json
[
  {
    "title": "Movie",
    "studios": "Studio",
    "producer": "Producer",
    "year": 2008,
    "winner": "yes"
  }
]
```
<br>
<br>
<br>
<br>

### `POST /app/winners`
Retorna os filmes vencedores de um determinado ano.

Parâmetros:
- `year`: Ano do qual queremos obter os vencedores.

<br>

#### Exemplo de Requisição:

```bash
    POST /app/winners
    {
      "year": "2005"
    }
  ```

<br>

#### Exemplo de Resposta:
```json
{
  "year": "2005",
  "winners": ["Movie 1", "Movie 2"]
}
```

<br>
<br>
<br>
<br>



### `GET /ai/recommendations`
Retorna uma recomendação de filmes com base em padrões de premiações, agrupando-os em clusters para sugerir possíveis filmes que podem ser considerados "ruins". A recomendação é gerada com base em análises de filmes anteriores e suas características, como prêmios e outros dados relacionados.

<br>

#### Funcionalidade:

- Quando um usuário acessa esta rota, a API busca filmes relacionados entre si e os organiza em clusters.
- A resposta inclui um identificador de cluster e a lista de filmes que fazem parte desse cluster.
- A resposta também inclui uma mensagem indicando que a recomendação foi gerada com sucesso.

<br>

#### Exemplo de Resposta:
```json
{
  "cluster": 0,
  "movies_in_cluster": ["Movie A", "Movie B", "Movie C"],
  "message": "Recomendação gerada"
}
```

<br>

#### Descrição dos campos:
- cluster: Um identificador numérico do cluster de filmes relacionados. Pode ser usado para identificar grupos de filmes com características similares.
- movies_in_cluster: Lista dos filmes presentes no cluster. Estes filmes compartilham características e padrões que os tornam candidatos para recomendação.
- message: Mensagem de sucesso indicando que a recomendação foi gerada corretamente.


<br>
<br>
<br>
<br>

### `POST /ai/predict-bad-movie`
Retorna uma previsão sobre a probabilidade de um filme ser considerado "ruim", com base nas características do produtor e estúdio. A previsão é gerada com base em dados históricos sobre o sucesso (ou fracasso) de filmes anteriores produzidos pelos mesmos produtores e estúdios.

<br>

#### Funcionalidade:
- O endpoint recebe uma requisição POST com informações sobre o produtor e o estúdio.
- A API analisa as combinações fornecidas e faz uma previsão de que o filme tem uma probabilidade de ser ruim ou não é provável ser ruim, com base em dados históricos de filmes anteriores.
- A previsão é retornada no campo prediction.


<br>

#### Exemplo de Requisição:

```bash
   POST /ai/predict-bad-movie
{
  "producer": "Producer 1",
  "studio": "Studio 1"
}
```
<br>

#### Exemplo de Resposta:
```json
{
  "prediction": "Probabilidade de ser ruim"
}
```
<br>

#### Descrição dos campos:

- prediction: A previsão gerada pela API, que pode ser:
  - "Probabilidade de ser ruim": Indica que, com base nas informações fornecidas (produtor e estúdio), o filme tem uma chance maior de ser considerado ruim.
  - "Não é provável ser ruim": Indica que o filme tem uma chance menor de ser ruim, com base nas mesmas informações.


#### Validação:
- Se a requisição não fornecer todos os parâmetros necessários (produtor ou estúdio ausente), a resposta será um erro 400, informando que os parâmetros estão faltando.




<br>

___

## Observações
- O banco de dados é automaticamente inicializado com os dados do arquivo movielist.csv na primeira execução.
- O sistema pode ser utilizado com outros conjuntos de dados no mesmo formato CSV, bastando substituir o arquivo e reiniciar o ambiente.
