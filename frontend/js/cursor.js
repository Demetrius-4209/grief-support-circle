class CursorTrail {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.particles = [];
        this.cursor = { x: 0, y: 0 };
        
        this.init();
    }

    init() {
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '9999';
        document.body.appendChild(this.canvas);

        this.resize();
        window.addEventListener('resize', () => this.resize());
        window.addEventListener('mousemove', (e) => this.onMouseMove(e));

        this.animate();
    }

    resize() {
        this.width = window.innerWidth;
        this.height = window.innerHeight;
        this.canvas.width = this.width;
        this.canvas.height = this.height;
    }

    onMouseMove(e) {
        this.cursor.x = e.clientX;
        this.cursor.y = e.clientY;
        this.addParticle(this.cursor.x, this.cursor.y);
    }

    addParticle(x, y) {
        this.particles.push({
            x: x,
            y: y,
            radius: Math.random() * 2 + 1,
            life: 1,
            color: Math.random() > 0.5 ? '56, 189, 248' : '168, 85, 247' // Cyan or Violet
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.width, this.height);

        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${p.color}, ${p.life})`;
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = `rgba(${p.color}, ${p.life})`;
            this.ctx.fill();

            p.life -= 0.02; // Fade speed
            p.radius *= 0.95; // Shrink speed

            if (p.life <= 0) {
                this.particles.splice(i, 1);
                i--;
            }
        }

        requestAnimationFrame(() => this.animate());
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new CursorTrail();
});
