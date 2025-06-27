from functools import wraps
from flask import request, jsonify, current_app
import jwt
from .models import Usuario


def token_required(f):
    """
    Decorator que verifica a validade de um token JWT.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'erro': 'Token é obrigatório.'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Usuario.query.get(data['sub'])
            if not current_user:
                return jsonify({'erro': 'Usuário do token não encontrado.'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirou. Faça login novamente.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido.'}), 401

        return f(current_user, *args, **kwargs)

    return decorated