from app import db
from datetime import datetime
from sqlalchemy import Text, JSON
import enum

class MissionStatus(enum.Enum):
    DRAFT = "draft"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(Text)
    
    # Mission Parameters
    destination = db.Column(db.String(100), nullable=False)
    launch_date = db.Column(db.Date, nullable=False)
    mission_duration = db.Column(db.Integer, nullable=False)  # in days
    crew_size = db.Column(db.Integer, nullable=False)
    spacecraft_type = db.Column(db.String(100), nullable=False)
    
    # Mission Details
    orbital_parameters = db.Column(JSON)
    payload_mass = db.Column(db.Float)  # kg
    fuel_requirements = db.Column(db.Float)  # kg
    
    # Status and Results
    status = db.Column(db.Enum(MissionStatus), default=MissionStatus.DRAFT)
    risk_level = db.Column(db.Enum(RiskLevel))
    feasibility_score = db.Column(db.Float)  # 0-100
    
    # AI Analysis Results
    ai_analysis = db.Column(JSON)
    nasa_data = db.Column(JSON)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    analyzed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Mission {self.name}>'

class MissionAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    
    # Analysis Components
    trajectory_analysis = db.Column(JSON)
    risk_assessment = db.Column(JSON)
    resource_requirements = db.Column(JSON)
    timeline_analysis = db.Column(JSON)
    
    # Recommendations
    recommendations = db.Column(JSON)
    optimization_suggestions = db.Column(JSON)
    
    # Metadata
    analysis_version = db.Column(db.String(50), default='1.0')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    mission = db.relationship('Mission', backref=db.backref('analyses', lazy=True))

class SimulationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    
    # Simulation Data
    trajectory_data = db.Column(JSON)
    fuel_consumption = db.Column(JSON)
    mission_timeline = db.Column(JSON)
    success_probability = db.Column(db.Float)
    
    # Environmental Factors
    radiation_exposure = db.Column(db.Float)
    temperature_variations = db.Column(JSON)
    micrometeorite_risk = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    mission = db.relationship('Mission', backref=db.backref('simulation_results', lazy=True))
