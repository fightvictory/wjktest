from flask import Blueprint

admin = Blueprint('admin_p', __name__)

from app.admin import views