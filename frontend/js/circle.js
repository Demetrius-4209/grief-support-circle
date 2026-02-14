const circleId = localStorage.getItem('circle_id');

// Fetch circle info
fetch(`http://localhost:5000/api/circle-info/${circleId}`)
    .then(r => r.json())
    .then(data => {
        // Initialize Jitsi
        const domain = 'meet.jit.si';
        const options = {
            roomName: data.jitsi_room,
            width: '100%',
            height: 600,
            parentNode: document.querySelector('#jitsi-container'),
            configOverwrite: {
                startWithAudioMuted: false,
                startWithVideoMuted: false,
            },
            interfaceConfigOverwrite: {
                TOOLBAR_BUTTONS: ['microphone', 'camera', 'hangup'],
            }
        };
        
        const api = new JitsiMeetExternalAPI(domain, options);
        
        // Simple 20-minute timer
        let timeLeft = 20 * 60; // 20 minutes in seconds
        const timerElement = document.getElementById('timer');
        
        setInterval(() => {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft === 0) {
                window.location.href = 'garden.html';
            }
        }, 1000);
    });

document.getElementById('endCircle').addEventListener('click', () => {
    window.location.href = 'garden.html';
});