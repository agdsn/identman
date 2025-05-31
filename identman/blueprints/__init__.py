from flask import render_template, Blueprint, request, redirect, jsonify, current_app
from identman.identman.helpers import Query
from identman.identman.csrf import get_token, get_token_csrf
from identman.identman.decryption import decrypt
import threading

bp = Blueprint('api', __name__, url_prefix='/api')


sem = threading.Semaphore(5)

@bp.route('')
def index():
    if not request.args.get('query'):
        return jsonify()
    else:
        token = get_token()
        return jsonify({"query": request.args.get('query'), "nHash": token._n, "csrfToken": token._csrf_token})


@bp.route('/challenge', methods=["POST"])
def challenge():
    request_data = request.get_json()
    query = Query(**request_data)



    if not query.validate():
        return jsonify(), 416
    try:
        plain = decrypt(b"Hallo", query.get_query())
    except:
        return jsonify(), 400



    return
