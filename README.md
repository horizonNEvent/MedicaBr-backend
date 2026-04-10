# MedicaBr Backend

API RESTful para gerenciar medicamentos pessoais. Permite cadastrar medicamentos, registrar quando foram tomados e receber alertas de estoque baixo.

## Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/horizonNEvent/MedicaBr-backend.git
cd MedicaBr-backend
```

2. **Crie um ambiente virtual (recomendado)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r api/requirements.txt
```

## Como executar

```bash
python api/app.py
```

A API estará disponível em: `http://localhost:5000`

## Documentação

Acesse a documentação interativa em:

**Hub de Documentação (escolha uma opção):**
```
http://localhost:5000/docs
```

**Ou acesse direto:**
- **Swagger** - `http://localhost:5000/swagger` 
- **ReDoc** - `http://localhost:5000/redoc` 
- **OpenAPI JSON** - `http://localhost:5000/openapi.json` 
- **Endpoints JSON** - `http://localhost:5000/`

## Rotas disponíveis

### Medicamentos
- `POST /medicamento` - Cadastrar medicamento
- `GET /medicamentos` - Listar todos os medicamentos
  - Parâmetro opcional: `?nome=dipirona` - Filtra por nome (case-insensitive)
- `GET /medicamento/<id>` - Buscar medicamento por ID
- `DELETE /medicamento/<id>` - Deletar medicamento
- `GET /medicamentos/alertas` - Listar medicamentos com estoque baixo
  - Parâmetro opcional: `?nome=dipirona` - Filtra por nome (case-insensitive)

### Registros de Uso
- `POST /registro_uso` - Registrar que tomou o medicamento
- `GET /historico` - Ver histórico de uso

## Arquitetura

O backend segue um padrão de arquitetura em camadas (Layered Architecture) para melhor separação de responsabilidades:

```
api/
├── routes/              → Endpoints HTTP
├── services/            → Lógica de negócio
├── repositories/        → Acesso ao banco de dados
├── model/               → Modelos SQLAlchemy
├── schemas/             → Validação Pydantic
├── database/            → Configuração SQLite
└── logger.py            → Sistema de logging
```

**Fluxo:** `HTTP Request → Routes → Services → Repositories → Models → Database`

## Estrutura do Banco de Dados

### Tabela: medicamento
```
id                INTEGER (PK)
nome              STRING (UNIQUE)
dosagem           STRING
frequencia_horas  INTEGER
estoque_atual     INTEGER
estoque_minimo    INTEGER
data_validade     DATETIME
data_insercao     DATETIME
```

### Tabela: registro_uso
```
id                INTEGER (PK)
medicamento_id    INTEGER (FK)
data_hora         DATETIME
observacao        STRING
```

## Tecnologias Utilizadas

- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-OpenAPI3** - Documentação automática com Swagger
- **Flask-CORS** - Suporte CORS
- **SQLite** - Banco de dados

## Exemplo de Requisição

### Criar medicamento
```bash
curl -X POST http://localhost:5000/medicamento \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dipirona",
    "dosagem": "500mg",
    "frequencia_horas": 6,
    "estoque_atual": 20,
    "estoque_minimo": 5,
    "data_validade": "2025-12-31"
  }'
```

### Listar medicamentos com filtro
```bash
# Todos os medicamentos
curl http://localhost:5000/medicamentos

# Filtrar por nome
curl http://localhost:5000/medicamentos?nome=dipirona
```

### Listar alertas com filtro
```bash
# Todos os medicamentos em alerta
curl http://localhost:5000/medicamentos/alertas

# Filtrar alertas por nome
curl http://localhost:5000/medicamentos/alertas?nome=para
```

### Registrar uso
```bash
curl -X POST http://localhost:5000/registro_uso \
  -H "Content-Type: application/json" \
  -d '{
    "medicamento_id": 1,
    "observacao": "Tomado com água"
  }'
```

## Suporte

Em caso de dúvidas ou problemas, abra uma issue no repositório.
