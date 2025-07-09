from datetime import datetime, date
from typing import Dict, List, Optional, Union

class MissionFormatter:
    @staticmethod
    def format_mission_data(mission) -> Dict:
        """Format mission data for display"""
        return {
            'id': mission.id,
            'name': mission.name,
            'description': mission.description,
            'destination': mission.destination.replace('_', ' ').title(),
            'launch_date': mission.launch_date.strftime('%Y-%m-%d'),
            'mission_duration': f"{mission.mission_duration} days",
            'crew_size': f"{mission.crew_size} {'person' if mission.crew_size == 1 else 'people'}",
            'spacecraft_type': mission.spacecraft_type.replace('_', ' ').title(),
            'payload_mass': f"{mission.payload_mass:,.0f} kg" if mission.payload_mass else 'Not specified',
            'fuel_requirements': f"{mission.fuel_requirements:,.0f} kg" if mission.fuel_requirements else 'Not specified',
            'status': mission.status.value.replace('_', ' ').title(),
            'risk_level': mission.risk_level.value.title() if mission.risk_level else 'Not assessed',
            'feasibility_score': f"{mission.feasibility_score:.1f}%" if mission.feasibility_score else 'Not assessed',
            'created_at': mission.created_at.strftime('%Y-%m-%d %H:%M'),
            'analyzed_at': mission.analyzed_at.strftime('%Y-%m-%d %H:%M') if mission.analyzed_at else 'Not analyzed'
        }
    
    @staticmethod
    def format_analysis_data(analysis) -> Dict:
        """Format analysis data for display"""
        if not analysis:
            return {}
        
        return {
            'trajectory_analysis': analysis.trajectory_analysis or {},
            'risk_assessment': analysis.risk_assessment or {},
            'resource_requirements': analysis.resource_requirements or {},
            'timeline_analysis': analysis.timeline_analysis or {},
            'recommendations': analysis.recommendations or [],
            'optimization_suggestions': analysis.optimization_suggestions or [],
            'created_at': analysis.created_at.strftime('%Y-%m-%d %H:%M')
        }
    
    @staticmethod
    def format_nasa_data(nasa_data: Dict) -> Dict:
        """Format NASA data for display"""
        if not nasa_data:
            return {}
        
        formatted = {
            'destination': nasa_data.get('destination', 'Unknown').replace('_', ' ').title(),
            'data_source': nasa_data.get('data_source', 'Unknown'),
            'retrieved_at': nasa_data.get('retrieved_at', 'Unknown')
        }
        
        # Format orbital parameters
        orbital_params = nasa_data.get('orbital_parameters', {})
        if orbital_params:
            formatted['orbital_parameters'] = {
                'distance_from_earth': DataFormatter.format_distance(orbital_params.get('distance_from_earth')),
                'velocity_magnitude': DataFormatter.format_velocity(orbital_params.get('velocity_magnitude')),
                'orbital_period': DataFormatter.format_duration(orbital_params.get('orbital_period')),
                'mass': DataFormatter.format_mass(orbital_params.get('mass')),
                'gravity': DataFormatter.format_gravity(orbital_params.get('gravity'))
            }
        
        # Format mission window
        mission_window = nasa_data.get('mission_window', {})
        if mission_window:
            formatted['mission_window'] = {
                'launch_date': mission_window.get('launch_date', 'Unknown'),
                'window_duration': f"{mission_window.get('window_duration', 'Unknown')} days",
                'next_window_in_days': f"{mission_window.get('next_window_in_days', 'Unknown')} days",
                'optimal_window': 'Yes' if mission_window.get('optimal_window') else 'No',
                'recommendation': mission_window.get('recommendation', 'No recommendation')
            }
        
        return formatted
    
    @staticmethod
    def format_ai_analysis(ai_data: Dict) -> Dict:
        """Format AI analysis data for display"""
        if not ai_data:
            return {}
        
        formatted = {
            'feasibility_score': f"{ai_data.get('feasibility_score', 0):.1f}%",
            'risk_level': ai_data.get('risk_level', 'Unknown').title(),
            'summary': ai_data.get('summary', 'No summary available'),
            'ai_model': ai_data.get('ai_model', 'Unknown'),
            'analysis_timestamp': ai_data.get('analysis_timestamp', 'Unknown')
        }
        
        # Format technical analysis
        tech_analysis = ai_data.get('technical_analysis', {})
        if tech_analysis:
            formatted['technical_analysis'] = {
                'trajectory': tech_analysis.get('trajectory', 'Not available'),
                'propulsion': tech_analysis.get('propulsion', 'Not available'),
                'life_support': tech_analysis.get('life_support', 'Not available'),
                'communication': tech_analysis.get('communication', 'Not available'),
                'landing': tech_analysis.get('landing', 'Not available')
            }
        
        # Format risk assessment
        risk_assessment = ai_data.get('risk_assessment', {})
        if risk_assessment:
            formatted['risk_assessment'] = {
                'primary_risks': risk_assessment.get('primary_risks', []),
                'radiation_exposure': risk_assessment.get('radiation_exposure', 'Not assessed'),
                'micrometeorite_risk': risk_assessment.get('micrometeorite_risk', 'Not assessed'),
                'system_failures': risk_assessment.get('system_failures', 'Not assessed')
            }
        
        # Format resource requirements
        resources = ai_data.get('resource_requirements', {})
        if resources:
            formatted['resource_requirements'] = {
                'fuel_estimate': resources.get('fuel_estimate', 'Not estimated'),
                'power_requirements': resources.get('power_requirements', 'Not estimated'),
                'water_requirements': resources.get('water_requirements', 'Not estimated'),
                'food_requirements': resources.get('food_requirements', 'Not estimated')
            }
        
        # Format timeline
        timeline = ai_data.get('timeline', {})
        if timeline:
            formatted['timeline'] = {
                'launch_preparation': timeline.get('launch_preparation', 'Not estimated'),
                'transit_time': timeline.get('transit_time', 'Not estimated'),
                'mission_operations': timeline.get('mission_operations', 'Not estimated'),
                'return_time': timeline.get('return_time', 'Not estimated')
            }
        
        formatted['recommendations'] = ai_data.get('recommendations', [])
        
        return formatted

