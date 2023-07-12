# 4Djobz

#### O 4Djobz é um site de recrutamento de candidatos e anúncio de vagas de emprego.
##### O projeto foi criado utilizando Python 3.11 e Django 4.2.3, e os gráficos da empresa foram feitos com o Plotly em Javascript.

## ⚙️ Setup 
Para executar o projeto em um ambiente local, siga os passos abaixo:

```python -m venv venv; pip install -r requirements.txt; cp .env-example .env; python .\manage.py makemigrations; python .\manage.py migrate```

```python .\manage.py runserver```

Por padrão, o Django vai subir o projeto em `http://127.0.0.1:8000/`.

<img src="https://raw.githubusercontent.com/xbandrade/py-4djobz/main/screenshots/jobs_list.png" width=70% height=70%>

## 💻 Funcionalidades do Website

#### Header da Página Inicial:
- `Buscar Vagas` ➔ lista todas as vagas publicadas que ainda não foram finalizadas
- `Login` ➔ faz login na conta de candidato ou de empresa, usando o email como username
- `Registrar` ➔ cria uma nova conta de candidato ou de empresa

Ambos os registros de candidato e empresa têm alguns campos extras, mas os obrigatórios são `nome`, `email` e `senha`.

Após fazer login, os dois tipos de usuários têm dashboards diferentes.

### Dashboard do Candidato:
- `Suas Candidaturas` ➔ lista todas as candidaturas do candidato logado, com detalhes sobre a vaga e o status atual dela

#### Header do Dashboard:
- `Buscar Vagas` ➔ lista as publicações de vagas mais recentes, com opções de busca por título da vaga e candidatura ao acessar os detalhes
  - `Candidatar-se` ➔ envia uma candidatura à vaga, os campos `expectativa salarial`, `escolaridade mínima` e `experiências` são obrigatórios

<img src="https://raw.githubusercontent.com/xbandrade/py-4djobz/main/screenshots/applications.png" width=70% height=70%>


### Dashboard da Empresa:
- `Publicar Vaga` ➔ envia uma nova publicação de vaga, os campos `Título da Vaga`, `Salário`, `Escolaridade` e `Requisitos` são obrigatórios e é possível ocultar o salário da vaga para candidatos.
- `Checar gráficos da empresa` ➔ gera gráficos a partir dos dados de vagas publicadas e candidaturas nas vagas da empresa no último mês
- `Suas Vagas Publicadas` ➔ lista todas as vagas publicadas pela empresa, com detalhes da vaga, opções para editar/deletar e acesso a todos os candidatos que aplicaram à vaga 
  - `Candidatos para a vaga` ➔ lista os candidatos que aplicaram para aquela vaga, com opções para ordenar a lista por compatibilidade com a vaga, baseado na escolaridade e na expectativa salarial do candidato


<img src="https://github.com/xbandrade/py-4djobz/blob/main/screenshots/company_charts2.png" width=70% height=70%>


#### O arquivo `db.sqlite3.bkp` contém uma database previamente populada com diversos candidatos, empresas, candidaturas e vagas publicadas.
 - ➔ Login de candidato na database teste: b@email.com, senha 9264
 - ➔ Login de empresa na database teste: baxx@email.com, senha 9264

## ✔️ Testes
❕O projeto foi feito utilizando TDD com `pytest`, com testes unitários e de integração que estão armazenados na pasta `/tests/` de cada app.
