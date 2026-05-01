# flaskweb-mongodb

API REST simples em Flask que utiliza MongoDB como banco de dados. Este projeto fornece endpoints para gerenciamento de usuários e clientes, com autenticação baseada em JWT para operações protegidas.

## Sumário
- Visão geral
- Requisitos
- Instalação
- Configuração (variáveis de ambiente)
- Executando a aplicação
- Endpoints principais
- Exemplos (curl)
- Estrutura do projeto
- Observações importantes
- Como contribuir

## Visão geral
- A aplicação cria a instância do Flask em `create_app()` (arquivo `app/__init__.py`) e conecta ao MongoDB usando `pymongo`.
- Autenticação JWT é gerada em `POST /login` e verificada pelo decorator `token_obrigatorio` (arquivo `app/decorators.py`).
- Modelos de validação/schemas usam `pydantic` (arquivos em `app/models/`).
- Rotas estão em `app/routes/` (clientes e usuários).

## Requisitos
- Python (versão compatível com os pacotes listados em `requiriments.txt`)
- MongoDB acessível pela URI configurada em `MONGO_URI`
- Dependências estão no arquivo `requiriments.txt`. Para instalar:

```flaskweb-mongodb/requiriments.txt#L1-20
annotated-types==0.7.0
blinker==1.9.0
click==8.3.3
dnspython==2.8.0
Flask==3.1.3
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
pydantic==2.13.3
pydantic_core==2.46.3
PyJWT==2.12.1
pymongo==4.17.0
python-dotenv==1.2.2
typing-inspection==0.4.2
typing_extensions==4.15.0
Werkzeug==3.1.8
```

## Instalação
1. Crie e ative um virtualenv:
```/dev/null/venv-setup.sh#L1-6
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\\Scripts\\Activate.ps1
```

2. Instale dependências:
```/dev/null/install.sh#L1-3
pip install -r requiriments.txt
```

## Configuração (variáveis de ambiente)
- O projeto utiliza `python-dotenv` e espera as variáveis no arquivo `.env` (ou no ambiente):
  - `MONGO_URI` — URI de conexão com o MongoDB (ex.: `mongodb+srv://user:pass@cluster0.mongodb.net/meudb?retryWrites=true&w=majority`)
  - `SECRET_KEY` — chave secreta usada para assinatura dos tokens JWT e para autenticação do usuário `admin`

Exemplo de `.env` (só para referência — NÃO colocar segredos em repositórios públicos):
```flaskweb-mongodb/.env#L1-3
MONGO_URI=mongodb+srv://<usuario>:<senha>@<cluster>/<database>?retryWrites=true&w=majority
SECRET_KEY=uma_chave_secreta
```

## Executando a aplicação
- A aplicação pode ser iniciada diretamente com `python run.py`. O arquivo de entrada é `run.py`:
```flaskweb-mongodb/run.py#L1-5
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

- Ou executar com um runner WSGI conforme sua preferência (gunicorn, etc.).

## Endpoints principais
- Autenticação
  - POST /login
    - Descrição: recebe JSON com `nome` e `senha`. Se `nome == "admin"` e `senha == SECRET_KEY`, retorna um token JWT válido por 2 horas.
    - Corpo de exemplo:
      ```/dev/null/login-example.json#L1-4
      {
        "nome": "admin",
        "senha": "SUA_SECRET_KEY"
      }
      ```
    - Resposta:
      - 200: `{ "token de acesso": "<JWT>" }`
      - 401: credenciais inválidas
      - 400/500: erros de validação/servidor

- Clientes
  - GET /clientes
    - Lista todos os clientes (retorna array de documentos).
    - Observação: implementação atual busca `db.clientes.find({})`.
  - GET /clientes/<cliente_id>
    - Recupera um cliente por `_id` (ObjectId).
  - POST /clientes
    - Cria um cliente. Requer header `Authorization: Bearer <token>`.
    - Corpo: JSON com campos do modelo `Cliente` (`nome`, `telefone`, `endereco`, `saldo`, `email` opcional).
  - PUT /clientes/<cliente_id>
    - Atualiza campos do cliente. Requer `Authorization`.
  - DELETE /clientes/<cliente_id>
    - Deleta cliente. Requer `Authorization`.

- Usuários
  - GET /usuarios
    - Lista usuários (campo `senha` é excluído do retorno).
  - GET /usuarios/<usuario_id>
    - Retorna usuário específico (sem `senha`).
  - POST /usuarios
    - Cria um novo usuário (recebe `nome` e `senha`).
  - DELETE /usuarios/<usuario_id>
    - Deleta usuário.

## Autenticação (como usar)
- Para endpoints protegidos (criar/atualizar/deletar clientes), envie o header:
  - `Authorization: Bearer <token>`
- Exemplo de obtenção do token e uso nas requisições abaixo.

## Exemplos com curl
- Obter token:
```/dev/null/curl_examples.sh#L1-6
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"nome":"admin","senha":"SUA_SECRET_KEY"}'
```

- Criar cliente (usando token):
```/dev/null/curl_examples.sh#L7-18
curl -X POST http://localhost:5000/clientes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SEU_TOKEN>" \
  -d '{
        "nome": "João Silva",
        "telefone": "1199999-9999",
        "endereco": "Rua Exemplo, 123",
        "saldo": 100.50,
        "email": "joao@example.com"
      }'
```

## Estrutura do projeto
- `flaskweb-mongodb/`
  - `app/`
    - `__init__.py` — cria app e conecta ao MongoDB
    - `decorators.py` — `token_obrigatorio` (verifica JWT)
    - `models/` — Pydantic models: `usuarios.py`, `clientes.py`, `compras.py`
    - `routes/` — rotas: `main.py` (clientes, login, rota raiz) e `usuario_routes.py`
  - `config.py` — lê variáveis de ambiente (`MONGO_URI`, `SECRET_KEY`)
  - `run.py` — arquivo de execução
  - `requiriments.txt` — dependências
  - `.env` — variáveis privadas (não versionar)

## Observações importantes
- A autenticação do endpoint `/login` usa a combinação exata `nome == "admin"` e `senha == SECRET_KEY`. Ajuste conforme necessário para um sistema com usuários persistidos e senhas hashed.
- A função de listagem em `main.py` (`/clientes`) possui dois laços sobre o mesmo cursor (`todos_clientes`) e pode consumir o cursor antes do segundo loop; verificar e ajustar se necessário.
- Certifique-se de que `MONGO_URI` aponte para o banco correto e que o usuário tenha permissões apropriadas.
- O arquivo `.env` pode estar presente localmente — evite commitar segredos.

## Como contribuir
- Abra issue descrevendo a melhoria/bug.
- Faça fork, crie branch com alterações e envie um pull request.
- Sugestões desejáveis: autenticação com usuários no banco, hashing de senhas, tratamento de erros consistente, testes automatizados.

## Licença
- Adicione a licença desejada (arquivo `LICENSE`) conforme sua preferência.

---

Se quiser, eu posso:
- Gerar um README.md alternativo (curto/longa) ou traduzir partes.
- Corrigir e melhorar pontos do código do projeto (por exemplo, consertar a listagem em `/clientes`).
Diga o que prefere que eu faça em seguida.
