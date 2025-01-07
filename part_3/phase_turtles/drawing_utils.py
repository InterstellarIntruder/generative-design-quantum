import turtle
import numpy as np

class QuantumVisualizer:
    def __init__(self):
        """Initialize the turtle-based visualization system"""
        self.t = turtle.Turtle()
        self.t.speed(0)  # Fastest drawing speed
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.t.pensize(2)

    def visualize_step(self, probability, phase, max_step_length=50):
        """
        Visualize a quantum step using turtle graphics.
        
        Args:
            probability (float): Probability value (0-1)
            phase (float): Phase angle in radians
            max_step_length (int): Maximum length of a step
        """
        # Map probability to step length
        step_length = max_step_length * probability
        
        # Map phase to rotation angle (0 to 360 degrees)
        rotation = np.degrees(phase) % 360
        
        # Color mapping based on phase (hue) and probability (brightness)
        hue = (phase / (2 * np.pi))
        rgb = self._hsv_to_rgb(hue, 1.0, probability)
        color = f"#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"
        self.t.pencolor(color)
        
        # Console visualization
        self._print_status(phase, probability, rotation)
        
        self.t.right(rotation)
        self.t.forward(step_length)

    def _print_status(self, phase, probability, rotation):
        """Print the current status to console with visual indicators"""
        phase_bar = "█" * int(20 * (phase / (2 * np.pi)))
        prob_bar = "█" * int(20 * probability)
        direction = "→" if rotation < 45 or rotation > 315 else \
                   "↗" if rotation < 135 else \
                   "←" if rotation < 225 else \
                   "↙" if rotation < 315 else "→"
        print(f"\rPhase: {phase:6.2f} [{phase_bar:<20}] "
              f"Prob: {probability:6.2f} [{prob_bar:<20}] "
              f"Angle: {rotation:6.1f}° {direction}", end="")

    def _hsv_to_rgb(self, h, s, v):
        """
        Convert HSV color values to RGB.
        
        Args:
            h (float): Hue (0-1)
            s (float): Saturation (0-1)
            v (float): Value/Brightness (0-1)
            
        Returns:
            tuple: (r, g, b) values from 0-1
        """
        if s == 0.0:
            return (v, v, v)
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)

    def setup_turtle(self):
        """Setup initial turtle position"""
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()

    def cleanup(self):
        """Clean up the visualization"""
        self.screen.exitonclick()
