from flask import jsonify
from app import app
from .models import Profissional

@app.route('/')
def index():
    """Rota inicial apenas para verificar se a API está no ar."""
    return "<h1>API do ConectaServiços no ar!</h1>"

@app.route('/api/v1/profissionais', methods=['GET'])
def get_profissionais():
    """Retorna a lista de todos os profissionais do banco de dados."""
    profissionais_db = Profissional.query.all()
    profissionais_lista = [p.to_dict() for p in profissionais_db]
    return jsonify(profissionais_lista)