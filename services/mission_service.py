import logging
from typing import Dict, List, Optional
from datetime import datetime
from models import Mission, MissionAnalysis, SimulationResult, MissionStatus, RiskLevel
from app import db
from services.nasa_service import NASAService
from services.ai_service import AIService

class MissionService:
    def __init__(self):
        self.nasa_service = NASAService()
        self.ai_service = AIService()
        self.logger = logging.getLogger(__name__)
    
    def create_mission(self, mission_data: Dict) -> Mission:
        """Create a new mission"""
        try:
            mission = Mission(
                name=mission_data['name'],
                description=mission_data.get('description', ''),
                destination=mission_data['destination'],
                launch_date=mission_data['launch_date'],
                mission_duration=mission_data['mission_duration'],
                crew_size=mission_data['crew_size'],
                spacecraft_type=mission_data['spacecraft_type'],
                payload_mass=mission_data.get('payload_mass'),
                fuel_requirements=mission_data.get('fuel_requirements'),
                status=MissionStatus.DRAFT
            )
            
            db.session.add(mission)
            db.session.commit()
            
            self.logger.info(f"Created mission: {mission.name} (ID: {mission.id})")
            return mission
            
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Error creating mission: {e}")
            raise
    
    def analyze_mission(self, mission_id: int) -> Dict:
        """Perform comprehensive mission analysis"""
        try:
            mission = Mission.query.get_or_404(mission_id)
            
            # Update mission status
            mission.status = MissionStatus.ANALYZING
            db.session.commit()
            
            # Get NASA data
            self.logger.info(f"Fetching NASA data for mission {mission.name}")
            nasa_data = self.nasa_service.get_planetary_data(
                mission.destination, 
                mission.launch_date
            )
            
            # Get mission window data
            window_data = self.nasa_service.get_mission_window(
                mission.destination,
                mission.launch_date
            )
            
            # Combine NASA data
            combined_nasa_data = {
                **nasa_data,
                'mission_window': window_data
            }
            
            # Prepare mission data for AI analysis
            mission_data = {
                'name': mission.name,
                'description': mission.description,
                'destination': mission.destination,
                'launch_date': mission.launch_date.isoformat(),
                'mission_duration': mission.mission_duration,
                'crew_size': mission.crew_size,
                'spacecraft_type': mission.spacecraft_type,
                'payload_mass': mission.payload_mass,
                'fuel_requirements': mission.fuel_requirements
            }
            
            # Perform AI analysis
            self.logger.info(f"Performing AI analysis for mission {mission.name}")
            ai_analysis = self.ai_service.analyze_mission_feasibility(
                mission_data, 
                combined_nasa_data
            )
            
            # Update mission with results
            mission.nasa_data = combined_nasa_data
            mission.ai_analysis = ai_analysis
            mission.feasibility_score = ai_analysis.get('feasibility_score', 50)
            mission.risk_level = RiskLevel(ai_analysis.get('risk_level', 'medium'))
            mission.status = MissionStatus.COMPLETED
            mission.analyzed_at = datetime.utcnow()
            
            # Create detailed analysis record
            analysis = MissionAnalysis(
                mission_id=mission.id,
                trajectory_analysis=ai_analysis.get('technical_analysis', {}),
                risk_assessment=ai_analysis.get('risk_assessment', {}),
                resource_requirements=ai_analysis.get('resource_requirements', {}),
                timeline_analysis=ai_analysis.get('timeline', {}),
                recommendations=ai_analysis.get('recommendations', []),
                optimization_suggestions=self._generate_optimization_suggestions(ai_analysis)
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            self.logger.info(f"Completed analysis for mission {mission.name}")
            
            return {
                'mission': mission,
                'analysis': analysis,
                'success': True
            }
            
        except Exception as e:
            db.session.rollback()
            if 'mission' in locals():
                mission.status = MissionStatus.FAILED
                db.session.commit()
            
            self.logger.error(f"Error analyzing mission {mission_id}: {e}")
            return {
                'error': str(e),
                'success': False
            }
    
    def get_mission_history(self, limit: int = 50) -> List[Mission]:
        """Get mission history"""
        try:
            missions = Mission.query.order_by(Mission.created_at.desc()).limit(limit).all()
            return missions
        except Exception as e:
            self.logger.error(f"Error fetching mission history: {e}")
            return []
    
    def get_mission_statistics(self) -> Dict:
        """Get mission statistics"""
        try:
            total_missions = Mission.query.count()
            completed_missions = Mission.query.filter_by(status=MissionStatus.COMPLETED).count()
            failed_missions = Mission.query.filter_by(status=MissionStatus.FAILED).count()
            
            # Risk level distribution
            risk_distribution = {}
            for risk_level in RiskLevel:
                count = Mission.query.filter_by(risk_level=risk_level).count()
                risk_distribution[risk_level.value] = count
            
            # Average feasibility score
            avg_feasibility = db.session.query(
                db.func.avg(Mission.feasibility_score)
            ).filter(Mission.feasibility_score.isnot(None)).scalar() or 0
            
            return {
                'total_missions': total_missions,
                'completed_missions': completed_missions,
                'failed_missions': failed_missions,
                'success_rate': (completed_missions / total_missions * 100) if total_missions > 0 else 0,
                'risk_distribution': risk_distribution,
                'average_feasibility': round(avg_feasibility, 2)
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating statistics: {e}")
            return {
                'total_missions': 0,
                'completed_missions': 0,
                'failed_missions': 0,
                'success_rate': 0,
                'risk_distribution': {},
                'average_feasibility': 0
            }
    
    def compare_missions(self, mission_ids: List[int]) -> Dict:
        """Compare multiple missions"""
        try:
            missions = Mission.query.filter(Mission.id.in_(mission_ids)).all()
            
            if len(missions) < 2:
                return {'error': 'At least 2 missions required for comparison'}
            
            comparison = {
                'missions': [],
                'comparison_metrics': {
                    'feasibility_scores': [],
                    'risk_levels': [],
                    'durations': [],
                    'crew_sizes': []
                }
            }
            
            for mission in missions:
                mission_data = {
                    'id': mission.id,
                    'name': mission.name,
                    'destination': mission.destination,
                    'feasibility_score': mission.feasibility_score,
                    'risk_level': mission.risk_level.value if mission.risk_level else 'unknown',
                    'duration': mission.mission_duration,
                    'crew_size': mission.crew_size,
                    'status': mission.status.value
                }
                
                comparison['missions'].append(mission_data)
                comparison['comparison_metrics']['feasibility_scores'].append(mission.feasibility_score or 0)
                comparison['comparison_metrics']['risk_levels'].append(mission.risk_level.value if mission.risk_level else 'unknown')
                comparison['comparison_metrics']['durations'].append(mission.mission_duration)
                comparison['comparison_metrics']['crew_sizes'].append(mission.crew_size)
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"Error comparing missions: {e}")
            return {'error': str(e)}
    
    def generate_mission_report(self, mission_id: int) -> Dict:
        """Generate comprehensive mission report"""
        try:
            mission = Mission.query.get_or_404(mission_id)
            
            if mission.status != MissionStatus.COMPLETED:
                return {'error': 'Mission analysis not completed'}
            
            mission_data = {
                'name': mission.name,
                'description': mission.description,
                'destination': mission.destination,
                'launch_date': mission.launch_date.isoformat(),
                'mission_duration': mission.mission_duration,
                'crew_size': mission.crew_size,
                'spacecraft_type': mission.spacecraft_type,
                'feasibility_score': mission.feasibility_score,
                'risk_level': mission.risk_level.value if mission.risk_level else 'unknown'
            }
            
            # Generate comprehensive report using AI
            report = self.ai_service.generate_mission_report(
                mission_data,
                mission.ai_analysis or {}
            )
            
            return {
                'mission': mission,
                'report': report,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f"Error generating report for mission {mission_id}: {e}")
            return {
                'error': str(e),
                'success': False
            }
    
    def _generate_optimization_suggestions(self, ai_analysis: Dict) -> List[str]:
        """Generate optimization suggestions based on AI analysis"""
        suggestions = []
        
        feasibility_score = ai_analysis.get('feasibility_score', 50)
        risk_level = ai_analysis.get('risk_level', 'medium')
        
        if feasibility_score < 70:
            suggestions.append("Consider extending mission preparation time")
            suggestions.append("Review spacecraft specifications for better suitability")
        
        if risk_level in ['high', 'critical']:
            suggestions.append("Implement additional safety protocols")
            suggestions.append("Consider backup mission scenarios")
        
        # Add resource-based suggestions
        resource_reqs = ai_analysis.get('resource_requirements', {})
        if 'fuel_estimate' in resource_reqs:
            suggestions.append("Optimize fuel consumption through trajectory planning")
        
        if not suggestions:
            suggestions.append("Mission parameters are well-optimized")
        
        return suggestions
