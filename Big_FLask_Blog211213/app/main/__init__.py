from flask import Blueprint


main = Blueprint('main', __name__)

from app.main import views, errors
from app.models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
