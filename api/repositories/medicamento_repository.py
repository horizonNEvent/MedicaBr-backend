from database import db
from model import Medicamento
from logger import logger


class MedicamentoRepository:
    """Acesso ao banco de dados para Medicamento"""

    @staticmethod
    def criar(medicamento):
        """Insere novo medicamento no banco"""
        try:
            db.session.add(medicamento)
            db.session.commit()
            logger.info(f'Medicamento salvo no banco: {medicamento.nome}')
            return medicamento
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao salvar medicamento: {str(e)}')
            raise

    @staticmethod
    def buscar_por_nome(nome):
        """Busca medicamento por nome"""
        return Medicamento.query.filter_by(nome=nome).first()

    @staticmethod
    def buscar_por_id(medicamento_id):
        """Busca medicamento por ID"""
        return Medicamento.query.get(medicamento_id)

    @staticmethod
    def listar_todos():
        """Retorna todos os medicamentos"""
        return Medicamento.query.all()

    @staticmethod
    def listar_com_alerta():
        """Retorna medicamentos com estoque baixo"""
        return Medicamento.query.filter(
            Medicamento.estoque_atual <= Medicamento.estoque_minimo
        ).all()

    @staticmethod
    def deletar(medicamento):
        """Deleta um medicamento"""
        try:
            db.session.delete(medicamento)
            db.session.commit()
            logger.info(f'Medicamento deletado: {medicamento.nome}')
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao deletar medicamento: {str(e)}')
            raise

    @staticmethod
    def atualizar_estoque(medicamento, quantidade):
        """Atualiza estoque do medicamento"""
        try:
            medicamento.estoque_atual += quantidade
            db.session.commit()
            logger.info(f'Estoque atualizado para {medicamento.nome}: {medicamento.estoque_atual}')
            return medicamento
        except Exception as e:
            db.session.rollback()
            logger.error(f'Erro ao atualizar estoque: {str(e)}')
            raise
