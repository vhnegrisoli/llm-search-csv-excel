# 🤖 AI CSV Excel Search Assistant

Um assistente de IA que realiza **pesquisas inteligentes** e **gera gráficos automaticamente** com base em planilhas `.csv` e `.xlsx`.  
Ideal para análises automatizadas de dados, visualização e exploração de insights — tudo por meio de uma **API desenvolvida com FastAPI**.

---

## ✨ Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** – API rápida e moderna
- **LangChain** – Cadeias de raciocínio com LLMs
- **OpenAI** – Geração de linguagem natural - trabalhado modelo **gpt-4o-mini**
- **Pandas** – Manipulação de dados
- **Matplotlib & Seaborn** – Geração de gráficos e visualizações

---

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
````

---

## ▶️ Como rodar

```bash
uvicorn src.main:app --reload
```

Acesse a documentação interativa em:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Funcionalidades

### 🔍 `/api/search`

**Descrição:**
Executa uma consulta em uma planilha já enviada, interpretando a requisição com um LLM e retornando insights e gráficos.

**Método:** `POST`
**Body (JSON):**

```json
{
  "query": "qual a média de vendas por região?",
  "file_name": "vendas_abril.csv",
  "file_delimiter": ";"
}
```

**Resposta esperada:**

```json
{
  "status": "OK"
}
```

---

### 📁 `/api/upload`

**Descrição:**
Realiza o upload de um arquivo `.csv` ou `.xlsx` para posterior análise.

**Método:** `POST`
**Body (form-data):**

* `file`: Arquivo da planilha

**Resposta esperada:**

```json
{
  "file_id": "uuid-gerado",
  "message": "Arquivo enviado com sucesso!",
  "file_path": "files/vendas_abril.csv"
}
```

---

## 📂 Estrutura do Projeto (simplificada)

```

.
├── app.py                                  # Arquivo principal que inicializa a FastAPI
├── .env                                    # Variáveis de ambiente
├── .gitignore
├── README.md
├── requirements.txt

├── src/
│   ├── llm/                                # Integração com LLMs (LangChain/OpenAI)
│   │   ├── llm\_integration.py             # Setup e comunicação com o modelo de linguagem
│   │   └── prompts.py                      # Prompt engineering e templates
│   ├── models/                             # Schemas (Pydantic) para entrada e saída da API
│   │   ├── dataframe.py
│   │   ├── endpoint.py
│   │   └── llm\_models.py
│   ├── routes/                             # Rotas da API
│   │   ├── search\_route.py                # Rota de busca e análise
│   │   └── upload\_route.py                # Rota de upload de planilhas
│   ├── services/                           # Lógica de negócio
│   │   ├── command\_service.py             # Executa comandos baseados no input do LLM
│   │   ├── dataframe\_info\_service.py     # Extrai informações básicas da planilha
│   │   ├── llm\_service.py                 # Camada de serviço para LLM
│   │   ├── pandas\_processor\_service.py   # Interpreta e executa código Pandas
│   │   ├── upload\_service.py              # Lida com arquivos recebidos
│   │   └── user\_intention\_service.py     # Determina a intenção do usuário via IA
│   └── utils/
│       └── file\_utils.py                  # Utilitários para lidar com arquivos

```

---

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## ✍️ Autor

**Victor Hugo Negrisoli**
🔗 [LinkedIn](https://www.linkedin.com/in/victorhugonegrisoli/) | 🐙 [GitHub](https://github.com/vhnegrisoli/)