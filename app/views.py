from flask import Blueprint, render_template, redirect, url_for, requestfrom
import db, videosfrom .forms 
import ExperimentFormfrom .models 
import Experiment, PoseEstimationData, ActionRecognitionData, PoseEstimationService, ActionRecognitionService, NLPQueryServiceimport, requests, User, Role, Permission
import jsonify
import os
import request
import tempfile

bp = Blueprint('main', __name__)

# User routes
@bp.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        data = request.json
        user = User(username=data['username'], email=data['email'], role_id=data['role_id'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(id):
    user = User.query.get(id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        data = request.json
        user.username = data['username']
        user.email = data['email']
        user.role_id = data['role_id']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

# Role routes
@bp.route('/roles', methods=['GET', 'POST'])
def manage_roles():
    if request.method == 'POST':
        data = request.json
        role = Role(name=data['name'])
        db.session.add(role)
        db.session.commit()
        return jsonify({"message": "Role created successfully"}), 201
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles])

@bp.route('/roles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_role(id):
    role = Role.query.get(id)
    if request.method == 'GET':
        return jsonify(role.to_dict())
    elif request.method == 'PUT':
        data = request.json
        role.name = data['name']
        db.session.commit()
        return jsonify({"message": "Role updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(role)
        db.session.commit()
        return jsonify({"message": "Role deleted successfully"})

# Permission routes
@bp.route('/permissions', methods=['GET', 'POST'])
def manage_permissions():
    if request.method == 'POST':
        data = request.json
        permission = Permission(name=data['name'])
        db.session.add(permission)
        db.session.commit()
        return jsonify({"message": "Permission created successfully"}), 201
    permissions = Permission.query.all()
    return jsonify([permission.to_dict() for permission in permissions])

@bp.route('/permissions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_permission(id):
    permission = Permission.query.get(id)
    if request.method == 'GET':
        return jsonify(permission.to_dict())
    elif request.method == 'PUT':
        data = request.json
        permission.name = data['name']
        db.session.commit()
        return jsonify({"message": "Permission updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(permission)
        db.session.commit()
        return jsonify({"message": "Permission deleted successfully"})

# PoseEstimationService routes
@bp.route('/pose_estimation_services', methods=['GET', 'POST'])
def manage_pose_estimation_services():
    if request.method == 'POST':
        data = request.json
        service = PoseEstimationService(
            service_name=data['service_name'],
            api_endpoint=data['api_endpoint'],
            config_path=data['config_path'],
            weights_path=data['weights_path']
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({"message": "PoseEstimationService created successfully"}), 201
    services = PoseEstimationService.query.all()
    return jsonify([service.to_dict() for service in services])

@bp.route('/pose_estimation_services/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_pose_estimation_service(id):
    service = PoseEstimationService.query.get(id)
    if request.method == 'GET':
        return jsonify(service.to_dict())
    elif request.method == 'PUT':
        data = request.json
        service.service_name = data['service_name']
        service.api_endpoint = data['api_endpoint']
        service.config_path = data['config_path']
        service.weights_path = data['weights_path']
        db.session.commit()
        return jsonify({"message": "PoseEstimationService updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "PoseEstimationService deleted successfully"})

# ActionRecognitionService routes
@bp.route('/action_recognition_services', methods=['GET', 'POST'])
def manage_action_recognition_services():
    if request.method == 'POST':
        data = request.json
        service = ActionRecognitionService(
            service_name=data['service_name'],
            api_endpoint=data['api_endpoint'],
            config_path=data['config_path'],
            weights_path=data['weights_path']
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({"message": "ActionRecognitionService created successfully"}), 201
    services = ActionRecognitionService.query.all()
    return jsonify([service.to_dict() for service in services])

@bp.route('/action_recognition_services/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_action_recognition_service(id):
    service = ActionRecognitionService.query.get(id)
    if request.method == 'GET':
        return jsonify(service.to_dict())
    elif request.method == 'PUT':
        data = request.json
        service.service_name = data['service_name']
        service.api_endpoint = data['api_endpoint']
        service.config_path = data['config_path']
        service.weights_path = data['weights_path']
        db.session.commit()
        return jsonify({"message": "ActionRecognitionService updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "ActionRecognitionService deleted successfully"})

# NLPQueryService routes
@bp.route('/nlp_query_services', methods=['GET', 'POST'])
def manage_nlp_query_services():
    if request.method == 'POST':
        data = request.json
        service = NLPQueryService(
            service_name=data['service_name'],
            api_endpoint=data['api_endpoint'],
            config_path=data['config_path'],
            weights_path=data['weights_path']
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({"message": "NLPQueryService created successfully"}), 201
    services = NLPQueryService.query.all()
    return jsonify([service.to_dict() for service in services])

@bp.route('/nlp_query_services/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_nlp_query_service(id):
    service = NLPQueryService.query.get(id)
    if request.method == 'GET':
        return jsonify(service.to_dict())
    elif request.method == 'PUT':
        data = request.json
        service.service_name = data['service_name']
        service.api_endpoint = data['api_endpoint']
        service.config_path = data['config_path']
        service.weights_path = data['weights_path']
        db.session.commit()
        return jsonify({"message": "NLPQueryService updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "NLPQueryService deleted successfully"})

# Experiment routes
# @bp.route('/experiments', methods=['GET', 'POST'])
# def manage_experiments():
#     if request.method == 'POST':
#         data = request.json
#         experiment = Experiment(
#             experiment_name=data['experiment_name'],
#             description=data['description'],
#             video_filename=data['video_filename'],
#             pose_estimation_service_id=data['pose_estimation_service_id'],
#             action_recognition_service_id=data['action_recognition_service_id'],
#             nlp_query_service_id=data['nlp_query_service_id']
#         )
#         db.session.add(experiment)
#         db.session.commit()
#         return jsonify({"message": "Experiment created successfully"}), 201
#     experiments = Experiment.query.all()
#     return jsonify([experiment.to_dict() for experiment in experiments])

@bp.route('/experiments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_experiment(id):
    experiment = Experiment.query.get(id)
    if request.method == 'GET':
        return jsonify(experiment.to_dict())
    elif request.method == 'PUT':
        data = request.json
        experiment.experiment_name = data['experiment_name']
        experiment.description = data['description']
        experiment.video_filename = data['video_filename']
        experiment.pose_estimation_service_id = data['pose_estimation_service_id']
        experiment.action_recognition_service_id = data['action_recognition_service_id']
        experiment.nlp_query_service_id = data['nlp_query_service_id']
        db.session.commit()
        return jsonify({"message": "Experiment updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(experiment)
        db.session.commit()
        return jsonify({"message": "Experiment deleted successfully"})

# PoseEstimationData routes
@bp.route('/pose_estimation_data', methods=['GET', 'POST'])
def manage_pose_estimation_data():
    if request.method == 'POST':
        data = request.json
        pose_data = PoseEstimationData(
            experiment_id=data['experiment_id'],
            keypoints_data=data['keypoints_data']
        )
        db.session.add(pose_data)
        db.session.commit()
        return jsonify({"message": "PoseEstimationData created successfully"}), 201
    pose_data_list = PoseEstimationData.query.all()
    return jsonify([pose_data.to_dict() for pose_data in pose_data_list])

@bp.route('/pose_estimation_data/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_pose_estimation_data_item(id):
    pose_data = PoseEstimationData.query.get(id)
    if request.method == 'GET':
        return jsonify(pose_data.to_dict())
    elif request.method == 'PUT':
        data = request.json
        pose_data.experiment_id = data['experiment_id']
        pose_data.keypoints_data = data['keypoints_data']
        db.session.commit()
        return jsonify({"message": "PoseEstimationData updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(pose_data)
        db.session.commit()
        return jsonify({"message": "PoseEstimationData deleted successfully"})

# ActionRecognitionData routes
@bp.route('/action_recognition_data', methods=['GET', 'POST'])
def manage_action_recognition_data():
    if request.method == 'POST':
        data = request.json
        action_data = ActionRecognitionData(
            experiment_id=data['experiment_id'],
            result_data=data['result_data']
        )
        db.session.add(action_data)
        db.session.commit()
        return jsonify({"message": "ActionRecognitionData created successfully"}), 201
    action_data_list = ActionRecognitionData.query.all()
    return jsonify([action_data.to_dict() for action_data in action_data_list])

@bp.route('/action_recognition_data/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_action_recognition_data_item(id):
    action_data = ActionRecognitionData.query.get(id)
    if request.method == 'GET':
        return jsonify(action_data.to_dict())
    elif request.method == 'PUT':
        data = request.json
        action_data.experiment_id = data['experiment_id']
        action_data.result_data = data['result_data']
        db.session.commit()
        return jsonify({"message": "ActionRecognitionData updated successfully"})
    elif request.method == 'DELETE':
        db.session.delete(action_data)
        db.session.commit()
        return jsonify({"message": "ActionRecognitionData deleted successfully"})

@bp.route('/experiment/new', methods=['GET', 'POST'])
def create_experiment():
    form = ExperimentForm()
    if form.validate_on_submit():
        video_file = videos.save(form.video_file.data)
        experiment = Experiment(
            experiment_name=form.experiment_name.data,
            description=form.description.data,
            video_filename=video_file,
            pose_estimation_service_id=form.pose_estimation_service.data,
            action_recognition_service_id=form.action_recognition_service.data,
            nlp_query_service_id=form.nlp_query_service.data
        )
        db.session.add(experiment)
        db.session.commit()
        
        pose_service = PoseEstimationService.query.get(form.pose_estimation_service.data)
        action_service = ActionRecognitionService.query.get(form.action_recognition_service.data)
        
        with open(videos.path(video_file), 'rb') as video:
            response = requests.post(pose_service.api_endpoint, files={'video': video})
            if response.status_code == 200:
                keypoints_data = response.json()
                pose_data = PoseEstimationData(experiment_id=experiment.id, keypoints_data=keypoints_data)
                db.session.add(pose_data)
                db.session.commit()
                
                response = requests.post(action_service.api_endpoint, json={'keypoints_data': keypoints_data})
                if response.status_code == 200:
                    result_data = response.json()
                    action_data = ActionRecognitionData(experiment_id=experiment.id, result_data=result_data)
                    db.session.add(action_data)
                    db.session.commit()
                    
        return redirect(url_for('main.experiment_detail', experiment_id=experiment.id))
    
    return render_template('create_experiment.html', form=form)

@bp.route('/experiment/<int:experiment_id>')
def experiment_detail(experiment_id):
    experiment = Experiment.query.get_or_404(experiment_id)
    pose_data = PoseEstimationData.query.filter_by(experiment_id=experiment.id).first()
    action_data = ActionRecognitionData.query.filter_by(experiment_id=experiment.id).first()
    return render_template('experiment_detail.html', experiment=experiment, pose_data=pose_data, action_data=action_data)

@bp.route('/pose_estimation_services_all', methods=['GET'])
def get_pose_estimation_services_all():
    services = PoseEstimationService.query.all()
    return jsonify([service.as_dict() for service in services])

@bp.route('/action_recognition_services_all', methods=['GET'])
def get_action_recognition_services_all():
    services = ActionRecognitionService.query.all()
    return jsonify([service.as_dict() for service in services])

@bp.route('/nlp_query_services_all', methods=['GET'])
def get_nlp_query_services_all():
    services = NLPQueryService.query.all()
    return jsonify([service.as_dict() for service in services])

@bp.route('/experiments', methods=['POST'])
def create_experiment():
    data = request.form
    video_file = request.files['video_file']

    video_path = os.path.join('uploads', video_file.filename)
    video_file.save(video_path)

    new_experiment = Experiment(
        experiment_name=data['experiment_name'],
        description=data['description'],
        video_filename=video_path,
        user_id=data['user_id'],
        pose_estimation_service_id=data['pose_estimation_service_id'],
        action_recognition_service_id=data['action_recognition_service_id'],
        nlp_query_service_id=data['nlp_query_service_id']
    )
    db.session.add(new_experiment)
    db.session.commit()

    pose_service = PoseEstimationService.query.get(data['pose_estimation_service_id'])
    pose_response = requests.post(pose_service.api_endpoint, files={'video': open(video_path, 'rb')}, data={
        'config_path': pose_service.config_path,
        'weights_path': pose_service.weights_path
    })
    pose_data = pose_response.json()

    pose_estimation_data = PoseEstimationData(
        experiment_id=new_experiment.id,
        keypoints_data=pose_data['keypoints']
    )
    db.session.add(pose_estimation_data)
    db.session.commit()

    action_service = ActionRecognitionService.query.get(data['action_recognition_service_id'])
    action_response = requests.post(action_service.api_endpoint, json={
        'keypoints_data': pose_data['keypoints'],
        'config_path': action_service.config_path,
        'weights_path': action_service.weights_path
    })
    action_data = action_response.json()

    action_recognition_data = ActionRecognitionData(
        experiment_id=new_experiment.id,
        result_data=action_data['results']
    )
    db.session.add(action_recognition_data)
    db.session.commit()

    return jsonify({'message': 'Experiment created successfully'}), 201

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'roles': [role.name for role in user.roles]} for user in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    for role_id in data['role_ids']:
        role = Role.query.get(role_id)
        if role:
            new_user.roles.append(role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = data['username']
    user.email = data['email']
    if 'password' in data:
        user.set_password(data['password'])
    user.roles = []
    for role_id in data['role_ids']:
        role = Role.query.get(role_id)
        if role:
            user.roles.append(role)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@bp.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    return jsonify([{'id': role.id, 'name': role.name, 'permissions': [perm.name for perm in role.permissions]} for role in roles])

@bp.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    new_role = Role(name=data['name'])
    for perm_id in data['permission_ids']:
        perm = Permission.query.get(perm_id)
        if perm:
            new_role.permissions.append(perm)
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'message': 'Role created successfully'}), 201

@bp.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.json
    role = Role.query.get(id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    role.name = data['name']
    role.permissions = []
    for perm_id in data['permission_ids']:
        perm = Permission.query.get(perm_id)
        if perm:
            role.permissions.append(perm)
    db.session.commit()
    return jsonify({'message': 'Role updated successfully'})

@bp.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'})

@bp.route('/permissions', methods=['GET'])
def get_permissions():
    permissions = Permission.query.all()
    return jsonify([{'id': perm.id, 'name': perm.name} for perm in permissions])

@bp.route('/permissions', methods=['POST'])
def create_permission():
    data = request.json
    new_permission = Permission(name=data['name'])
    db.session.add(new_permission)
    db.session.commit()
    return jsonify({'message': 'Permission created successfully'}), 201

@bp.route('/permissions/<int:id>', methods=['PUT'])
def update_permission(id):
    data = request.json
    permission = Permission.query.get(id)
    if not permission:
        return jsonify({'message': 'Permission not found'}), 404
    permission.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Permission updated successfully'})

@bp.route('/permissions/<int:id>', methods=['DELETE'])
def delete_permission(id):
    permission = Permission.query.get(id)
    if not permission:
        return jsonify({'message': 'Permission not found'}), 404
    db.session.delete(permission)
    db.session.commit()
    return jsonify({'message': 'Permission deleted successfully'})

@app.route('/experiments_stream', methods=['POST'])
def create_experiment():
    data = request.form
    video_stream = request.files['video_stream']

    with tempfile.NamedTemporaryFile(delete=False, dir=app.config['UPLOAD_FOLDER'], suffix='.mp4') as temp_video_file:
        temp_video_file.write(video_stream.read())
        video_path = temp_video_file.name

    new_experiment = Experiment(
        experiment_name=data['experiment_name'],
        description=data['description'],
        video_filename=video_path,
        user_id=data['user_id'],
        pose_estimation_service_id=data['pose_estimation_service_id'],
        action_recognition_service_id=data['action_recognition_service_id'],
        nlp_query_service_id=data['nlp_query_service_id']
    )
    db.session.add(new_experiment)
    db.session.commit()

    pose_service = PoseEstimationService.query.get(data['pose_estimation_service_id'])
    pose_response = requests.post(pose_service.api_endpoint, files={'video': open(video_path, 'rb')}, data={
        'config_path': pose_service.config_path,
        'weights_path': pose_service.weights_path
    })
    pose_data = pose_response.json()

    pose_estimation_data = PoseEstimationData(
        experiment_id=new_experiment.id,
        keypoints_data=pose_data['keypoints']
    )
    db.session.add(pose_estimation_data)
    db.session.commit()

    action_service = ActionRecognitionService.query.get(data['action_recognition_service_id'])
    action_response = requests.post(action_service.api_endpoint, json={
        'keypoints_data': pose_data['keypoints'],
        'config_path': action_service.config_path,
        'weights_path': action_service.weights_path
    })
    action_data = action_response.json()

    action_recognition_data = ActionRecognitionData(
        experiment_id=new_experiment.id,
        result_data=action_data['results']
    )
    db.session.add(action_recognition_data)
    db.session.commit()

    return jsonify({'message': 'Experiment created successfully'}), 201

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 这里可以添加验证逻辑
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user_management')
def user_management():
    return render_template('user.html')

@app.route('/role_management')
def role_management():
    return render_template('role.html')

@app.route('/permission_management')
def permission_management():
    return render_template('permission.html')

@app.route('/offline_experiment_management')
def offline_experiment_management():
    return render_template('experiment.html')

@app.route('/video_stream_experiment_management')
def video_stream_experiment_management():
    return render_template('experiment_stream.html')

@app.route('/pose_estimation_service_management')
def pose_estimation_service_management():
    return render_template('poseEstimationService.html')

@app.route('/behavior_recognition_service_management')
def behavior_recognition_service_management():
    return render_template('actionRecognitionService.html')

@app.route('/pose_estimation_data_management')
def pose_estimation_data_management():
    return render_template('poseEstimationData.html')

@app.route('/behavior_recognition_data_management')
def behavior_recognition_data_management():
    return render_template('actionRecognitionData.html')

@app.route('/nl_query_service_management')
def nl_query_service_management():
    return render_template('nlpQueryService.html')

@app.route('/chat2db')
def chat2db():
    return render_template('chat2DB.html')