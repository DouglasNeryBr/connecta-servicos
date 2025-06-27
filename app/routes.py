import jwt
from flask import jsonify, request
from app import app, db
from .models import Profissional, Usuario
from datetime import datetime, timedelta, timezone
from .decorators import token_required


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
    else: # GET
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

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """
    Registra um novo usuário no sistema.
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'erro': 'Email e senha são obrigatórios.'}), 400

    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado.'}), 409

    novo_usuario = Usuario(
        email=data['email'],
        nome=data.get('nome'),
        tipo_usuario=data.get('tipo_usuario', 'cliente')
    )
    novo_usuario.set_password(data['password'])

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """
    Autentica um usuário e retorna um token JWT.
    """
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'erro': 'Email e senha são obrigatórios.'}), 401

    user = Usuario.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'erro': 'Email ou senha inválidos.'}), 401

    payload = {
        'sub': user.id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token})


@app.route('/api/v1/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """
    Rota protegida que retorna os dados do usuário logado.
    O decorator 'token_required' garante que só usuários autenticados cheguem aqui.
    """
    user_data = {
        'id': current_user.id,
        'nome': current_user.nome,
        'email': current_user.email,
        'tipo_usuario': current_user.tipo_usuario
    }
    return jsonify(user_data)
