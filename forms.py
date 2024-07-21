from wtforms import Form, StringField, validators


class WhishForm(Form):
    title = StringField('Title', [validators.DataRequired(), validators.Length(max=128)])
    description = StringField('Description', [validators.Length(max=1024)])
