# house_routes.py

from flask import Blueprint

bp = Blueprint('house', __name__, url_prefix='/house')

@bp.route('/')
def index():
    return 'house index page'