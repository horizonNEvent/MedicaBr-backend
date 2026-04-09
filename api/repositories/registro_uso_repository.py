from database import db
from model import RegistroUso
from logger import logger


class RegistroUsoRepository:
    """Acesso ao banco de dados para RegistroUso"""

    @staticmethod
    def criar(registro):
        """Insere novo registro de uso"""
        try:
            db.session.add(registro)
            db.session.commit()
            logger.info(f'Registro de uso criado para medicamento_id: {registro.medicamento_id}')
            return registro
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao salvar registro de uso: {str(e)}')
            raise

    @staticmethod
    def listar_todos():
        """Retorna todos os registros de uso ordenados por data decrescente"""
        return RegistroUso.query.order_by(RegistroUso.data_hora.desc()).all()

    @staticmethod
    def buscar_por_medicamento(medicamento_id):
        """Retorna registros de uso de um medicamento específico"""
        return RegistroUso.query.filter_by(medicamento_id=medicamento_id).order_by(
            RegistroUso.data_hora.desc()
        ).all()
