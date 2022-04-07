from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea

class TextForm(FlaskForm):
    message = StringField('text', widget=TextArea())
    submit = SubmitField('Classify')