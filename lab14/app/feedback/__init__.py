from flask import Blueprint

feedback_blueprint = Blueprint('feedback_bp', __name__, template_folder="templates/feedback")

from . import views