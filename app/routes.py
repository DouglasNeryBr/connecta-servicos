from flask import jsonify
from app import app
from .models import PROFISSIONAIS_DB

@app.route('/')
def index():
    """Rota inicial apenas para verificar se a API está no ar."""
    return "<h1>API do ConectaServiços no ar!</h1>"

@app.route('/api/v1/profissionais', methods=['GET'])
def get_profissionais():
    """Retorna a lista de todos os profissionais."""
    return jsonify(PROFISSIONAIS_DB)