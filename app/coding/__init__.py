from flask import Blueprint

bp = Blueprint('coding', __name__)

from app.coding import routes