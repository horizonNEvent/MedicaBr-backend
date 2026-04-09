from flask_openapi3 import OpenAPI
from schemas import RegistroUsoCreate
from services.registro_uso_service import RegistroUsoService
from logger import logger


def registrar_rotas_registro_uso(app: OpenAPI):
    """Registra todas as rotas de registro de uso"""

    @app.post('/registro_uso', summary='Registrar uso de medicamento')
    def registrar_uso(body: RegistroUsoCreate):
        """Registra que um medicamento foi tomado"""
        try:
            registro = RegistroUsoService.registrar_uso(body)
            return registro.to_dict(), 201

        except ValueError as e:
            logger.warning(f'Erro de validação: {str(e)}')
            return {
                'status_code': 404,
                'message': str(e),
            }, 404

        except Exception as e:
            logger.error(f'Erro ao registrar uso: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao registrar uso',
            }, 500

    @app.get('/historico', summary='Histórico de uso')
    def historico_uso():
        """Lista os últimos registros de uso de todos os medicamentos"""
        try:
            registros = RegistroUsoService.listar_historico()

            return {
                'total': len(registros),
                'registros': [reg.to_dict() for reg in registros],
            }, 200

        except Exception as e:
            logger.error(f'Erro ao listar histórico: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao listar histórico',
            }, 500
