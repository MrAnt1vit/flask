from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField("Department title", validators=[DataRequired()])
    chief = StringField("Cheif id")
    members = StringField("Members")
    email = EmailField('email', validators=[DataRequired()])
    submit = SubmitField('Submit')