class DataFormatter:
    @staticmethod
    def format_distance(distance: Optional[float]) -> str:
        """Format distance with appropriate units"""
        if distance is None:
            return 'Unknown'
        
        if distance < 1000:
            return f"{distance:.1f} km"
        elif distance < 1000000:
            return f"{distance/1000:.1f} thousand km"
        else:
            return f"{distance/1000000:.1f} million km"
    
    @staticmethod
    def format_velocity(velocity: Optional[float]) -> str:
        """Format velocity"""
        if velocity is None:
            return 'Unknown'
        return f"{velocity:.1f} km/s"
    
    @staticmethod
    def format_duration(duration: Optional[float]) -> str:
        """Format duration in days"""
        if duration is None:
            return 'Unknown'
        
        if duration < 30:
            return f"{duration:.1f} days"
        elif duration < 365:
            return f"{duration/30:.1f} months"
        else:
            return f"{duration/365:.1f} years"
    
    @staticmethod
    def format_mass(mass: Optional[float]) -> str:
        """Format mass"""
        if mass is None:
            return 'Unknown'
        
        if mass < 1e6:
            return f"{mass:.2e} kg"
        else:
            return f"{mass:.2e} kg"
    
    @staticmethod
    def format_gravity(gravity: Optional[float]) -> str:
        """Format gravity"""
        if gravity is None:
            return 'Unknown'
        return f"{gravity:.2f} m/s²"
    
    @staticmethod
    def format_percentage(value: Optional[float]) -> str:
        """Format percentage"""
        if value is None:
            return 'Unknown'
        return f"{value:.1f}%"
    
    @staticmethod
    def format_datetime(dt: Optional[datetime]) -> str:
        """Format datetime"""
        if dt is None:
            return 'Unknown'
        return dt.strftime('%Y-%m-%d %H:%M UTC')
    
    @staticmethod
    def format_risk_level(risk_level: str) -> Dict:
        """Format risk level with color coding"""
        risk_colors = {
            'low': {'color': 'success', 'icon': 'check-circle'},
            'medium': {'color': 'warning', 'icon': 'exclamation-triangle'},
            'high': {'color': 'danger', 'icon': 'exclamation-circle'},
            'critical': {'color': 'danger', 'icon': 'times-circle'}
        }
        
        return {
            'level': risk_level.title(),
            'color': risk_colors.get(risk_level, {}).get('color', 'secondary'),
            'icon': risk_colors.get(risk_level, {}).get('icon', 'question-circle')
        }
    
    @staticmethod
    def format_status(status: str) -> Dict:
        """Format status with color coding"""
        status_colors = {
            'draft': {'color': 'secondary', 'icon': 'edit'},
            'analyzing': {'color': 'info', 'icon': 'spinner'},
            'completed': {'color': 'success', 'icon': 'check'},
            'failed': {'color': 'danger', 'icon': 'times'}
        }
        
        return {
            'status': status.replace('_', ' ').title(),
            'color': status_colors.get(status, {}).get('color', 'secondary'),
            'icon': status_colors.get(status, {}).get('icon', 'question-circle')
        }
