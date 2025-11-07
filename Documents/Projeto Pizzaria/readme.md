# FASTAPI Pizza Delivery
- Sistema de delivery de pizzaria com controle de estoque, utilizando API RESTful, Python e FastAPI. Permite gerenciar pedidos, ingredientes, pizzas e usuários, com autenticação e controle de permissões.

# Tecnologias
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Alembic (para versionamento do banco de dados)

# Funcionalidades
- Cadastro de usuários com criptografia de senha
- Login de usuário com JWT (access token + refresh token)
- Criar, listar, atualizar e cancelar pedidos
- Adicionar itens a pedidos
- Atualizar automaticamente estoque de ingredientes e pizzas
- Controle de permissões: usuário comum vs administrador

# Sobre o Projeto
Este projeto foi desenvolvido para facilitar o gerenciamento de pedidos e o controle de estoque de uma pizzaria.
Permite criar pedidos, adicionar itens, atualizar estoque automaticamente e listar pedidos, com controle de acesso para administradores e usuários.

## SCRUM / Histórico de Desenvolvimento

# 1ª Sprint (31/10/25 - 01/11/25)
- Modelo do banco de dados com SQLAlchemy e Alembic –  Finalizado
- Criação de sessão com banco de dados –  Finalizado
- Rota de cadastro de usuário com criptografia de senha –  Finalizado
- Rota de login com autenticação JWT –  Finalizado

# 2ª Sprint (01/11/25 - 02/11/25)
- Rota de refresh token –  Finalizado
- CRUD de produtos com inserção no banco –  Finalizado
- Função que atualiza estoque de ingredientes e pizzas –  Finalizado

# 3ª Sprint (02/11/25 - 03/11/25)
- Rotas de pedidos com atualização de estoque –  Finalizado
- Rotas de visualização e remoção de usuários –  Finalizado

# Projeto finalizado em 03/11/2025

Rotas da API

Auth
POST /auth/create_account ->	Criar nova conta
POST /auth/login	-> Login do usuário
POST /auth/login_force -> Login forçado
POST /auth/refresh_token	-> Atualizar token

Stock (Estoque)
POST /stock/ADD_Ingredients	-> Adicionar ingredientes
POST /stock/ADD_Pizzas   -> Adicionar pizzas
POST /stock/ADD_ing_to_Pizzas -> Adicionar ingredientes às pizzas
PUT /stock/update_ingredient_stock -> Atualizar estoque de ingrediente
DELETE /stock/delete_ingredient	-> Deletar ingrediente
DELETE /stock/delete_ingredient_to_Pizza -> Remover ingrediente de pizza

Users (Usuários)
GET	/users/Users -> Listar usuários
PUT	/users/updateuserinfo -> Atualizar informações do usuário
DELETE	/users/delete_user -> Deletar usuário

Order (Pedidos)
POST	/order/Create_Order	-> Criar pedido
PUT	/order/ADD_items_to_order	-> Adicionar itens ao pedido
PUT	/order/Update_Order	-> Atualizar pedido
GET	/order/View_Orders	-> Ver pedidos
GET	/order/View_Order/{orderid}	-> Ver pedido por ID
GET	/order/View_All_orders	-> Ver todos os pedidos