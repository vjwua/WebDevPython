from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, current_app
from . import enterprises_blueprint
from app import db, bcrypt, jwt
from .models import Enterprise
from app.auth.models import User
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, unset_jwt_cookies
import datetime
basicAuth = HTTPBasicAuth()

@basicAuth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return True
    return False

@basicAuth.error_handler
def unauthorized():
    return jsonify({"message":"Username or password incorrect!"}), 401

@enterprises_blueprint.route('/login', methods=['POST'])
@basicAuth.login_required
def login():
    username = basicAuth.username()
    user = User.query.filter_by(username=username).first()

    if user:
        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({'token': token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'message': 'Token is not created!'}), 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify(
        {"message": "The token has been revoked.",
         "error": "token_revoked"}), 401

@enterprises_blueprint.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'token': new_token})

@enterprises_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response

@enterprises_blueprint.route('/enterprises', methods=['GET'])
def get_all_enterprises():
    enterprises = Enterprise.query.all()
    return_values = [
        {"id": enterprise.id, 
         "name": enterprise.name, 
         "activity_type": enterprise.activity_type,
         "number_of_workers": enterprise.number_of_workers,
         "revenue": enterprise.revenue}
         for enterprise in enterprises]

    return jsonify({'enterprises': return_values})

@enterprises_blueprint.route('/enterprises', methods=['POST'])
@jwt_required()
def post_enterprise():
    new_data = request.get_json()

    if not new_data:
        return jsonify({"message": "No input data provided"}), 400
    
    if not new_data.get("title") or not new_data.get("description"):
        return jsonify({"message": "There's no keys"}), 422 

    enterprise = Enterprise(
        name=new_data.get('name'), 
        activity_type=new_data.get('activity_type'),
        number_of_workers=new_data.get('number_of_workers'),
        revenue=new_data.get('revenue')
    ),
    
    db.session.add(enterprise)
    db.session.commit()

    new_enterprise = Enterprise.query.filter_by(id=enterprise.id).first()
    return jsonify(
        {"id": new_enterprise.id, 
         "name": new_enterprise.name, 
         "activity_type": new_enterprise.activity_type,
         "number_of_workers": new_enterprise.number_of_workers,
         "revenue": new_enterprise.revenue}), 201

@enterprises_blueprint.route('/enterprises/<int:id>', methods=['PUT'])
@jwt_required()
def update_enterprise(id):
    enterprise = Enterprise.query.filter_by(id=id).first()
    
    if not enterprise:
        return jsonify({"message": f"enterprise with id = {id} not found"}), 404
    
    new_data = request.get_json()
    
    if not new_data:
        return jsonify({"message": "no input data provided"}), 400
    
    if new_data.get('name'):
        enterprise.name = new_data.get('name')
    
    if new_data.get('activity_type'):
        enterprise.activity_type = new_data.get('activity_type')

    if new_data.get('number_of_workers'):
        enterprise.number_of_workers = new_data.get('number_of_workers')

    if new_data.get('revenue'):
        enterprise.revenue = new_data.get('revenue')

    try:
        db.session.commit()
        return jsonify({"message": "enterprise was updated"}), 204
    except IntegrityError:
        db.session.rollback()

@enterprises_blueprint.route('/enterprises/<int:id>', methods=['GET'])
def get_enterprise(id):
    enterprise = Enterprise.query.get_or_404(id)
    return jsonify(
        {"id": enterprise.id, 
         "name": enterprise.name, 
         "activity_type": enterprise.activity_type,
         "number_of_workers": enterprise.number_of_workers,
         "revenue": enterprise.revenue})

@enterprises_blueprint.route('/enterprises/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_enterprise(id):
      enterprise = Enterprise.query.get(id)

      if not enterprise:
        return jsonify({"message": f"enterprise with id = {id} not found"}), 404
      
      db.session.delete(enterprise)
      db.session.commit()
      return jsonify({"message" : "Resource successfully deleted."}), 200