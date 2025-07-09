import re
from datetime import datetime, date
from typing import Optional, Union

class ValidationError(Exception):
    """Custom validation error"""
    pass

class MissionValidator:
    @staticmethod
    def validate_mission_name(name: str) -> bool:
        """Validate mission name"""
        if not name or len(name.strip()) < 3:
            raise ValidationError("Mission name must be at least 3 characters long")
        
        if len(name) > 200:
            raise ValidationError("Mission name cannot exceed 200 characters")
        
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9\s\-_\.]+$', name):
            raise ValidationError("Mission name contains invalid characters")
        
        return True
    
    @staticmethod
    def validate_launch_date(launch_date: Union[date, str]) -> bool:
        """Validate launch date"""
        if isinstance(launch_date, str):
            try:
                launch_date = datetime.strptime(launch_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD")
        
        if launch_date < date.today():
            raise ValidationError("Launch date cannot be in the past")
        
        # Check if date is too far in the future (arbitrary limit of 50 years)
        max_date = date.today().replace(year=date.today().year + 50)
        if launch_date > max_date:
            raise ValidationError("Launch date cannot be more than 50 years in the future")
        
        return True
    
    @staticmethod
    def validate_mission_duration(duration: int) -> bool:
        """Validate mission duration"""
        if duration < 1:
            raise ValidationError("Mission duration must be at least 1 day")
        
        if duration > 3650:  # 10 years
            raise ValidationError("Mission duration cannot exceed 10 years (3650 days)")
        
        return True
    
    @staticmethod
    def validate_crew_size(crew_size: int) -> bool:
        """Validate crew size"""
        if crew_size < 0:
            raise ValidationError("Crew size cannot be negative")
        
        if crew_size > 20:
            raise ValidationError("Crew size cannot exceed 20 members")
        
        return True
    
    @staticmethod
    def validate_payload_mass(payload_mass: Optional[float]) -> bool:
        """Validate payload mass"""
        if payload_mass is None:
            return True
        
        if payload_mass < 0:
            raise ValidationError("Payload mass cannot be negative")
        
        if payload_mass > 100000:  # 100 tons
            raise ValidationError("Payload mass cannot exceed 100,000 kg")
        
        return True
    
    @staticmethod
    def validate_fuel_requirements(fuel_requirements: Optional[float]) -> bool:
        """Validate fuel requirements"""
        if fuel_requirements is None:
            return True
        
        if fuel_requirements < 0:
            raise ValidationError("Fuel requirements cannot be negative")
        
        if fuel_requirements > 1000000:  # 1000 tons
            raise ValidationError("Fuel requirements cannot exceed 1,000,000 kg")
        
        return True
    
    @staticmethod
    def validate_destination(destination: str) -> bool:
        """Validate destination"""
        valid_destinations = [
            'mars', 'moon', 'venus', 'jupiter', 'saturn', 
            'asteroid_belt', 'europa', 'titan', 'enceladus', 'io'
        ]
        
        if destination not in valid_destinations:
            raise ValidationError(f"Invalid destination. Must be one of: {', '.join(valid_destinations)}")
        
        return True
    
    @staticmethod
    def validate_spacecraft_type(spacecraft_type: str) -> bool:
        """Validate spacecraft type"""
        valid_types = ['orion', 'dragon', 'soyuz', 'artemis', 'custom']
        
        if spacecraft_type not in valid_types:
            raise ValidationError(f"Invalid spacecraft type. Must be one of: {', '.join(valid_types)}")
        
        return True
    
    @classmethod
    def validate_mission_data(cls, mission_data: dict) -> bool:
        """Validate complete mission data"""
        cls.validate_mission_name(mission_data.get('name', ''))
        cls.validate_destination(mission_data.get('destination', ''))
        cls.validate_launch_date(mission_data.get('launch_date'))
        cls.validate_mission_duration(mission_data.get('mission_duration', 0))
        cls.validate_crew_size(mission_data.get('crew_size', 0))
        cls.validate_spacecraft_type(mission_data.get('spacecraft_type', ''))
        cls.validate_payload_mass(mission_data.get('payload_mass'))
        cls.validate_fuel_requirements(mission_data.get('fuel_requirements'))
        
        return True

class DataValidator:
    @staticmethod
    def validate_nasa_response(response_data: dict) -> bool:
        """Validate NASA API response"""
        if not response_data:
            raise ValidationError("Empty NASA API response")
        
        required_fields = ['destination', 'data_source', 'retrieved_at']
        for field in required_fields:
            if field not in response_data:
                raise ValidationError(f"Missing required field in NASA response: {field}")
        
        return True
    
    @staticmethod
    def validate_ai_analysis(analysis_data: dict) -> bool:
        """Validate AI analysis response"""
        if not analysis_data:
            raise ValidationError("Empty AI analysis response")
        
        required_fields = ['feasibility_score', 'risk_level', 'summary']
        for field in required_fields:
            if field not in analysis_data:
                raise ValidationError(f"Missing required field in AI analysis: {field}")
        
        # Validate feasibility score
        score = analysis_data.get('feasibility_score', 0)
        if not isinstance(score, (int, float)) or score < 0 or score > 100:
            raise ValidationError("Feasibility score must be between 0 and 100")
        
        # Validate risk level
        valid_risk_levels = ['low', 'medium', 'high', 'critical']
        if analysis_data.get('risk_level') not in valid_risk_levels:
            raise ValidationError(f"Invalid risk level. Must be one of: {', '.join(valid_risk_levels)}")
        
        return True
