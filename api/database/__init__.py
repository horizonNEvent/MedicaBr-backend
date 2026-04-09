import os
from flask_sqlalchemy import SQLAlchemy

# Caminho do banco de dados SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'medilembr.db')

# Configurar SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        import sys
        from pathlib import Path
        api_path = Path(__file__).parent.parent
        if str(api_path) not in sys.path:
            sys.path.insert(0, str(api_path))

        from model.medicamento import Medicamento
        from model.registro_uso import RegistroUso

        db.create_all()
