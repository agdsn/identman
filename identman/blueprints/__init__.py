from flask import render_template, Blueprint, request, redirect, jsonify

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def index():
    if not request.args.get('query'):
        return jsonify(), 404
    else:
        return jsonify({"query": request.args.get('query')})


@bp.route('/challenge/<content>')
def challenge(content: str):
    return
