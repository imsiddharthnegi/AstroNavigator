from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from datetime import date, timedelta

class MissionForm(FlaskForm):
    name = StringField('Mission Name', validators=[
        DataRequired(),
        Length(min=3, max=200, message='Mission name must be between 3 and 200 characters')
    ])
    
    description = TextAreaField('Mission Description', validators=[
        Optional(),
        Length(max=1000, message='Description must be less than 1000 characters')
    ])
    
    destination = SelectField('Destination', validators=[DataRequired()], choices=[
        ('mars', 'Mars'),
        ('moon', 'Moon'),
        ('venus', 'Venus'),
        ('jupiter', 'Jupiter'),
        ('saturn', 'Saturn'),
        ('asteroid_belt', 'Asteroid Belt'),
        ('europa', 'Europa (Jupiter Moon)'),
        ('titan', 'Titan (Saturn Moon)'),
        ('enceladus', 'Enceladus (Saturn Moon)'),
        ('io', 'Io (Jupiter Moon)')
    ])
    
    launch_date = DateField('Launch Date', validators=[DataRequired()], 
                           default=date.today() + timedelta(days=30))
    
    mission_duration = IntegerField('Mission Duration (days)', validators=[
        DataRequired(),
        NumberRange(min=1, max=3650, message='Mission duration must be between 1 and 3650 days')
    ])
    
    crew_size = IntegerField('Crew Size', validators=[
        DataRequired(),
        NumberRange(min=0, max=20, message='Crew size must be between 0 and 20')
    ])
    
    spacecraft_type = SelectField('Spacecraft Type', validators=[DataRequired()], choices=[
        ('orion', 'Orion Multi-Purpose Crew Vehicle'),
        ('dragon', 'SpaceX Dragon'),
        ('soyuz', 'Soyuz'),
        ('artemis', 'Artemis Lunar Lander'),
        ('custom', 'Custom Spacecraft')
    ])
    
    payload_mass = FloatField('Payload Mass (kg)', validators=[
        Optional(),
        NumberRange(min=0, max=100000, message='Payload mass must be between 0 and 100,000 kg')
    ])
    
    fuel_requirements = FloatField('Estimated Fuel Requirements (kg)', validators=[
        Optional(),
        NumberRange(min=0, max=1000000, message='Fuel requirements must be between 0 and 1,000,000 kg')
    ])
    
    submit = SubmitField('Create Mission')

class MissionAnalysisForm(FlaskForm):
    mission_id = IntegerField('Mission ID', validators=[DataRequired()])
    submit = SubmitField('Analyze Mission')
