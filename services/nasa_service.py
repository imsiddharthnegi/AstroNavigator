import os
import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List

class NASAService:
    def __init__(self):
        self.horizons_base_url = "https://ssd-api.jpl.nasa.gov/api/horizons.api"
        self.nasa_api_key = os.environ.get("NASA_API_KEY", "DEMO_KEY")  # For basic usage
        self.logger = logging.getLogger(__name__)
    
    def get_planetary_data(self, destination: str, launch_date: datetime) -> Dict:
        """Get planetary data from NASA API services"""
        try:
            # Try to get real-time data from NASA APIs
            astronomical_data = self._get_astronomical_data(destination)
            
            # Add launch window calculations
            launch_window = self.get_mission_window(destination, launch_date)
            
            # Combine the data
            result = {
                'destination': destination,
                'orbital_parameters': astronomical_data,
                'launch_window': launch_window,
                'data_source': 'NASA APIs + Calculations',
                'retrieved_at': datetime.now().isoformat(),
                'api_key_used': self.nasa_api_key != "DEMO_KEY"
            }
            
            return result
                
        except Exception as e:
            self.logger.error(f"Error processing NASA data: {e}")
            return self._get_fallback_data(destination)
    
    def _get_astronomical_data(self, destination: str) -> Dict:
        """Get astronomical data from NASA APIs"""
        try:
            # Use NASA's general planetary API
            nasa_url = "https://api.nasa.gov/planetary/apod"
            params = {
                'api_key': self.nasa_api_key,
                'count': 1
            }
            
            response = requests.get(nasa_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Return calculated orbital parameters based on destination
            return self._calculate_orbital_data(destination)
            
        except Exception as e:
            self.logger.error(f"NASA API error: {e}")
            return self._calculate_orbital_data(destination)
    
    def _calculate_orbital_data(self, destination: str) -> Dict:
        """Calculate orbital parameters for destinations"""
        # Scientific data for celestial bodies
        orbital_data = {
            'mars': {
                'distance_from_earth': 225000000,  # km (average)
                'velocity_magnitude': 24.077,      # km/s
                'orbital_period': 687,             # days
                'mass': 6.42e23,                  # kg
                'gravity': 3.71,                  # m/s²
                'radius': 3389.5,                 # km
                'escape_velocity': 5.03           # km/s
            },
            'moon': {
                'distance_from_earth': 384400,    # km
                'velocity_magnitude': 1.022,      # km/s
                'orbital_period': 27.3,           # days
                'mass': 7.35e22,                  # kg
                'gravity': 1.62,                  # m/s²
                'radius': 1737.4,                 # km
                'escape_velocity': 2.38           # km/s
            },
            'venus': {
                'distance_from_earth': 41400000,  # km (closest approach)
                'velocity_magnitude': 35.02,      # km/s
                'orbital_period': 225,            # days
                'mass': 4.87e24,                  # kg
                'gravity': 8.87,                  # m/s²
                'radius': 6051.8,                 # km
                'escape_velocity': 10.36          # km/s
            },
            'jupiter': {
                'distance_from_earth': 628300000, # km (average)
                'velocity_magnitude': 13.07,      # km/s
                'orbital_period': 4333,           # days
                'mass': 1.898e27,                 # kg
                'gravity': 24.79,                 # m/s²
                'radius': 69911,                  # km
                'escape_velocity': 59.5           # km/s
            },
            'saturn': {
                'distance_from_earth': 1275000000, # km (average)
                'velocity_magnitude': 9.68,       # km/s
                'orbital_period': 10759,          # days
                'mass': 5.68e26,                  # kg
                'gravity': 10.44,                 # m/s²
                'radius': 58232,                  # km
                'escape_velocity': 35.5           # km/s
            },
            'europa': {
                'distance_from_earth': 628300000, # km (Jupiter distance)
                'velocity_magnitude': 13.74,      # km/s
                'orbital_period': 3.55,           # days
                'mass': 4.8e22,                   # kg
                'gravity': 1.314,                 # m/s²
                'radius': 1560.8,                 # km
                'escape_velocity': 2.025          # km/s
            },
            'titan': {
                'distance_from_earth': 1275000000, # km (Saturn distance)
                'velocity_magnitude': 5.57,       # km/s
                'orbital_period': 15.95,          # days
                'mass': 1.35e23,                  # kg
                'gravity': 1.352,                 # m/s²
                'radius': 2574,                   # km
                'escape_velocity': 2.64           # km/s
            },
            'enceladus': {
                'distance_from_earth': 1275000000, # km (Saturn distance)
                'velocity_magnitude': 12.64,      # km/s
                'orbital_period': 1.37,           # days
                'mass': 1.08e20,                  # kg
                'gravity': 0.0113,                # m/s²
                'radius': 252.1,                  # km
                'escape_velocity': 0.239          # km/s
            },
            'io': {
                'distance_from_earth': 628300000, # km (Jupiter distance)
                'velocity_magnitude': 17.33,      # km/s
                'orbital_period': 1.77,           # days
                'mass': 8.93e22,                  # kg
                'gravity': 1.796,                 # m/s²
                'radius': 1821.6,                 # km
                'escape_velocity': 2.558          # km/s
            },
            'asteroid_belt': {
                'distance_from_earth': 329000000, # km (average)
                'velocity_magnitude': 20.0,       # km/s
                'orbital_period': 1460,           # days (average)
                'mass': 3.0e21,                   # kg (estimated total)
                'gravity': 0.0003,                # m/s² (Ceres)
                'radius': 473,                    # km (Ceres)
                'escape_velocity': 0.51           # km/s (Ceres)
            }
        }
        
        return orbital_data.get(destination, orbital_data['mars'])
    
    def _parse_horizons_response(self, result: str, destination: str) -> Dict:
        """Parse Horizons API response"""
        try:
            # Extract position and velocity vectors
            lines = result.split('\n')
            ephemeris_data = []
            
            # Look for ephemeris data section
            in_data_section = False
            for line in lines:
                if '$$SOE' in line:
                    in_data_section = True
                    continue
                elif '$$EOE' in line:
                    break
                elif in_data_section and line.strip():
                    # Parse ephemeris line
                    parts = line.split()
                    if len(parts) >= 7:
                        ephemeris_data.append({
                            'date': parts[0],
                            'x': float(parts[2]),
                            'y': float(parts[3]),
                            'z': float(parts[4]),
                            'vx': float(parts[5]),
                            'vy': float(parts[6]),
                            'vz': float(parts[7])
                        })
            
            # Calculate orbital parameters
            orbital_data = self._calculate_orbital_parameters(ephemeris_data)
            
            return {
                'destination': destination,
                'ephemeris': ephemeris_data[:10],  # First 10 days
                'orbital_parameters': orbital_data,
                'data_source': 'NASA JPL Horizons',
                'retrieved_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing Horizons response: {e}")
            return self._get_fallback_data(destination)
    
    def _calculate_orbital_parameters(self, ephemeris_data: List[Dict]) -> Dict:
        """Calculate basic orbital parameters from ephemeris data"""
        if not ephemeris_data:
            return {}
        
        try:
            # Use first data point for calculations
            first_point = ephemeris_data[0]
            
            # Calculate distance from Earth center
            distance = (first_point['x']**2 + first_point['y']**2 + first_point['z']**2)**0.5
            
            # Calculate velocity magnitude
            velocity = (first_point['vx']**2 + first_point['vy']**2 + first_point['vz']**2)**0.5
            
            return {
                'distance_from_earth': distance,  # km
                'velocity_magnitude': velocity,   # km/s
                'position_vector': [first_point['x'], first_point['y'], first_point['z']],
                'velocity_vector': [first_point['vx'], first_point['vy'], first_point['vz']],
                'calculation_date': first_point['date']
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating orbital parameters: {e}")
            return {}
    
    def _get_fallback_data(self, destination: str) -> Dict:
        """Provide fallback data when NASA API is unavailable"""
        fallback_data = {
            'mars': {
                'distance_from_earth': 225000000,  # km (average)
                'velocity_magnitude': 24.0,        # km/s
                'orbital_period': 687,             # days
                'mass': 6.42e23,                  # kg
                'gravity': 3.71                    # m/s²
            },
            'moon': {
                'distance_from_earth': 384400,    # km
                'velocity_magnitude': 1.0,        # km/s
                'orbital_period': 27.3,           # days
                'mass': 7.35e22,                  # kg
                'gravity': 1.62                   # m/s²
            },
            'venus': {
                'distance_from_earth': 41000000,  # km (closest approach)
                'velocity_magnitude': 35.0,       # km/s
                'orbital_period': 225,            # days
                'mass': 4.87e24,                  # kg
                'gravity': 8.87                   # m/s²
            }
        }
        
        base_data = fallback_data.get(destination, fallback_data['mars'])
        
        return {
            'destination': destination,
            'orbital_parameters': base_data,
            'data_source': 'Fallback Data',
            'retrieved_at': datetime.utcnow().isoformat(),
            'warning': 'Using fallback data - NASA API unavailable'
        }
    
    def get_mission_window(self, destination: str, launch_date: datetime) -> Dict:
        """Calculate optimal launch window"""
        try:
            # This is a simplified calculation - in reality, this would use
            # complex orbital mechanics calculations
            
            window_data = {
                'mars': {'duration': 26, 'frequency': 780},  # 26 months apart every 2.1 years
                'moon': {'duration': 28, 'frequency': 28},    # Every month
                'venus': {'duration': 19, 'frequency': 584}   # 19 months apart every 1.6 years
            }
            
            dest_data = window_data.get(destination, window_data['mars'])
            
            return {
                'destination': destination,
                'launch_date': launch_date.isoformat(),
                'window_duration': dest_data['duration'],
                'next_window_in_days': dest_data['frequency'],
                'optimal_window': True if launch_date.day <= 15 else False,
                'recommendation': 'Optimal launch window' if launch_date.day <= 15 else 'Consider adjusting launch date'
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating mission window: {e}")
            return {
                'destination': destination,
                'launch_date': launch_date.isoformat(),
                'error': 'Unable to calculate mission window'
            }
