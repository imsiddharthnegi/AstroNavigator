from flask import Blueprint, render_template, request, flash, redirect, url_for
from utils.formatters import MissionFormatter
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    """Main landing page"""
    try:
        # Import here to avoid circular import
        from services.mission_service import MissionService
        mission_service = MissionService()
        
        # Get recent missions and statistics
        recent_missions = mission_service.get_mission_history(limit=5)
        statistics = mission_service.get_mission_statistics()
        
        formatted_missions = []
        for mission in recent_missions:
            formatted_missions.append(MissionFormatter.format_mission_data(mission))
        
        return render_template('index.html', 
                             recent_missions=formatted_missions,
                             statistics=statistics)
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        flash('Error loading dashboard data', 'error')
        return render_template('index.html', 
                             recent_missions=[],
                             statistics={})

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/api/status')
def api_status():
    """API status endpoint"""
    return {
        'status': 'operational',
        'services': {
            'database': 'operational',
            'nasa_api': 'operational',
            'ai_service': 'operational'
        },
        'version': '1.0.0'
    }

@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500
