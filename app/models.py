from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    permissions = db.relationship('Permission', secondary='role_permissions', backref=db.backref('roles', lazy='dynamic'))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)

class PoseEstimationService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    api_endpoint = db.Column(db.String(255), nullable=False)
    config_path = db.Column(db.String(255), nullable=False)
    weights_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ActionRecognitionService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    api_endpoint = db.Column(db.String(255), nullable=False)
    config_path = db.Column(db.String(255), nullable=False)
    weights_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class NLPQueryService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False)
    api_endpoint = db.Column(db.String(255), nullable=False)
    config_path = db.Column(db.String(255), nullable=False)
    weights_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.String(255), db.ForeignKey('pose_estimation_service.id'), nullable=False)
    pose_estimation_service_id = db.Column(db.Integer, db.ForeignKey('pose_estimation_service.id'), nullable=False)
    action_recognition_service_id = db.Column(db.Integer, db.ForeignKey('action_recognition_service.id'), nullable=False)
    nlp_query_service_id = db.Column(db.Integer, db.ForeignKey('nlp_query_service.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class PoseEstimationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False)
    keypoints_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class ActionRecognitionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable=False)
    result_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())