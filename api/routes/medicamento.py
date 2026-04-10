from flask_openapi3 import OpenAPI
from flask import request
from schemas import (
    MedicamentoCreate, MedicamentoResponse, MedicamentoListResponse,
    RegistroUsoCreate, RegistroUsoResponse, RegistroUsoListResponse,
)
from services.medicamento_service import MedicamentoService
from logger import logger


def registrar_rotas_medicamento(app: OpenAPI):
    """Registra todas as rotas de medicamento"""

    @app.post('/medicamento', summary='Cadastrar medicamento')
    def criar_medicamento(body: MedicamentoCreate):
        """Cadastra um novo medicamento"""
        try:
            medicamento = MedicamentoService.criar_medicamento(body)
            return medicamento.to_dict(), 201

        except ValueError as e:
            logger.warning(f'Erro de validação: {str(e)}')
            return {
                'status_code': 400,
                'message': str(e),
            }, 400

        except Exception as e:
            logger.error(f'Erro ao criar medicamento: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao cadastrar medicamento',
                'details': str(e),
            }, 500

    @app.get('/medicamentos', summary='Listar medicamentos')
    def listar_medicamentos():
        """Lista todos os medicamentos cadastrados ou filtra por nome"""
        try:
            nome_filtro = request.args.get('nome', default=None)

            if nome_filtro:
                medicamentos = MedicamentoService.listar_com_filtro(nome_filtro)
            else:
                medicamentos = MedicamentoService.listar_todos()

            return {
                'total': len(medicamentos),
                'medicamentos': [med.to_dict() for med in medicamentos],
            }, 200

        except Exception as e:
            logger.error(f'Erro ao listar medicamentos: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao listar medicamentos',
            }, 500

    @app.route('/medicamento/<int:medicamento_id>', methods=['GET'])
    def buscar_medicamento(medicamento_id):
        """Busca um medicamento específico por ID"""
        try:
            medicamento = MedicamentoService.buscar_por_id(medicamento_id)
            return medicamento.to_dict(), 200

        except ValueError as e:
            logger.warning(f'Medicamento não encontrado: {medicamento_id}')
            return {
                'status_code': 404,
                'message': str(e),
            }, 404

        except Exception as e:
            logger.error(f'Erro ao buscar medicamento: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao buscar medicamento',
            }, 500

    @app.route('/medicamento/<int:medicamento_id>', methods=['DELETE'])
    def deletar_medicamento(medicamento_id):
        """Deleta um medicamento e todos seus registros de uso"""
        try:
            nome = MedicamentoService.deletar_medicamento(medicamento_id)
            return {
                'status_code': 200,
                'message': f'Medicamento {nome} deletado com sucesso',
            }, 200

        except ValueError as e:
            logger.warning(f'Erro ao deletar: {str(e)}')
            return {
                'status_code': 404,
                'message': str(e),
            }, 404

        except Exception as e:
            logger.error(f'Erro ao deletar medicamento: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao deletar medicamento',
            }, 500

    @app.get('/medicamentos/alertas', summary='Medicamentos com alerta de estoque')
    def medicamentos_com_alerta():
        """Lista medicamentos com estoque baixo (abaixo do mínimo), opcionalmente filtrado por nome"""
        try:
            nome_filtro = request.args.get('nome', default=None)
            medicamentos = MedicamentoService.listar_com_alertas(nome_filtro)
            em_alerta = [
                {**med.to_dict(), 'em_alerta': True}
                for med in medicamentos
            ]

            return {
                'total': len(em_alerta),
                'medicamentos': em_alerta,
            }, 200

        except Exception as e:
            logger.error(f'Erro ao buscar alertas: {str(e)}')
            return {
                'status_code': 500,
                'message': 'Erro ao buscar alertas',
            }, 500
