from flask import render_template_string
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from database import db, init_db
from logger import logger
from routes.medicamento import registrar_rotas_medicamento
from routes.registro_uso import registrar_rotas_registro_uso

app = OpenAPI(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)

init_db(app)

registrar_rotas_medicamento(app)
registrar_rotas_registro_uso(app)


@app.get('/', summary='Health Check')
def health_check():
    """Verifica se a API está funcionando"""
    return {
        'status': 'API MediLembr rodando',
        'version': '1.0.0',
        'endpoints': {
            'Medicamentos': {
                'POST /medicamento': 'Criar medicamento',
                'GET /medicamentos': 'Listar todos',
                'GET /medicamento/<id>': 'Buscar por ID',
                'DELETE /medicamento/<id>': 'Deletar',
                'GET /medicamentos/alertas': 'Listar com alerta'
            },
            'Registros': {
                'POST /registro_uso': 'Registrar uso',
                'GET /historico': 'Ver histórico'
            }
        }
    }, 200


@app.errorhandler(404)
def not_found(error):
    logger.warning('Rota não encontrada')
    return {
        'status_code': 404,
        'message': 'Rota não encontrada',
    }, 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Erro interno: {str(error)}')
    return {
        'status_code': 500,
        'message': 'Erro interno do servidor',
    }, 500


@app.get('/swagger')
def swagger_docs():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediLembr API - Swagger</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css">
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.get('/docs')
def docs_hub():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediLembr API - Documentação</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 12px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
                text-align: center;
            }
            .subtitle {
                color: #666;
                text-align: center;
                margin-bottom: 40px;
            }
            .docs-grid {
                display: grid;
                gap: 15px;
            }
            .doc-card {
                padding: 20px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-decoration: none;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .doc-card:hover {
                border-color: #667eea;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
                transform: translateY(-2px);
            }
            .doc-card h3 {
                color: #667eea;
                margin-bottom: 8px;
            }
            .doc-card p {
                color: #666;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MediLembr API</h1>
            <p class="subtitle">Escolha uma forma de acessar a documentação</p>

            <div class="docs-grid">
                <a href="/swagger" class="doc-card">
                    <h3>Swagger</h3>
                    <p>Documentação interativa padrão da indústria. Teste endpoints direto.</p>
                </a>

                <a href="/redoc" class="doc-card">
                    <h3>ReDoc</h3>
                    <p>Documentação interativa e moderna. Interface limpa e fácil de usar.</p>
                </a>

                <a href="/openapi.json" class="doc-card">
                    <h3>OpenAPI JSON</h3>
                    <p>Especificação OpenAPI em formato JSON. Para ferramentas e integrações.</p>
                </a>

                <a href="/" class="doc-card">
                    <h3>Endpoints JSON</h3>
                    <p>Lista simples de todos os endpoints disponíveis em formato JSON.</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.get('/redoc')
def redoc_docs():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediLembr API - ReDoc</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <redoc spec-url="/openapi.json"></redoc>
        <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.get('/openapi.json')
def openapi_spec():
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "MediLembr API",
            "description": "API RESTful para gerenciar medicamentos pessoais",
            "version": "1.0.0"
        },
        "servers": [{"url": "http://localhost:5000"}],
        "paths": {
            "/medicamento": {
                "post": {
                    "summary": "Criar medicamento",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "nome": {"type": "string"},
                                        "dosagem": {"type": "string"},
                                        "frequencia_horas": {"type": "integer"},
                                        "estoque_atual": {"type": "integer"},
                                        "estoque_minimo": {"type": "integer"},
                                        "data_validade": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {"201": {"description": "Medicamento criado"}}
                }
            },
            "/medicamentos": {
                "get": {
                    "summary": "Listar medicamentos",
                    "responses": {"200": {"description": "Lista de medicamentos"}}
                }
            },
            "/medicamento/{id}": {
                "get": {
                    "summary": "Buscar medicamento por ID",
                    "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                    "responses": {"200": {"description": "Medicamento encontrado"}}
                },
                "delete": {
                    "summary": "Deletar medicamento",
                    "parameters": [{"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}],
                    "responses": {"200": {"description": "Medicamento deletado"}}
                }
            },
            "/medicamentos/alertas": {
                "get": {
                    "summary": "Listar medicamentos com alerta",
                    "responses": {"200": {"description": "Medicamentos em alerta"}}
                }
            },
            "/registro_uso": {
                "post": {
                    "summary": "Registrar uso de medicamento",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "medicamento_id": {"type": "integer"},
                                        "observacao": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {"201": {"description": "Uso registrado"}}
                }
            },
            "/historico": {
                "get": {
                    "summary": "Listar histórico de uso",
                    "responses": {"200": {"description": "Histórico de uso"}}
                }
            }
        }
    }
    return spec


if __name__ == '__main__':
    logger.info('Iniciando MediLembr API...')
    app.run(debug=True, host='localhost', port=5000)
