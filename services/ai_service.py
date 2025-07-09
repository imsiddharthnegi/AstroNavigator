import os
import json
import logging
from typing import Dict, Optional
from openai import OpenAI

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.logger = logging.getLogger(__name__)
    
    def analyze_mission_feasibility(self, mission_data: Dict, nasa_data: Dict) -> Dict:
        """Analyze mission feasibility using AI"""
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            
            prompt = self._build_feasibility_prompt(mission_data, nasa_data)
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert space mission analyst with deep knowledge of orbital mechanics, spacecraft engineering, and mission planning. Provide detailed technical analysis in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return self._process_ai_response(result)
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return self._get_fallback_analysis(mission_data)
    
    def _build_feasibility_prompt(self, mission_data: Dict, nasa_data: Dict) -> str:
        """Build the prompt for AI analysis"""
        return f"""
        Analyze the feasibility of this space mission and provide a comprehensive assessment in JSON format:

        Mission Details:
        - Name: {mission_data.get('name', 'Unknown')}
        - Destination: {mission_data.get('destination', 'Unknown')}
        - Launch Date: {mission_data.get('launch_date', 'Unknown')}
        - Duration: {mission_data.get('mission_duration', 'Unknown')} days
        - Crew Size: {mission_data.get('crew_size', 'Unknown')}
        - Spacecraft: {mission_data.get('spacecraft_type', 'Unknown')}
        - Payload Mass: {mission_data.get('payload_mass', 'Unknown')} kg

        NASA Orbital Data:
        {json.dumps(nasa_data, indent=2)}

        Provide your analysis in the following JSON structure:
        {{
            "feasibility_score": <number 0-100>,
            "risk_level": "<low|medium|high|critical>",
            "summary": "<brief summary of overall assessment>",
            "technical_analysis": {{
                "trajectory": "<analysis of trajectory and orbital mechanics>",
                "propulsion": "<fuel and propulsion requirements assessment>",
                "life_support": "<life support systems analysis for crew missions>",
                "communication": "<communication challenges and solutions>",
                "landing": "<landing/docking feasibility if applicable>"
            }},
            "risk_assessment": {{
                "primary_risks": ["<risk1>", "<risk2>", "<risk3>"],
                "radiation_exposure": "<assessment of radiation risks>",
                "micrometeorite_risk": "<assessment of debris/micrometeorite risks>",
                "system_failures": "<critical system failure scenarios>"
            }},
            "resource_requirements": {{
                "fuel_estimate": "<fuel requirements in kg>",
                "power_requirements": "<power system needs>",
                "water_requirements": "<water needs for crew>",
                "food_requirements": "<food needs for crew>"
            }},
            "recommendations": [
                "<recommendation1>",
                "<recommendation2>",
                "<recommendation3>"
            ],
            "timeline": {{
                "launch_preparation": "<months>",
                "transit_time": "<months>",
                "mission_operations": "<months>",
                "return_time": "<months if applicable>"
            }}
        }}
        """
    
    def _process_ai_response(self, ai_result: Dict) -> Dict:
        """Process and validate AI response"""
        try:
            # Ensure required fields exist
            processed = {
                'feasibility_score': min(100, max(0, ai_result.get('feasibility_score', 50))),
                'risk_level': ai_result.get('risk_level', 'medium'),
                'summary': ai_result.get('summary', 'Analysis completed'),
                'technical_analysis': ai_result.get('technical_analysis', {}),
                'risk_assessment': ai_result.get('risk_assessment', {}),
                'resource_requirements': ai_result.get('resource_requirements', {}),
                'recommendations': ai_result.get('recommendations', []),
                'timeline': ai_result.get('timeline', {}),
                'ai_model': 'gpt-4o',
                'analysis_timestamp': self._get_current_timestamp()
            }
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Error processing AI response: {e}")
            return self._get_fallback_analysis({})
    
    def generate_mission_report(self, mission_data: Dict, analysis_result: Dict) -> Dict:
        """Generate comprehensive mission report"""
        try:
            prompt = f"""
            Generate a comprehensive mission report based on the following data:

            Mission: {mission_data.get('name', 'Unknown Mission')}
            Analysis: {json.dumps(analysis_result, indent=2)}

            Create a detailed report in JSON format with:
            {{
                "executive_summary": "<2-3 paragraph summary>",
                "mission_overview": "<detailed mission description>",
                "technical_specifications": "<detailed technical specs>",
                "risk_mitigation": "<risk mitigation strategies>",
                "success_factors": "<key factors for mission success>",
                "contingency_plans": "<backup plans and alternatives>",
                "resource_allocation": "<detailed resource breakdown>",
                "timeline_details": "<detailed mission timeline>",
                "conclusion": "<final assessment and recommendations>"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior space mission analyst creating formal mission reports for space agencies. Write professionally and technically accurate content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=3000,
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return {
                'executive_summary': 'Report generation failed. Please try again.',
                'error': str(e)
            }
    
    def _get_fallback_analysis(self, mission_data: Dict) -> Dict:
        """Provide fallback analysis when AI is unavailable"""
        return {
            'feasibility_score': 65,
            'risk_level': 'medium',
            'summary': 'AI analysis unavailable. Basic assessment provided.',
            'technical_analysis': {
                'trajectory': 'Trajectory analysis requires AI service',
                'propulsion': 'Propulsion analysis requires AI service',
                'life_support': 'Life support analysis requires AI service',
                'communication': 'Communication analysis requires AI service'
            },
            'risk_assessment': {
                'primary_risks': ['AI service unavailable'],
                'radiation_exposure': 'Requires detailed analysis',
                'micrometeorite_risk': 'Requires detailed analysis'
            },
            'resource_requirements': {
                'fuel_estimate': 'Requires AI analysis',
                'power_requirements': 'Requires AI analysis'
            },
            'recommendations': [
                'Enable AI service for detailed analysis',
                'Consult mission planning experts',
                'Review historical mission data'
            ],
            'timeline': {
                'analysis_status': 'AI service required for timeline analysis'
            },
            'error': 'AI service unavailable - using fallback analysis'
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
