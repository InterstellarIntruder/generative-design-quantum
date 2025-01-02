import turtle

class TurtleDrawer:
    def __init__(self, color="cyan"):
        """
        Initialize the turtle graphics system for quantum state visualization.
        
        Args:
            color: Color of the turtle's pen (default: cyan)
        """
        self.t = turtle.Turtle()
        self.t.speed(0)  # Set fastest speed
        self.screen = turtle.Screen()
        
        # Set up black background and neon colors
        self.screen.bgcolor("black")
        self.t.pensize(2)
        self.t.pencolor(color)  # Set the pen color
        
        # Initialize recording attributes
        self.frames = []
        self.is_recording = False

    def setup_initial_position(self, x: float, y: float):
        """
        Move turtle to starting position without drawing.
        
        Args:
            x: X-coordinate
            y: Y-coordinate
        """
        self.t.penup()
        self.t.goto(x, y)
        self.t.pendown()

    def rotate(self, angle: float):
        """
        Rotate the turtle by specified angle.
        
        Args:
            angle: Rotation angle in degrees
        """
        self.t.right(angle)

    def move_and_draw(self, heading: float, distance: float):
        """
        Move the turtle while drawing, maintaining the trail.
        
        Args:
            heading: Direction to move in degrees
            distance: Distance to move
        """
        self.t.setheading(heading)
        self.t.pendown()  # Ensure we're drawing
        self.t.forward(distance)

    def draw_quantum_paths(self, prob_0: float, prob_1: float, distance: float):
        """
        Visualize quantum superposition by drawing two possible paths.
        
        Args:
            prob_0: Probability of |0⟩ state
            prob_1: Probability of |1⟩ state
            distance: Length of each path
        """
        # Store current position and heading for returning later
        original_pos = self.t.position()
        original_heading = self.t.heading()
        original_color = self.t.pencolor()  # Store the turtle's assigned color
        
        # Draw the actual path taken so far (in turtle's assigned color)
        self.t.pensize(2)  # Make the main path slightly thicker
        self.t.pendown()  # Ensure pen is down for continuous line
        self.t.forward(distance/2)  # Draw to the midpoint
        
        # Remember midpoint position
        midpoint = self.t.position()
        
        # Draw |0⟩ state path (45 degrees, darker magenta)
        self.t.pensize(1)  # Thinner line for quantum paths
        self.t.pencolor(0.4, 0, 0.4)  # Darker magenta
        self.t.setheading(original_heading + 45)
        self.t.forward(distance)
        
        # Return to midpoint for second path
        self.t.penup()
        self.t.goto(midpoint)
        self.t.pendown()
        
        # Draw |1⟩ state path (-45 degrees, darker yellow)
        self.t.pencolor(0.4, 0.4, 0)  # Darker yellow
        self.t.setheading(original_heading - 45)
        self.t.forward(distance)
        
        # Continue the main path from midpoint
        self.t.penup()
        self.t.goto(midpoint)
        self.t.pencolor(original_color)  # Return to turtle's assigned color
        self.t.pensize(2)  # Thicker line for main path
        self.t.pendown()  # Ensure pen is down for continuous line
        
        # Move to the end of the most probable path while drawing
        if prob_0 > prob_1:
            self.move_and_draw(original_heading + 45, distance/2)
        else:
            self.move_and_draw(original_heading - 45, distance/2)

    def save_drawing_as_png(self, filename: str = "quantum_turtle_art.png"):
        """
        Save the turtle drawing as a PNG file.
        Requires PIL (Python Imaging Library).
        
        Args:
            filename: Name of the file to save (default: quantum_turtle_art.png)
        """
        try:
            from PIL import Image, ImageGrab
            
            # Ensure all turtle graphics are rendered
            self.screen.update()
            
            # Get the canvas and its root window
            canvas = self.screen.getcanvas()
            root = canvas.winfo_toplevel()
            
            # Get the window position and size
            x = root.winfo_rootx() + canvas.winfo_x()
            y = root.winfo_rooty() + canvas.winfo_y()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Capture the image
            image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            image.save(filename)
            print(f"Drawing saved as {filename}")
        except ImportError:
            print("PIL (Python Imaging Library) is required for PNG export.")
            print("Install it with: pip install Pillow")

    def start_gif_recording(self):
        """
        Start recording frames for GIF creation.
        """
        self.frames = []
        self.is_recording = True

    def capture_frame(self):
        """
        Capture current frame for GIF.
        """
        if not self.is_recording:
            return
            
        try:
            from PIL import Image, ImageGrab
            
            # Ensure all turtle graphics are rendered
            self.screen.update()
            
            # Get the canvas and its root window
            canvas = self.screen.getcanvas()
            root = canvas.winfo_toplevel()
            
            # Get the window position and size
            x = root.winfo_rootx() + canvas.winfo_x()
            y = root.winfo_rooty() + canvas.winfo_y()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Capture the frame
            frame = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            self.frames.append(frame)
        except ImportError:
            print("PIL (Python Imaging Library) is required for GIF creation.")
            print("Install it with: pip install Pillow")

    def save_as_gif(self, filename: str = "quantum_turtle_animation.gif", duration: int = 100):
        """
        Save recorded frames as GIF.
        
        Args:
            filename: Name of the GIF file
            duration: Duration for each frame in milliseconds
        """
        if not self.frames:
            print("No frames recorded. Call start_gif_recording() first.")
            return
            
        try:
            self.frames[0].save(
                filename,
                save_all=True,
                append_images=self.frames[1:],
                optimize=True,
                duration=duration,
                loop=0
            )
            print(f"Animation saved as {filename}")
        except Exception as e:
            print(f"Error saving GIF: {e}") 