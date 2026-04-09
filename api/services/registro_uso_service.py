from model import RegistroUso
from repositories.registro_uso_repository import RegistroUsoRepository
from repositories.medicamento_repository import MedicamentoRepository
from logger import logger


class RegistroUsoService:
    """Lógica de negócio para RegistroUso"""

    @staticmethod
    def registrar_uso(data):
        """Registra o uso de um medicamento"""

        # Validar se medicamento existe
        medicamento = MedicamentoRepository.buscar_por_id(data.medicamento_id)
        if not medicamento:
            logger.warning(f'Tentativa de registrar uso de medicamento inexistente: {data.medicamento_id}')
            raise ValueError('Medicamento não encontrado')

        # Criar novo registro
        novo_registro = RegistroUso(
            medicamento_id=data.medicamento_id,
            observacao=data.observacao,
        )

        # Registrar uso no banco
        registro_criado = RegistroUsoRepository.criar(novo_registro)

        # Decrementar estoque do medicamento
        MedicamentoRepository.atualizar_estoque(medicamento, -1)
        logger.info(f'Uso registrado para: {medicamento.nome}')

        return registro_criado

    @staticmethod
    def listar_historico():
        """Retorna histórico completo de uso"""
        registros = RegistroUsoRepository.listar_todos()
        logger.info(f'Listando {len(registros)} registros de uso')
        return registros

    @staticmethod
    def listar_por_medicamento(medicamento_id):
        """Retorna histórico de uso de um medicamento"""
        medicamento = MedicamentoRepository.buscar_por_id(medicamento_id)
        if not medicamento:
            logger.warning(f'Medicamento não encontrado: {medicamento_id}')
            raise ValueError('Medicamento não encontrado')

        registros = RegistroUsoRepository.buscar_por_medicamento(medicamento_id)
        logger.info(f'Listando {len(registros)} registros para {medicamento.nome}')
        return registros
