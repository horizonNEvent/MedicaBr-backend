from database import db
from datetime import datetime

class Medicamento(db.Model):
    __tablename__ = 'medicamento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    dosagem = db.Column(db.String(100), nullable=False)
    frequencia_horas = db.Column(db.Integer, nullable=False)
    estoque_atual = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=5)
    data_validade = db.Column(db.DateTime, nullable=False)
    data_insercao = db.Column(db.DateTime, nullable=False, default=datetime.now)

    registros_uso = db.relationship('RegistroUso', backref='medicamento', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Medicamento {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'dosagem': self.dosagem,
            'frequencia_horas': self.frequencia_horas,
            'estoque_atual': self.estoque_atual,
            'estoque_minimo': self.estoque_minimo,
            'data_validade': self.data_validade.isoformat() if self.data_validade else None,
            'data_insercao': self.data_insercao.isoformat() if self.data_insercao else None,
        }
