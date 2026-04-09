from database import db
from datetime import datetime

class RegistroUso(db.Model):
    __tablename__ = 'registro_uso'

    id = db.Column(db.Integer, primary_key=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)
    observacao = db.Column(db.String(500))

    def __repr__(self):
        return f'<RegistroUso medicamento_id={self.medicamento_id} data_hora={self.data_hora}>'

    def to_dict(self):
        return {
            'id': self.id,
            'medicamento_id': self.medicamento_id,
            'medicamento_nome': self.medicamento.nome if self.medicamento else None,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'observacao': self.observacao,
        }
