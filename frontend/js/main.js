// Onboarding form submission
document.getElementById('onboardingForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        grief_type: formData.get('grief_type'),
        time_frame: formData.get('time_frame'),
        need: formData.get('need')
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/onboard', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        // Store session ID
        localStorage.setItem('session_id', result.session_id);
        
        // Redirect to waiting room
        window.location.href = 'waiting.html';
    } catch (error) {
        alert('Something went wrong. Please try again.');
    }
});