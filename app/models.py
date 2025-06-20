from app import db

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