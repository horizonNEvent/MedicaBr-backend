from datetime import datetime
from model import Medicamento
from repositories.medicamento_repository import MedicamentoRepository
from logger import logger


class MedicamentoService:
    """Lógica de negócio para Medicamento"""

    @staticmethod
    def criar_medicamento(data):
        """Cria novo medicamento com validações"""

        # Validar se medicamento já existe
        existe = MedicamentoRepository.buscar_por_nome(data.nome)
        if existe:
            logger.warning(f'Tentativa de cadastro duplicado: {data.nome}')
            raise ValueError('Medicamento já cadastrado')

        # Validar e parsear data
        try:
            data_validade = datetime.strptime(data.data_validade, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Formato de data inválido. Use YYYY-MM-DD')

        # Criar novo medicamento
        novo_medicamento = Medicamento(
            nome=data.nome,
            dosagem=data.dosagem,
            frequencia_horas=data.frequencia_horas,
            estoque_atual=data.estoque_atual,
            estoque_minimo=data.estoque_minimo,
            data_validade=data_validade,
        )

        # Salvar no banco
        medicamento_criado = MedicamentoRepository.criar(novo_medicamento)
        logger.info(f'Medicamento cadastrado: {data.nome}')

        return medicamento_criado

    @staticmethod
    def listar_todos():
        """Retorna todos os medicamentos"""
        medicamentos = MedicamentoRepository.listar_todos()
        logger.info(f'Listando {len(medicamentos)} medicamentos')
        return medicamentos

    @staticmethod
    def listar_com_filtro(nome=None):
        """Retorna medicamentos filtrados por nome"""
        medicamentos = MedicamentoRepository.buscar_por_nome_like(nome)
        logger.info(f'Listando {len(medicamentos)} medicamentos com filtro: {nome or "nenhum"}')
        return medicamentos

    @staticmethod
    def buscar_por_id(medicamento_id):
        """Busca medicamento por ID"""
        medicamento = MedicamentoRepository.buscar_por_id(medicamento_id)

        if not medicamento:
            logger.warning(f'Medicamento não encontrado: {medicamento_id}')
            raise ValueError('Medicamento não encontrado')

        logger.info(f'Medicamento encontrado: {medicamento.nome}')
        return medicamento

    @staticmethod
    def deletar_medicamento(medicamento_id):
        """Deleta um medicamento e seus registros"""
        medicamento = MedicamentoRepository.buscar_por_id(medicamento_id)

        if not medicamento:
            logger.warning(f'Tentativa de deletar medicamento inexistente: {medicamento_id}')
            raise ValueError('Medicamento não encontrado')

        nome = medicamento.nome
        MedicamentoRepository.deletar(medicamento)
        logger.info(f'Medicamento deletado: {nome}')

        return nome

    @staticmethod
    def listar_com_alertas(nome=None):
        """Retorna medicamentos com estoque baixo, opcionalmente filtrados por nome"""
        medicamentos = MedicamentoRepository.listar_com_alerta(nome)
        logger.info(f'{len(medicamentos)} medicamentos em alerta de estoque com filtro: {nome or "nenhum"}')
        return medicamentos

    @staticmethod
    def registrar_uso(medicamento_id):
        """Registra uso e decrementa estoque"""
        medicamento = MedicamentoRepository.buscar_por_id(medicamento_id)

        if not medicamento:
            logger.warning(f'Tentativa de registrar uso de medicamento inexistente: {medicamento_id}')
            raise ValueError('Medicamento não encontrado')

        # Decrementa estoque em 1
        medicamento_atualizado = MedicamentoRepository.atualizar_estoque(medicamento, -1)
        logger.info(f'Uso registrado para: {medicamento.nome}')

        return medicamento_atualizado
