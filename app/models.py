from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Profissional(db.Model):
    """
    Representa a tabela de profissionais no banco de dados.
    """
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    profissao = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100))
    estrelas = db.Column(db.Float)
    descricao = db.Column(db.String(255))

    def to_dict(self):
        """
        Converte o objeto Profissional para um dicionário,
        facilitando a conversão para JSON.
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'profissao': self.profissao,
            'cidade': self.cidade,
            'estrelas': self.estrelas,
            'descricao': self.descricao
        }


class Usuario(db.Model):
    """
    Representa a tabela de usuários (clientes e profissionais).
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    nome = db.Column(db.String(100))
    tipo_usuario = db.Column(db.String(50), nullable=False, default='cliente') # ex: 'cliente' ou 'profissional'

    def set_password(self, password):
        """Gera o hash da senha e o armazena."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)
