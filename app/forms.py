from flask_wtf import FlaskFormfrom, wtforms 
import StringField, TextAreaField, SelectField, FileField, SubmitFieldfrom, wtforms.validators 
import DataRequiredfrom .models 
import PoseEstimationService, ActionRecognitionService, NLPQueryService

class ExperimentForm(FlaskForm):
    experiment_name = StringField('Experiment Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    video_file = FileField('Video File', validators=[DataRequired()])
    pose_estimation_service = SelectField('Pose Estimation Service', coerce=int, validators=[DataRequired()])
    action_recognition_service = SelectField('Action Recognition Service', coerce=int, validators=[DataRequired()])
    nlp_query_service = SelectField('NLP Query Service', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pose_estimation_service.choices = [(service.id, service.service_name, service.config_path, service.weights_path) for service in PoseEstimationService.query.all()]
        self.action_recognition_service.choices = [(service.id, service.service_name, service.config_path, service.weights_path) for service in ActionRecognitionService.query.all()]
        self.nlp_query_service.choices = [(service.id, service.service_name, service.config_path, service.weights_path) for service in NLPQueryService.query.all()]