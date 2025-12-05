# 🍕 API Pizzaria MPC — Backend Profissional para Gestão de Pizzarias

API REST completa para gerenciamento operacional de uma pizzaria, incluindo sistema de login com JWT, controle de produtos, estoque, pedidos e segurança aplicada com hash e validações. Desenvolvida para ser robusta, escalável e integrável com frontend, sistemas externos e automações.

# 📌 Sumário
- Visão Geral
- Funcionalidades Principais
- Tecnologias Utilizadas
- Instalação e Execução
- Arquitetura e Estrutura do Projeto
- Autenticação JWT
- Endpoints da API
- Exemplos de Requests
- Boas Práticas Implementadas
- Autor

# 🧭 Visão Geral
A API Pizzaria MPC foi projetada para administrar todos os aspectos operacionais de uma pizzaria. O sistema permite controlar produtos, usuários, login seguro, pedidos, estoque e histórico, utilizando uma arquitetura organizada e moderna.

# 🚀 Funcionalidades Principais

## 🔐 Sistema de Login com JWT
- Login seguro via JWT (expiração configurável)
- Proteção de rotas com Bearer Token
- Controle de acesso por usuário

## 🧂 Criptografia de Senhas
- Hash de senhas com bcrypt
- Sem armazenamento de senhas em plaintext
- Proteção contra ataques comuns

## 🍕 Gerenciamento de Produtos
- CRUD de produtos
- Categorias de pizzas, bebidas e adicionais
- Preço, descrição, tipo e disponibilidade

## 📦 Controle de Estoque
- Estoque atualizado automaticamente
- Bloqueio de pedidos com itens faltantes
- Funções para adicionar/remover quantidade

## 🛒 Gerenciamento de Pedidos
- Criação de pedidos completos
- Atualização de status (Pendente → Preparando → Entregue)
- Cálculo automático do valor final
- Histórico completo de pedidos

## 📊 Histórico e Registros
- Consultas avançadas
- Relatórios por data, valor ou status

## 🧰 Outras Funcionalidades
- Arquitetura modular MVC
- Respostas uniformizadas
- Proteção contra SQL Injection
- Integração com automações

# 🛠️ Tecnologias Utilizadas
- Python 3.x
- FastAPI
- SQLAlchemy ORM
- JWT Authentication
- bcrypt
- PostgreSQL / SQLite
- Docker e docker-compose
- Uvicorn ASGI

# ⚙️ Instalação e Execução

## 1️⃣ Clone o repositório
  ```bash
  git clone https://github.com/Joao-Pontes22/API--Pizzaria-MPC.git
  cd API--Pizzaria-MPC
  ```

## 2️⃣ Crie o ambiente virtual (opcional)
  ```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
  ```
## 3️⃣ Instale as dependências
  ```bash
pip install -r requirements.txt
  ```
## 4️⃣ Configure o arquivo .env
  ```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/pizzaria
SECRET_KEY=sua_chave_secreta
  ```
## 5️⃣ Execute a API
  ```bash
uvicorn main:app --reload
  ```
## 6️⃣ Usando Docker (opcional)
  ```bash
docker-compose up --build
  ```
## 📄 Documentação automática
  ```bash
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
  ```
# 🏛️ Arquitetura e Estrutura do Projeto
  ```bash
Projeto-Pizzaria/
├── Routes/        # Rotas organizadas por recurso
├── Models/        # ORM / tabelas do banco
├── Schemas/       # Validações Pydantic
├── Services/      # Regras de negócio
├── Database/      # Conexão e sessão
├── Security/      # JWT e Hash
├── main.py        # Entrada da API
├── requirements.txt
└── README.md
  ```
# 🔐 Autenticação JWT
  ```bash
Fluxo:
1. Envia email + senha
2. API valida credenciais
3. Retorna token JWT
4. Token é enviado no header:
  ```
  ```bash
Authorization: Bearer seu_token
  ```
# 📡 Endpoints da API

## 🔑 Autenticação
  ```bash
POST /auth/register        → cria usuário  
POST /auth/login           → retorna JWT  
GET  /auth/me              → dados do usuário logado  
  ```
## 🍕 Produtos
  ```bash
GET    /products           → lista produtos  
GET    /products/{id}      → busca por ID  
POST   /products           → cria produto  
PUT    /products/{id}      → atualiza  
DELETE /products/{id}      → deleta  
  ```
## 📦 Estoque
  ```bash
GET  /stock                → lista estoque  
PUT  /stock/update         → atualiza item  
PUT  /stock/increase/{id}  → adiciona quantidade  
PUT  /stock/decrease/{id}  → reduz quantidade  
  ```
## 🛒 Pedidos
  ```bash
POST   /orders             → cria pedido  
GET    /orders             → lista pedidos  
GET    /orders/{id}        → busca pedido  
PUT    /orders/{id}/status → atualiza status  
DELETE /orders/{id}        → cancela pedido  
  ```
# 📌 Exemplos de Requests

## Criar Produto
  ```bash
{
  "name": "Pizza Calabresa",
  "price": 39.90,
  "category": "pizza",
  "description": "Calabresa, cebola e queijo"
}
  ```
## Login
  ```bash
{
  "email": "admin@pizzaria.com",
  "password": "123456"
}
   ```
## Criar Pedido
  ```bash
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
  ```
# 🔒 Boas Práticas Implementadas
- Hash seguro de senhas
- JWT com expiração
- Arquitetura modular
- Padronização de respostas
- Tratamento de erros
- Otimização com ORM
- Segurança contra SQL Injection
- Separação entre camadas (Routes, Models, Schemas)
- Facilmente escalável com Docker

# 👤 Autor
João Vitor Oliveira Pontes  
GitHub: https://github.com/Joao-Pontes22
