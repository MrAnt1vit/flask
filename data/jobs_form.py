from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField("Job title", validators=[DataRequired()])
    team_leader = StringField("Team Leader id")
    work_size = IntegerField("Work size")
    collaborators = StringField("Collaborators")
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')
