from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from forms import MissionForm
from utils.formatters import MissionFormatter, DataFormatter
from utils.validators import MissionValidator, ValidationError
import logging

mission_bp = Blueprint('mission', __name__)
logger = logging.getLogger(__name__)

@mission_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new mission"""
    form = MissionForm()
    
    if form.validate_on_submit():
        try:
            # Import here to avoid circular import
            from services.mission_service import MissionService
            mission_service = MissionService()
            
            # Validate mission data
            mission_data = {
                'name': form.name.data,
                'description': form.description.data,
                'destination': form.destination.data,
                'launch_date': form.launch_date.data,
                'mission_duration': form.mission_duration.data,
                'crew_size': form.crew_size.data,
                'spacecraft_type': form.spacecraft_type.data,
                'payload_mass': form.payload_mass.data,
                'fuel_requirements': form.fuel_requirements.data
            }
            
            MissionValidator.validate_mission_data(mission_data)
            
            # Create mission
            mission = mission_service.create_mission(mission_data)
            
            flash(f'Mission "{mission.name}" created successfully!', 'success')
            return redirect(url_for('mission.view', mission_id=mission.id))
            
        except ValidationError as e:
            flash(f'Validation error: {str(e)}', 'error')
        except Exception as e:
            logger.error(f"Error creating mission: {e}")
            flash('An error occurred while creating the mission', 'error')
    
    return render_template('mission/create.html', form=form)

@mission_bp.route('/<int:mission_id>')
def view(mission_id):
    """View mission details"""
    try:
        from models import Mission
        mission = Mission.query.get_or_404(mission_id)
        
        formatted_mission = MissionFormatter.format_mission_data(mission)
        
        # Get formatted analysis data if available
        analysis_data = {}
        if mission.analyses:
            latest_analysis = mission.analyses[-1]  # Get most recent analysis
            analysis_data = MissionFormatter.format_analysis_data(latest_analysis)
        
        # Format NASA data
        nasa_data = {}
        if mission.nasa_data:
            nasa_data = MissionFormatter.format_nasa_data(mission.nasa_data)
        
        # Format AI analysis
        ai_analysis = {}
        if mission.ai_analysis:
            ai_analysis = MissionFormatter.format_ai_analysis(mission.ai_analysis)
        
        return render_template('mission/view.html',
                             mission=formatted_mission,
                             analysis_data=analysis_data,
                             nasa_data=nasa_data,
                             ai_analysis=ai_analysis)
    
    except Exception as e:
        logger.error(f"Error viewing mission {mission_id}: {e}")
        flash('Error loading mission details', 'error')
        return redirect(url_for('main.index'))

@mission_bp.route('/<int:mission_id>/analyze', methods=['POST'])
def analyze(mission_id):
    """Analyze mission"""
    try:
        from services.mission_service import MissionService
        mission_service = MissionService()
        result = mission_service.analyze_mission(mission_id)
        
        if result['success']:
            flash('Mission analysis completed successfully!', 'success')
            return redirect(url_for('mission.results', mission_id=mission_id))
        else:
            flash(f'Analysis failed: {result["error"]}', 'error')
            return redirect(url_for('mission.view', mission_id=mission_id))
    
    except Exception as e:
        logger.error(f"Error analyzing mission {mission_id}: {e}")
        flash('An error occurred during mission analysis', 'error')
        return redirect(url_for('mission.view', mission_id=mission_id))

@mission_bp.route('/<int:mission_id>/results')
def results(mission_id):
    """View mission analysis results"""
    try:
        from models import Mission
        mission = Mission.query.get_or_404(mission_id)
        
        if not mission.ai_analysis:
            flash('Mission analysis not available', 'warning')
            return redirect(url_for('mission.view', mission_id=mission_id))
        
        formatted_mission = MissionFormatter.format_mission_data(mission)
        formatted_analysis = MissionFormatter.format_ai_analysis(mission.ai_analysis)
        formatted_nasa_data = MissionFormatter.format_nasa_data(mission.nasa_data or {})
        
        return render_template('mission/results.html',
                             mission=formatted_mission,
                             analysis=formatted_analysis,
                             nasa_data=formatted_nasa_data)
    
    except Exception as e:
        logger.error(f"Error viewing results for mission {mission_id}: {e}")
        flash('Error loading mission results', 'error')
        return redirect(url_for('mission.view', mission_id=mission_id))

@mission_bp.route('/history')
def history():
    """View mission history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10
        
        from models import Mission
        missions_pagination = Mission.query.order_by(Mission.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        formatted_missions = []
        for mission in missions_pagination.items:
            formatted_missions.append(MissionFormatter.format_mission_data(mission))
        
        return render_template('mission/history.html',
                             missions=formatted_missions,
                             pagination=missions_pagination)
    
    except Exception as e:
        logger.error(f"Error loading mission history: {e}")
        flash('Error loading mission history', 'error')
        return render_template('mission/history.html', missions=[], pagination=None)

@mission_bp.route('/compare')
def compare():
    """Compare missions"""
    try:
        mission_ids = request.args.getlist('missions', type=int)
        
        if len(mission_ids) < 2:
            flash('Please select at least 2 missions to compare', 'warning')
            return redirect(url_for('mission.history'))
        
        from services.mission_service import MissionService
        mission_service = MissionService()
        comparison_data = mission_service.compare_missions(mission_ids)
        
        if 'error' in comparison_data:
            flash(comparison_data['error'], 'error')
            return redirect(url_for('mission.history'))
        
        return render_template('mission/compare.html', comparison=comparison_data)
    
    except Exception as e:
        logger.error(f"Error comparing missions: {e}")
        flash('Error comparing missions', 'error')
        return redirect(url_for('mission.history'))

@mission_bp.route('/<int:mission_id>/report')
def report(mission_id):
    """Generate mission report"""
    try:
        from services.mission_service import MissionService
        mission_service = MissionService()
        report_data = mission_service.generate_mission_report(mission_id)
        
        if not report_data['success']:
            flash(f'Report generation failed: {report_data["error"]}', 'error')
            return redirect(url_for('mission.view', mission_id=mission_id))
        
        formatted_mission = MissionFormatter.format_mission_data(report_data['mission'])
        
        return render_template('mission/report.html',
                             mission=formatted_mission,
                             report=report_data['report'])
    
    except Exception as e:
        logger.error(f"Error generating report for mission {mission_id}: {e}")
        flash('Error generating mission report', 'error')
        return redirect(url_for('mission.view', mission_id=mission_id))

@mission_bp.route('/api/status/<int:mission_id>')
def api_status(mission_id):
    """Get mission status via API"""
    try:
        from models import Mission
        mission = Mission.query.get_or_404(mission_id)
        
        return jsonify({
            'mission_id': mission.id,
            'name': mission.name,
            'status': mission.status.value,
            'feasibility_score': mission.feasibility_score,
            'risk_level': mission.risk_level.value if mission.risk_level else None,
            'created_at': mission.created_at.isoformat(),
            'analyzed_at': mission.analyzed_at.isoformat() if mission.analyzed_at else None
        })
    
    except Exception as e:
        logger.error(f"Error getting mission status: {e}")
        return jsonify({'error': 'Mission not found'}), 404

@mission_bp.route('/api/statistics')
def api_statistics():
    """Get mission statistics via API"""
    try:
        from services.mission_service import MissionService
        mission_service = MissionService()
        statistics = mission_service.get_mission_statistics()
        return jsonify(statistics)
    
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'error': 'Unable to fetch statistics'}), 500
