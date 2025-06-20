from flask import jsonify, request
from app import app, db
from .models import Profissional


@app.route('/')
def index():
    """Rota inicial apenas para verificar se a API está no ar."""
    return "<h1>API do ConectaServiços no ar!</h1>"


@app.route('/api/v1/profissionais', methods=['GET', 'POST'])
def handle_profissionais():
    """
    Manipula requisições GET para listar e POST para criar profissionais.
    """
    if request.method == 'POST':
        data = request.get_json()

        if not data or not data.get('nome') or not data.get('profissao'):
            return jsonify({'erro': 'Dados insuficientes. Nome e profissão são obrigatórios.'}), 400

        novo_profissional = Profissional(
            nome=data['nome'],
            profissao=data['profissao'],
            cidade=data.get('cidade'),
            estrelas=data.get('estrelas'),
            descricao=data.get('descricao')
        )

        db.session.add(novo_profissional)
        db.session.commit()

        return jsonify(novo_profissional.to_dict()), 201

    else:  # GET
        profissionais_db = Profissional.query.all()
        profissionais_lista = [p.to_dict() for p in profissionais_db]
        return jsonify(profissionais_lista)


@app.route('/api/v1/profissionais/<int:id>', methods=['GET'])
def get_profissional_by_id(id):
    """
    Retorna os detalhes de um profissional específico buscando pelo seu ID.
    """
    profissional = Profissional.query.get_or_404(id)
    return jsonify(profissional.to_dict())


@app.route('/api/v1/profissionais/<int:id>', methods=['PUT'])
def update_profissional(id):
    """
    Atualiza os dados de um profissional existente.
    """
    profissional = Profissional.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({'erro': 'Requisição sem dados.'}), 400

    profissional.nome = data.get('nome', profissional.nome)
    profissional.profissao = data.get('profissao', profissional.profissao)
    profissional.cidade = data.get('cidade', profissional.cidade)
    profissional.estrelas = data.get('estrelas', profissional.estrelas)
    profissional.descricao = data.get('descricao', profissional.descricao)

    db.session.commit()

    return jsonify(profissional.to_dict())


@app.route('/api/v1/profissionais/<int:id>', methods=['DELETE'])
def delete_profissional(id):
    """
    Deleta um profissional do banco de dados.
    """
    profissional = Profissional.query.get_or_404(id)
    db.session.delete(profissional)
    db.session.commit()
    return jsonify({'mensagem': f'Profissional com id {id} deletado com sucesso.'})
