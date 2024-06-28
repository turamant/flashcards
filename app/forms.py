from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FlashCardForm(FlaskForm):
    english_word = StringField('English Word', validators=[DataRequired()])
    translation = StringField('Translation', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Save')
