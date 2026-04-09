from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegistroUsoCreate(BaseModel):
    """Schema para registrar o uso de um medicamento"""
    medicamento_id: int = Field(..., description="ID do medicamento")
    observacao: Optional[str] = Field(None, description="Observação sobre o uso", max_length=500)


class RegistroUsoResponse(BaseModel):
    """Schema de resposta para registro de uso"""
    id: int
    medicamento_id: int
    medicamento_nome: str
    data_hora: str
    observacao: Optional[str]


class RegistroUsoListResponse(BaseModel):
    """Schema de resposta para lista de registros"""
    total: int
    registros: list[RegistroUsoResponse]
