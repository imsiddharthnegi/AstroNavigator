// AstroMissionSim - Mission Form JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeMissionForm();
});

function initializeMissionForm() {
    const form = document.getElementById('mission-form');
    const previewContainer = document.getElementById('mission-preview');
    
    if (!form) return;
    
    // Form elements
    const nameField = document.getElementById('name');
    const descriptionField = document.getElementById('description');
    const destinationField = document.getElementById('destination');
    const launchDateField = document.getElementById('launch_date');
    const durationField = document.getElementById('mission_duration');
    const crewSizeField = document.getElementById('crew_size');
    const spacecraftField = document.getElementById('spacecraft_type');
    const payloadField = document.getElementById('payload_mass');
    const fuelField = document.getElementById('fuel_requirements');
    
    // Validation rules
    const validators = {
        name: (value) => value.length >= 3 && value.length <= 200,
        destination: (value) => value !== '',
        launch_date: (value) => {
            const date = new Date(value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            return date >= today;
        },
        mission_duration: (value) => {
            const num = parseInt(value);
            return num >= 1 && num <= 3650;
        },
        crew_size: (value) => {
            const num = parseInt(value);
            return num >= 0 && num <= 20;
        },
        spacecraft_type: (value) => value !== '',
        payload_mass: (value) => {
            if (value === '') return true;
            const num = parseFloat(value);
            return num >= 0 && num <= 100000;
        },
        fuel_requirements: (value) => {
            if (value === '') return true;
            const num = parseFloat(value);
            return num >= 0 && num <= 1000000;
        }
    };
    
    // Real-time validation
    const fields = [nameField, destinationField, launchDateField, durationField, crewSizeField, spacecraftField, payloadField, fuelField];
    
    fields.forEach(field => {
        if (field) {
            field.addEventListener('input', AstroUtils.debounce(() => {
                validateField(field);
                updatePreview();
            }, 300));
            
            field.addEventListener('blur', () => {
                validateField(field);
                updatePreview();
            });
        }
    });
    
    // Validate individual field
    function validateField(field) {
        const fieldName = field.name;
        const validator = validators[fieldName];
        
        if (validator) {
            return AstroUtils.validateField(field, validator);
        }
        
        return true;
    }
    
    // Update mission preview
    function updatePreview() {
        if (!previewContainer) return;
        
        const formData = getFormData();
        
        if (Object.values(formData).every(value => value === '')) {
            previewContainer.innerHTML = '<p class="text-muted">Fill in the form to see mission preview</p>';
            return;
        }
        
        const preview = generatePreview(formData);
        previewContainer.innerHTML = preview;
    }
    
    // Get form data
    function getFormData() {
        return {
            name: nameField ? nameField.value : '',
            description: descriptionField ? descriptionField.value : '',
            destination: destinationField ? destinationField.value : '',
            launch_date: launchDateField ? launchDateField.value : '',
            mission_duration: durationField ? durationField.value : '',
            crew_size: crewSizeField ? crewSizeField.value : '',
            spacecraft_type: spacecraftField ? spacecraftField.value : '',
            payload_mass: payloadField ? payloadField.value : '',
            fuel_requirements: fuelField ? fuelField.value : ''
        };
    }
    
    // Generate preview HTML
    function generatePreview(data) {
        let html = '<div class="mission-preview-content">';
        
        if (data.name) {
            html += `<h6 class="text-primary"><i class="fas fa-rocket me-2"></i>${data.name}</h6>`;
        }
        
        if (data.description) {
            html += `<p class="small text-muted">${data.description}</p>`;
        }
        
        html += '<div class="row">';
        
        if (data.destination) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Destination:</small><br>
                    <span class="badge bg-info">${formatDestination(data.destination)}</span>
                </div>
            `;
        }
        
        if (data.launch_date) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Launch Date:</small><br>
                    <span><i class="fas fa-calendar me-1"></i>${AstroUtils.formatDate(data.launch_date)}</span>
                </div>
            `;
        }
        
        if (data.mission_duration) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Duration:</small><br>
                    <span><i class="fas fa-clock me-1"></i>${AstroUtils.formatDuration(parseInt(data.mission_duration))}</span>
                </div>
            `;
        }
        
        if (data.crew_size) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Crew:</small><br>
                    <span><i class="fas fa-users me-1"></i>${data.crew_size} ${data.crew_size === '1' ? 'person' : 'people'}</span>
                </div>
            `;
        }
        
        if (data.spacecraft_type) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Spacecraft:</small><br>
                    <span><i class="fas fa-shuttle-space me-1"></i>${formatSpacecraft(data.spacecraft_type)}</span>
                </div>
            `;
        }
        
        if (data.payload_mass) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Payload:</small><br>
                    <span><i class="fas fa-weight me-1"></i>${AstroUtils.formatNumber(data.payload_mass)} kg</span>
                </div>
            `;
        }
        
        if (data.fuel_requirements) {
            html += `
                <div class="col-md-6 mb-2">
                    <small class="text-muted">Fuel:</small><br>
                    <span><i class="fas fa-gas-pump me-1"></i>${AstroUtils.formatNumber(data.fuel_requirements)} kg</span>
                </div>
            `;
        }
        
        html += '</div>';
        
        // Add mission complexity indicator
        const complexity = calculateComplexity(data);
        html += `
            <div class="mt-3">
                <small class="text-muted">Mission Complexity:</small><br>
                <div class="progress" style="height: 20px;">
                    <div class="progress-bar bg-${complexity.color}" role="progressbar" style="width: ${complexity.percentage}%">
                        ${complexity.level}
                    </div>
                </div>
            </div>
        `;
        
        html += '</div>';
        
        return html;
    }
    
    // Format destination name
    function formatDestination(destination) {
        return destination.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    // Format spacecraft name
    function formatSpacecraft(spacecraft) {
        return spacecraft.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    // Calculate mission complexity
    function calculateComplexity(data) {
        let score = 0;
        
        // Destination complexity
        const destinationScores = {
            'moon': 1,
            'mars': 3,
            'venus': 2,
            'jupiter': 4,
            'saturn': 5,
            'asteroid_belt': 3,
            'europa': 4,
            'titan': 5,
            'enceladus': 4,
            'io': 4
        };
        
        if (data.destination) {
            score += destinationScores[data.destination] || 2;
        }
        
        // Duration complexity
        if (data.mission_duration) {
            const duration = parseInt(data.mission_duration);
            if (duration > 1000) score += 3;
            else if (duration > 500) score += 2;
            else if (duration > 100) score += 1;
        }
        
        // Crew complexity
        if (data.crew_size) {
            const crew = parseInt(data.crew_size);
            if (crew > 10) score += 3;
            else if (crew > 5) score += 2;
            else if (crew > 0) score += 1;
        }
        
        // Payload complexity
        if (data.payload_mass) {
            const payload = parseFloat(data.payload_mass);
            if (payload > 50000) score += 3;
            else if (payload > 10000) score += 2;
            else if (payload > 1000) score += 1;
        }
        
        // Determine complexity level
        let level, color, percentage;
        
        if (score <= 3) {
            level = 'Simple';
            color = 'success';
            percentage = 25;
        } else if (score <= 6) {
            level = 'Moderate';
            color = 'warning';
            percentage = 50;
        } else if (score <= 9) {
            level = 'Complex';
            color = 'danger';
            percentage = 75;
        } else {
            level = 'Extreme';
            color = 'danger';
            percentage = 100;
        }
        
        return { level, color, percentage };
    }
    
    // Form submission handling
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate all fields
        fields.forEach(field => {
            if (field && !validateField(field)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            AstroUtils.showToast('Please fix the errors in the form', 'danger');
            return;
        }
        
        // Show loading state
        const submitBtn = form.querySelector('input[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.value = 'Creating Mission...';
        }
    });
    
    // Smart defaults based on destination
    if (destinationField) {
        destinationField.addEventListener('change', function() {
            const destination = this.value;
            setSmartDefaults(destination);
        });
    }
    
    // Set smart defaults based on destination
    function setSmartDefaults(destination) {
        const defaults = {
            'moon': {
                duration: 14,
                crew: 2,
                spacecraft: 'artemis'
            },
            'mars': {
                duration: 687,
                crew: 4,
                spacecraft: 'orion'
            },
            'venus': {
                duration: 365,
                crew: 3,
                spacecraft: 'orion'
            },
            'jupiter': {
                duration: 2000,
                crew: 0,
                spacecraft: 'custom'
            },
            'saturn': {
                duration: 2500,
                crew: 0,
                spacecraft: 'custom'
            }
        };
        
        const destDefaults = defaults[destination];
        if (destDefaults) {
            if (durationField && !durationField.value) {
                durationField.value = destDefaults.duration;
            }
            if (crewSizeField && !crewSizeField.value) {
                crewSizeField.value = destDefaults.crew;
            }
            if (spacecraftField && !spacecraftField.value) {
                spacecraftField.value = destDefaults.spacecraft;
            }
        }
        
        updatePreview();
    }
    
    // Initialize with current values
    updatePreview();
}

// Launch window calculator
function calculateLaunchWindow(destination, launchDate) {
    const windows = {
        'mars': {
            optimal: [3, 4, 5], // March, April, May
            frequency: 26 // months
        },
        'venus': {
            optimal: [1, 2, 11, 12], // Jan, Feb, Nov, Dec
            frequency: 19 // months
        },
        'jupiter': {
            optimal: [6, 7, 8], // June, July, August
            frequency: 13 // months
        }
    };
    
    const date = new Date(launchDate);
    const month = date.getMonth() + 1;
    const destWindow = windows[destination];
    
    if (destWindow) {
        const isOptimal = destWindow.optimal.includes(month);
        return {
            optimal: isOptimal,
            message: isOptimal ? 'Optimal launch window' : 'Consider adjusting launch date for better efficiency'
        };
    }
    
    return {
        optimal: true,
        message: 'Launch window analysis not available for this destination'
    };
}

// Export for use in other files
window.MissionForm = {
    calculateLaunchWindow
};
