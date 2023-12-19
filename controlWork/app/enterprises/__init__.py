from flask import Blueprint

enterprises_blueprint = Blueprint('enterprises_bp', __name__, template_folder="templates/enterprises")

#from . import views