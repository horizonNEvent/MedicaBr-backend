from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MedicamentoCreate(BaseModel):
    """Schema para criar um medicamento"""
    nome: str = Field(..., description="Nome do medicamento", min_length=1, max_length=255)
    dosagem: str = Field(..., description="Dosagem (ex: 500mg)", min_length=1, max_length=100)
    frequencia_horas: int = Field(..., description="Frequência em horas (ex: 8)", ge=1)
    estoque_atual: int = Field(default=0, description="Estoque inicial", ge=0)
    estoque_minimo: int = Field(default=5, description="Limite mínimo de alerta", ge=1)
    data_validade: str = Field(..., description="Data de validade (formato: YYYY-MM-DD)")


class MedicamentoUpdate(BaseModel):
    """Schema para atualizar um medicamento"""
    estoque_atual: Optional[int] = Field(None, description="Novo estoque", ge=0)
    estoque_minimo: Optional[int] = Field(None, description="Novo limite mínimo", ge=1)
    data_validade: Optional[str] = Field(None, description="Nova data de validade")


class MedicamentoResponse(BaseModel):
    """Schema de resposta para medicamento"""
    id: int
    nome: str
    dosagem: str
    frequencia_horas: int
    estoque_atual: int
    estoque_minimo: int
    data_validade: str
    data_insercao: str
    em_alerta: bool = False


class MedicamentoListResponse(BaseModel):
    """Schema de resposta para lista de medicamentos"""
    total: int
    medicamentos: list[MedicamentoResponse]
