import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import numpy as np
import threading
import multiprocessing
from texture_generator import TextureGenerator, NoiseTypeEnum
from noise import snoise2

# Theme Colors
THEME_COLOR = "#2c3e50"  # Dark blue-gray
ACCENT_COLOR = "#3498db"  # Bright blue
ACCENT_COLOR_DARK = "#2980b9"  # Darker blue
TEXT_COLOR = "#ecf0f1"  # Off-white
BACKGROUND_COLOR = THEME_COLOR  # Slightly lighter than theme color
CANVAS_BG = "#1e272e"  # Dark blue-gray for canvas
BUTTON_COLOR = "#3498db"  # Bright blue
SLIDER_COLOR = "#3498db"  # Bright blue
SUCCESS_COLOR = "#2ecc71"  # Green
WARNING_COLOR = "#f39c12"  # Orange
ERROR_COLOR = "#e74c3c"  # Red

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ModernStyle:
    """Creates a modern style for tkinter widgets"""
    def __init__(self, root):
        self.style = ttk.Style()
        
        # Configure the basic theme
        self.style.theme_use('clam')  # Use 'clam' as base theme
        
        # Configure the general appearance
        self.style.configure('.',
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR,
            font=('Segoe UI', 10),
            borderwidth=1)
        
        # Configure Frame
        self.style.configure('TFrame', background=BACKGROUND_COLOR)
        
        # Configure LabelFrame
        self.style.configure('TLabelframe', 
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR)
        self.style.configure('TLabelframe.Label', 
            background=BACKGROUND_COLOR,
            foreground=ACCENT_COLOR,
            font=('Segoe UI', 10, 'bold'))
        
        # Configure Label
        self.style.configure('TLabel', 
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR)
        
        # Configure Button
        self.style.configure('TButton', 
            background=BUTTON_COLOR,
            foreground=TEXT_COLOR,
            padding=(10, 5),
            relief='flat')
        self.style.map('TButton',
            background=[('active', ACCENT_COLOR_DARK), ('disabled', '#7f8c8d')],
            foreground=[('disabled', '#95a5a6')])
        
        # Success Button
        self.style.configure('Success.TButton', 
            background=SUCCESS_COLOR,
            foreground=TEXT_COLOR)
        self.style.map('Success.TButton',
            background=[('active', '#27ae60')])
        
        # Warning Button
        self.style.configure('Warning.TButton', 
            background=WARNING_COLOR,
            foreground=TEXT_COLOR)
        self.style.map('Warning.TButton',
            background=[('active', '#d35400')])
        
        # Configure Entry
        self.style.configure('TEntry', 
            fieldbackground=THEME_COLOR,
            foreground=TEXT_COLOR,
            padding=5)
        
        # Configure Combobox
        self.style.map('TCombobox',
            fieldbackground=[('readonly', THEME_COLOR)],
            background=[('readonly', THEME_COLOR)],
            foreground=[('readonly', TEXT_COLOR)])
        
        # Configure Notebook
        self.style.configure('TNotebook', 
            background=THEME_COLOR,
            tabmargins=[2, 5, 2, 0])
        self.style.configure('TNotebook.Tab', 
            background=THEME_COLOR,
            foreground=TEXT_COLOR,
            padding=[10, 2])
        self.style.map('TNotebook.Tab',
            background=[('selected', ACCENT_COLOR)],
            foreground=[('selected', TEXT_COLOR)])
            
        # Configure Scale (Slider)
        self.style.configure('Horizontal.TScale', 
            troughcolor=THEME_COLOR,
            background=SLIDER_COLOR)
        
        # Configure Progressbar
        self.style.configure('Horizontal.TProgressbar', 
            troughcolor=THEME_COLOR,
            background=ACCENT_COLOR)
        
        # Configure Radiobutton
        self.style.configure('TRadiobutton', 
            background=BACKGROUND_COLOR,
            foreground=TEXT_COLOR)
        self.style.map('TRadiobutton',
            background=[('active', BACKGROUND_COLOR)],
            foreground=[('active', ACCENT_COLOR)])

class TextureGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("voxmapper v1.3")
        self.root.geometry("1350x1050")
        

         # Apply the modern style
        self.style = ModernStyle(root)
        
        # Configure the root window background
        self.root.configure(bg=THEME_COLOR)
        
        # Create an animation frame counter for effects
        self.animation_frame = 0
        
        # Initialize texture generator
        self.generator = TextureGenerator()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        # Create the header
        self._create_header()  # Call the new header method
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Create noise tab
        self.noise_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.noise_tab, text="Noise Generation")
        
        self.vars = {
            "noise_size": tk.IntVar(value=512),
            "persistence": tk.DoubleVar(value=0.6),
            "scale": tk.DoubleVar(value=150.0),
            "seed": tk.IntVar(value=42),
            "min_height": tk.DoubleVar(value=1.0),  # Changed to tk.DoubleVar
            "max_height": tk.DoubleVar(value=0.5),
            "noise_type": tk.StringVar(value="perlin"),
            "octaves": tk.IntVar(value=7),
            "lacunarity": tk.DoubleVar(value=2.0),
            "height_scale": tk.IntVar(value=255),
            "grass_amount": tk.IntVar(value=0),
            "special_value": tk.IntVar(value=0),
            "vignette_strength": tk.DoubleVar(value=0.0),
            "vignette_radius": tk.DoubleVar(value=0.5),
        }

        self.vars.update({
            "grass_noise_type": tk.StringVar(value="perlin"),  # Default noise type for grass
            "grass_octaves": tk.IntVar(value=5),  # Default octaves for grass noise
            "grass_persistence": tk.DoubleVar(value=0.5),  # Default persistence for grass noise
            "grass_scale": tk.DoubleVar(value=50.0),  # Default scale for grass noise
            "perlin_noise_amount": tk.DoubleVar(value=0.5),  # Default value for Perlin noise amount
            "simple_noise_amount": tk.DoubleVar(value=0.5),  # Default value for simple noise amount
            "noise_type": tk.StringVar(value="perlin"),  # Default noise type
            "fractal_noise_amount": tk.DoubleVar(value=0.5),  # Default value for fractal noise amount
            "use_noise_grass": tk.BooleanVar(value=False),  # Toggle for noise-based grass
            "grass_noise_scale": tk.DoubleVar(value=50.0),  # Scale for grass noise
            "grass_noise_octaves": tk.IntVar(value=4),      # Octaves for grass noise
            "grass_noise_persistence": tk.DoubleVar(value=0.5),  # Persistence for grass noise
            "grass_density": tk.DoubleVar(value=0.5),       # Grass density threshold for noise-based grass
            "noise_grass_density": tk.DoubleVar(value=0.5)  # Grass density threshold for noise-based grass
        })

        self.slider_active = {}
        
        # Create controls and preview for noise tab
        self._create_noise_controls()
        self._create_noise_preview()

        # Create grass map tab
        self._create_grass_map_tab()
        
        # Initial preview update
        self.update_noise_preview()

    def _create_styled_canvas(self, parent, width=600, height=600):
        """Creates a styled canvas with a nice background grid pattern"""
        # Create a frame to hold the canvas
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(parent, bg=THEME_COLOR)
        
        # Create the canvas with a dark background
        canvas = tk.Canvas(canvas_frame, width=width, height=height, bg=CANVAS_BG, 
                        highlightthickness=1, highlightbackground=ACCENT_COLOR_DARK)
        
        # Add a subtle grid pattern
        grid_size = 20
        for i in range(0, width, grid_size):
            canvas.create_line(i, 0, i, height, fill="#3a4b5c", width=1, dash=(1, 3))
        for i in range(0, height, grid_size):
            canvas.create_line(0, i, width, i, fill="#3a4b5c", width=1, dash=(1, 3))
        
        # Add corner marks
        corner_size = 10
        canvas.create_line(0, 0, corner_size, 0, fill=ACCENT_COLOR, width=2)
        canvas.create_line(0, 0, 0, corner_size, fill=ACCENT_COLOR, width=2)
        canvas.create_line(width, 0, width-corner_size, 0, fill=ACCENT_COLOR, width=2)
        canvas.create_line(width, 0, width, corner_size, fill=ACCENT_COLOR, width=2)
        canvas.create_line(0, height, corner_size, height, fill=ACCENT_COLOR, width=2)
        canvas.create_line(0, height, 0, height-corner_size, fill=ACCENT_COLOR, width=2)
        canvas.create_line(width, height, width-corner_size, height, fill=ACCENT_COLOR, width=2)
        canvas.create_line(width, height, width, height-corner_size, fill=ACCENT_COLOR, width=2)
        
        canvas.pack()
        return canvas
    
    def _create_styled_button(self, parent, text, command, style='TButton', width=None, icon=None):
        """Creates a modern button with hover effect and optional icon"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)
        
        if icon:
            # If icon provided, create an icon button
            try:
                # Load the icon image (adjust the path as needed)
                icon_image = Image.open(icon).resize((16, 16))
                icon_photo = ImageTk.PhotoImage(icon_image)
                
                # Store reference to prevent garbage collection
                if not hasattr(self, 'icon_references'):
                    self.icon_references = {}
                self.icon_references[text] = icon_photo
                
                # Create button with icon and text
                button = ttk.Button(button_frame, text=" " + text, image=icon_photo, 
                                compound='left', command=command, style=style)
            except Exception as e:
                print(f"Error loading icon: {e}")
                button = ttk.Button(button_frame, text=text, command=command, style=style)
        else:
            # Create button without icon
            button = ttk.Button(button_frame, text=text, command=command, style=style)
        
        if width:
            button.configure(width=width)
        
        button.pack(fill="x")
        
        # Add hover effect
        def on_enter(event):
            button.state(['active'])
        def on_leave(event):
            button.state(['!active'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button

    def _create_header(self):
        """Creates an enhanced header with gradient effect without animation"""
        # Create header frame with gradient effect
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(side="top", pady=(10, 15), fill="x")
        
        # Initial dimensions
        gradient_height = 120
        
        # Create a canvas to display the gradient
        header_canvas = tk.Canvas(header_frame, height=gradient_height, 
                                bd=0, highlightthickness=0, bg=THEME_COLOR)
        header_canvas.pack(fill="x")
        
        # Store canvas for later reference
        self.header_canvas = header_canvas
        
        # Try to load the logo image (static, no animation)
        try:
            logo_img = Image.open("voxmapper_logo.png").resize((100, 100), Image.Resampling.LANCZOS)
            
            # Add glow effect
            glow = Image.new('RGBA', (120, 120), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow)
            # Draw a soft glow circle
            for i in range(10, 0, -1):
                alpha = int(100 / i)
                glow_draw.ellipse([10-i, 10-i, 110+i, 110+i], 
                                fill=(int(ACCENT_COLOR[1:3], 16), 
                                    int(ACCENT_COLOR[3:5], 16), 
                                    int(ACCENT_COLOR[5:7], 16), 
                                    alpha))
            
            # Composite the logo on top of the glow
            glow.paste(logo_img, (10, 10), logo_img if logo_img.mode == 'RGBA' else None)
            self.logo_image = ImageTk.PhotoImage(glow)
            has_logo = True
        except Exception as e:
            print(f"Error loading logo: {e}")
            has_logo = False
        
        # Function to update the gradient when the window resizes
        def update_gradient(event=None):
            # Get current width
            gradient_width = header_frame.winfo_width()
            if gradient_width <= 1:  # Not yet properly initialized
                gradient_width = self.root.winfo_width()
            if gradient_width <= 1:  # Still not initialized
                gradient_width = 1200  # Fallback width
                
            # Create new gradient image
            gradient_img = Image.new('RGB', (gradient_width, gradient_height), color=THEME_COLOR)
            draw = ImageDraw.Draw(gradient_img)
            
            # Draw a gradient from theme color to slightly lighter
            for y in range(gradient_height):
                # Calculate color interpolation
                r_factor = y / gradient_height
                r = int((1-r_factor) * int(THEME_COLOR[1:3], 16) + r_factor * int(BACKGROUND_COLOR[1:3], 16))
                g = int((1-r_factor) * int(THEME_COLOR[3:5], 16) + r_factor * int(BACKGROUND_COLOR[3:5], 16))
                b = int((1-r_factor) * int(THEME_COLOR[5:7], 16) + r_factor * int(BACKGROUND_COLOR[5:7], 16))
                color = f"#{r:02x}{g:02x}{b:02x}"
                draw.line([(0, y), (gradient_width, y)], fill=color)
            
            # Add a subtle pattern overlay for texture
            for x in range(0, gradient_width, 20):
                for y in range(0, gradient_height, 20):
                    # Draw subtle dots
                    dot_color = f"#{min(int(THEME_COLOR[1:3], 16) + 10, 255):02x}{min(int(THEME_COLOR[3:5], 16) + 10, 255):02x}{min(int(THEME_COLOR[5:7], 16) + 10, 255):02x}"
                    draw.ellipse([x, y, x+2, y+2], fill=dot_color)
            
            # Apply a slight blur for a smoother appearance
            gradient_img = gradient_img.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Convert to PhotoImage and keep a reference
            self.header_bg = ImageTk.PhotoImage(gradient_img)
            
            # Clear canvas and redraw everything
            header_canvas.delete("all")
            
            # Background gradient
            header_canvas.create_image(0, 0, anchor="nw", image=self.header_bg)
            
            # Logo
            if hasattr(self, 'logo_image') and has_logo:
                header_canvas.create_image(50, gradient_height//2, image=self.logo_image)
            else:
                # Fallback text if logo wasn't loaded
                header_canvas.create_text(50, gradient_height//2, text="VM", 
                                        fill=ACCENT_COLOR, font=("Arial", 36, "bold"))
            
            # Title text
            header_canvas.create_text(200, gradient_height//2 - 15, text="VOXMAPPER", 
                                    fill=ACCENT_COLOR, font=("Arial", 36, "bold"), 
                                    anchor="w")
            header_canvas.create_text(200, gradient_height//2 + 15, text="v1.3 by NGNT", 
                                    fill=TEXT_COLOR, font=("Arial", 16), 
                                    anchor="w")
            
            # Add a subtle separator line
            header_canvas.create_line(0, gradient_height-1, gradient_width, gradient_height-1, 
                                fill=ACCENT_COLOR_DARK, width=2)
        
        # Bind resize event
        self.root.bind("<Configure>", lambda e: update_gradient() if e.widget == self.root else None)
        
        # Initial gradient rendering
        update_gradient()
        
        return header_frame

    def _create_noise_controls(self):
        # Create left panel for controls
        scroll_frame = self._make_scrollable_tab(self.noise_tab)
        controls_frame = ttk.Frame(scroll_frame)
        controls_frame.pack(fill="both", expand=True, padx=(0, 20))
    
        # Basic settings
        basic_frame = ttk.LabelFrame(controls_frame, text="Basic Settings", padding=10)
        basic_frame.pack(fill="x", pady=5)
    
        self._create_slider(basic_frame, "Size", "noise_size", 64, 2048, 64)
        self._create_slider(basic_frame, "Persistence", "persistence", 0.1, 1.0, 0.1)
        self._create_slider(basic_frame, "Scale", "scale", 1.0, 500.0, 0.1)  # Adjusted range
        self._create_slider(basic_frame, "Seed", "seed", 0, 10000, 1)

        # Teardown heightmap settings
        heightmap_frame = ttk.LabelFrame(controls_frame, text="Teardown Heightmap Settings", padding=10)
        heightmap_frame.pack(fill="x", pady=5)

        # Add noise-based grass parameters (initially hidden)
        self.grass_noise_frame = ttk.LabelFrame(heightmap_frame, text="Grass Noise Settings", padding=5)
        self.vars["use_noise_grass"].trace_add("write", self._toggle_grass_noise_controls)

        # Create sliders for heightmap settings
        self._create_slider(heightmap_frame, "Min Height", "min_height", -1.0, 1.0, 0.1)
        self._create_slider(heightmap_frame, "Max Height", "max_height", 0.0, 2.0, 0.1)
        self._create_slider(heightmap_frame, "Height Scale", "height_scale", 1, 255, 1)  # Restored Height Scale slider
        self._create_slider(heightmap_frame, "Grass Amount", "grass_amount", 0, 255, 1)  # Restored Grass Amount slider
        self._create_slider(self.grass_noise_frame, "Scale", "grass_noise_scale", 1.0, 200.0, 0.1)
        self._create_slider(self.grass_noise_frame, "Octaves", "grass_noise_octaves", 1, 8, 1)
        self._create_slider(self.grass_noise_frame, "Persistence", "grass_noise_persistence", 0.1, 1.0, 0.1)
        self._create_slider(self.grass_noise_frame, "Density", "noise_grass_density", 0.0, 1.0, 0.01)
        self._create_slider(heightmap_frame, "Special Value", "special_value", 0, 255, 1)  # Restored Special Value slider

        # Add grass type toggle (uniform vs noise-based)
        grass_type_frame = ttk.Frame(heightmap_frame)
        grass_type_frame.pack(fill="x", pady=2)
        ttk.Label(grass_type_frame, text="Grass Type:").pack(side="left", padx=5)
        ttk.Radiobutton(grass_type_frame, text="Uniform", variable=self.vars["use_noise_grass"], value=False).pack(side="left")
        ttk.Radiobutton(grass_type_frame, text="Noise", variable=self.vars["use_noise_grass"], value=True).pack(side="left")
    
        # Add reset zoom button
        ttk.Button(basic_frame, text="Reset Zoom", command=lambda: self.vars["scale"].set(5.0)).pack(fill="x", pady=5)

        # Vignette settings
        vignette_frame = ttk.LabelFrame(controls_frame, text="Vignette Settings", padding=10)
        vignette_frame.pack(fill="x", pady=5)
        
        self._create_slider(vignette_frame, "Strength", "vignette_strength", 0.0, 1.0, 0.01)
        self._create_slider(vignette_frame, "Radius", "vignette_radius", 0.0, 1.0, 0.01)
        
        # Noise type
        noise_frame = ttk.LabelFrame(controls_frame, text="Noise Settings", padding=10)
        noise_frame.pack(fill="x", pady=5)

        # Add shape-specific controls
        shape_frame = ttk.LabelFrame(controls_frame, text="Shape Noise Settings", padding=10)
        shape_frame.pack(fill="x", pady=5)

        self.vars["shape_type"] = tk.StringVar(value="circle")
        self.vars["shape_size"] = tk.IntVar(value=10)
        self.vars["shape_spacing"] = tk.IntVar(value=5)

        # Add a combobox for selecting the grass noise type
        ttk.Label(shape_frame, text="Shape Type:").pack(side="left", padx=5)
        shape_type_combo = ttk.Combobox(shape_frame, textvariable=self.vars["shape_type"], 
                                        values=["circle", "square", "pyramid"], state="readonly")
        shape_type_combo.pack(side="left", padx=5)

        self._create_slider(shape_frame, "Shape Size", "shape_size", 1, 300, 1)
        self._create_slider(shape_frame, "Spacing", "shape_spacing", 0, 300, 1)
        
        ttk.Label(noise_frame, text="Type:").pack(side="left", padx=5)
        noise_combo = ttk.Combobox(noise_frame, textvariable=self.vars["noise_type"], 
                           values=["perlin", "fractal", "turbulence", "shape"], state="readonly")
        noise_combo.pack(side="left", padx=5)
        
        # Noise parameters
        self._create_slider(noise_frame, "Octaves", "octaves", 1, 10, 1)
        self._create_slider(noise_frame, "Lacunarity", "lacunarity", 1.0, 4.0, 0.1)
        
        # Apply and Generate buttons
        self.generate_button = ttk.Button(controls_frame, text="Generate Noise", command=self.generate_noise)
        self.generate_button.pack(fill="x", pady=10)

        # New button for generating greyscale heightmap
        self.generate_greyscale_button = ttk.Button(controls_frame, text="Generate Greyscale Heightmap", command=self.generate_greyscale_heightmap)
        self.generate_greyscale_button.pack(fill="x", pady=5)

    def _toggle_grass_noise_controls(self, *args):
        """Toggle visibility of grass noise controls based on the use_noise_grass variable."""
        if self.vars["use_noise_grass"].get():
            self.grass_noise_frame.pack(fill="x", pady=5)
        else:
            self.grass_noise_frame.pack_forget()

    def _create_slider(self, parent, label, var_name, from_, to_, resolution):
        # Check if the variable exists, if not create it with a default value
        if var_name not in self.vars:
            if isinstance(resolution, int):
                self.vars[var_name] = tk.IntVar(value=int((from_ + to_) / 2))
            else:
                self.vars[var_name] = tk.DoubleVar(value=(from_ + to_) / 2)
        
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        # Create label directly in the main frame with fixed width
        slider_label = ttk.Label(frame, text=label, anchor="w", width=15)
        slider_label.pack(side="left", padx=5)

        # Create the ttk.Scale for the slider
        slider = ttk.Scale(frame, from_=from_, to=to_, orient="horizontal", 
                        variable=self.vars[var_name], length=200)
        slider.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Create the value display entry directly in the main frame
        value_display = ttk.Entry(frame, width=8)
        value_display.pack(side="right", padx=5)
        
        # Function to update value display and color
        def update_value(*args):
            try:
                value = self.vars[var_name].get()
                value_display.delete(0, tk.END)
                if isinstance(resolution, int):
                    value_display.insert(0, str(int(value)))
                else:
                    value_display.insert(0, f"{value:.2f}")
                    
                # Change the color of the value display based on the slider's activity
                if self.slider_active.get(var_name, False):
                    value_display.configure(foreground=ACCENT_COLOR)
                else:
                    value_display.configure(foreground=TEXT_COLOR)
            except (tk.TclError, ValueError) as e:
                print(f"Error handling slider {var_name}: {e}")
                pass

        # Manual entry handling for the value display
        def on_value_change(event):
            try:
                text_value = value_display.get().strip()
                if text_value:
                    if isinstance(self.vars[var_name], tk.IntVar):
                        value = int(float(text_value))
                    else:
                        value = float(text_value)
                    
                    # Clamp value within range
                    value = max(from_, min(to_, value))
                    self.vars[var_name].set(value)

                    # Trigger update based on slider's variable
                    if var_name in ["grass_density", "perlin_noise_amount", "simple_noise_amount", "lightness"]:
                        self.update_grass_map_preview()
                    elif var_name in ["brown_threshold", "green_threshold"]:
                        self.update_colormap_preview()
                    else:
                        self.update_noise_preview()
            except (ValueError, tk.TclError):
                update_value()  # Reset to current value on invalid input

        # Bind events for manual input
        value_display.bind("<Return>", on_value_change)
        value_display.bind("<FocusOut>", on_value_change)

        # Slider press and release to handle activity state
        def on_slider_press(event):
            self.slider_active[var_name] = True
            update_value()
            
        def on_slider_release(event):
            self.slider_active[var_name] = False
            update_value()

            # Trigger appropriate updates based on variable name
            if var_name in ["grass_density", "perlin_noise_amount", "simple_noise_amount", "lightness"]:
                self.update_grass_map_preview()
            elif var_name in ["brown_threshold", "green_threshold"]:
                self.update_colormap_preview()
            else:
                self.update_noise_preview()

        # Bind slider events
        slider.bind("<ButtonPress-1>", on_slider_press)
        slider.bind("<ButtonRelease-1>", on_slider_release)

        # Track value changes and update the display
        self.vars[var_name].trace_add("write", update_value)
        
        # Initial update of value display
        update_value()

        # Add tooltip with range information
        tooltip_text = f"{label}: Range {from_} to {to_}"
        ToolTip(slider, tooltip_text)

        return slider


    def _make_scrollable_tab(self, tab):
        # Create canvas with background matching the theme
        canvas = tk.Canvas(tab, bg=BACKGROUND_COLOR, highlightthickness=0)

        # The scrollbar (ttk picks up the style from ttk.Style)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)

        # Frame that lives inside the canvas
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        # Ensure scrollregion expands as content grows
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add the scrollable frame to the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Connect canvas scroll to scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Smooth scroll on mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        scrollable_frame.bind("<Enter>", lambda _: scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel))
        scrollable_frame.bind("<Leave>", lambda _: scrollable_frame.unbind_all("<MouseWheel>"))

        # Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame


    def update_grass_map_preview(self):
        # Call the method to generate the grass map based on current settings
        self.generate_grass_map()

    def create_grass_map_data(self):
        """Generate the current grass map data array (not saving or previewing yet)."""
        size = self.vars["noise_size"].get()
        density = self.vars["grass_density"].get()
        perlin_amount = self.vars["perlin_noise_amount"].get()
        simple_amount = self.vars["simple_noise_amount"].get()
        lightness = self.vars["lightness"].get()
        
        # For smaller sizes, avoid multiprocessing
        if size < 512:
            # Generate the entire map in the main process for small maps
            grass_map_data = np.zeros((size, size), dtype=np.float32)
            for y in range(size):
                for x in range(size):
                    # Generate noise values as before
                    noise_value_perlin = snoise2(x / (50.0 * perlin_amount), 
                                            y / (50.0 * perlin_amount), 
                                            octaves=5, 
                                            persistence=0.5, 
                                            lacunarity=2.0, 
                                            repeatx=size, 
                                            repeaty=size, 
                                            base=42)
                    noise_value_simple = np.random.rand()  # Example: random noise
                    
                    # Normalize the noise values to be between 0 and 1
                    normalized_noise_value_perlin = (noise_value_perlin + 1) / 2
                    normalized_noise_value_simple = noise_value_simple
                    
                    # Combine noise values based on their amounts
                    combined_noise_value = (perlin_amount * normalized_noise_value_perlin + 
                                        simple_amount * normalized_noise_value_simple) / (perlin_amount + simple_amount)
                    
                    # Determine grass presence based on combined noise and density
                    grass_map_data[y, x] = combined_noise_value < density
        else:
            # Use multiprocessing only for larger maps
            try:
                # Use context manager to ensure clean process termination
                ctx = multiprocessing.get_context('spawn')  # Use spawn method for Windows compatibility
                num_workers = min(ctx.cpu_count(), 4)  # Limit to 4 workers max
                chunk_size = size // num_workers
                tasks = [
                    (i * chunk_size, (i + 1) * chunk_size if i < num_workers - 1 else size,
                    size, density, perlin_amount, simple_amount)
                    for i in range(num_workers)
                ]
                
                with ctx.Pool(processes=num_workers, initializer=_mp_worker_initializer) as pool:
                    results = pool.starmap(self._generate_grass_map_chunk, tasks)
                    
                grass_map_data = np.vstack(results)
                
            except Exception as e:
                print(f"Multiprocessing error: {e}")
                # Fall back to single-process method
                messagebox.showinfo("Notice", "Using single-process mode for generating grass map")
                
                # Generate the entire map in the main process as fallback
                grass_map_data = np.zeros((size, size), dtype=np.float32)
                for y in range(size):
                    for x in range(size):
                        # Same code as above single-process version
                        noise_value_perlin = snoise2(x / (50.0 * perlin_amount), 
                                                y / (50.0 * perlin_amount), 
                                                octaves=5, 
                                                persistence=0.5, 
                                                lacunarity=2.0, 
                                                repeatx=size, 
                                                repeaty=size, 
                                                base=42)
                        noise_value_simple = np.random.rand()
                        normalized_noise_value_perlin = (noise_value_perlin + 1) / 2
                        normalized_noise_value_simple = noise_value_simple
                        combined_noise_value = (perlin_amount * normalized_noise_value_perlin + 
                                            simple_amount * normalized_noise_value_simple) / (perlin_amount + simple_amount)
                        grass_map_data[y, x] = combined_noise_value < density

        # Turn into an image
        grass_map_image = np.zeros((size, size), dtype=np.uint8)
        grass_map_image[grass_map_data.astype(bool)] = 255

        brightness_value = int(255 * lightness)
        brightness_value = max(0, min(255, brightness_value))

        grass_map_image[~grass_map_data.astype(bool)] = brightness_value

        return grass_map_image

    def _create_grass_map_tab(self):
        # Create the grass map tab
        self.grass_map_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.grass_map_tab, text="Grass Map")

        # Create left panel for controls
        controls_frame = ttk.Frame(self.grass_map_tab)
        controls_frame.pack(side="left", fill="y", padx=(0, 20))

        # Add sliders for grass density
        self.vars["grass_density"] = tk.DoubleVar(value=0.5)  # Default value for grass density
        self._create_slider(controls_frame, "Grass Density", "grass_density", 0.0, 1.0, 0.01)

        # Add sliders for noise amounts
        self._create_slider(controls_frame, "Perlin Noise Amount", "perlin_noise_amount", 0.0, 4.0, 0.01)
        self._create_slider(controls_frame, "Simple Noise Amount", "simple_noise_amount", 0.0, 2.0, 0.01)

        # Add a slider for lightness adjustment
        self.vars["lightness"] = tk.DoubleVar(value=0.0)  # Default lightness value
        self._create_slider(controls_frame, "Lightness", "lightness", 0.0, 1.0, 0.01)  # Range from 0 (black) to 2 (white)

        # Add a button to export the grass map
        ttk.Button(controls_frame, text="Export Grass Map", command=self.export_grass_map).pack(fill="x", pady=5)

        # Add a preview canvas for the grass map
        self.grass_map_preview_canvas = tk.Canvas(self.grass_map_tab, width=600, height=600, bg='white')
        self.grass_map_preview_canvas.pack(side="right", pady=(20, 0))

        self.grass_map_preview_photo = None  # Persistent reference to image

    def select_grass_color(self):
        # Open a color picker dialog
        color_code = colorchooser.askcolor(title="Choose Grass Color")  # Use the imported colorchooser
        if color_code[1]:  # Check if a color was selected
            self.grass_color = color_code[0]  # RGB tuple

    def generate_grass_map(self):
        """Update the preview canvas with the current grass map."""
        grass_map_image = self.create_grass_map_data()
        self._update_grass_map_preview(grass_map_image)

    @staticmethod
    def _generate_grass_map_chunk(start_row, end_row, size, density, perlin_amount, simple_amount):
        chunk_data = np.zeros((end_row - start_row, size), dtype=np.float32)

        for y in range(start_row, end_row):
            for x in range(size):
                # Generate Perlin noise
                noise_value_perlin = snoise2(x / (50.0 * perlin_amount), 
                                            y / (50.0 * perlin_amount), 
                                            octaves=5, 
                                            persistence=0.5, 
                                            lacunarity=2.0, 
                                            repeatx=size, 
                                            repeaty=size, 
                                            base=42)
                # Generate Simple noise
                noise_value_simple = np.random.rand()  # Example: random noise

                # Normalize the noise values to be between 0 and 1
                normalized_noise_value_perlin = (noise_value_perlin + 1) / 2  # Normalize from [-1, 1] to [0, 1]
                normalized_noise_value_simple = (noise_value_simple)  # Already between [0, 1]

                # Combine noise values based on their amounts
                combined_noise_value = (perlin_amount * normalized_noise_value_perlin + 
                                        simple_amount * normalized_noise_value_simple) / (perlin_amount + simple_amount)

                # Determine grass presence based on combined noise and density
                chunk_data[y - start_row, x] = combined_noise_value < density

        return chunk_data

    def _update_grass_map_preview(self, grass_map_image):
        # Convert the NumPy array to an image
        grass_map_image_pil = Image.fromarray(grass_map_image)

        # Resize the grass map image to fit the canvas
        canvas_width, canvas_height = 600, 600
        resized_img = grass_map_image_pil.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)

        self.grass_map_preview_photo = ImageTk.PhotoImage(resized_img)
        self.grass_map_preview_canvas.delete("all")

        # Center the image on the canvas
        img_width, img_height = resized_img.size
        offset_x = (canvas_width - img_width) // 2
        offset_y = (canvas_height - img_height) // 2

        self.grass_map_preview_canvas.create_image(offset_x, offset_y, anchor="nw", image=self.grass_map_preview_photo)

    def export_grass_map(self):
        """Save the current grass map to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            return  # User canceled

        grass_map_image = self.create_grass_map_data()
        Image.fromarray(grass_map_image).save(file_path)
        messagebox.showinfo("Success", f"Grass map saved to {file_path}")

    def _on_size_change(self):
        # Get the current size and the new size
        old_size = getattr(self, "current_size", self.vars["noise_size"].get())
        new_size = self.vars["noise_size"].get()

        # Calculate the scaling factor
        scale_factor = new_size / old_size

        # Get the canvas dimensions
        canvas_width, canvas_height = 600, 600

        # Calculate the current focus point in terms of the heightmap
        focus_x = getattr(self, "focus_x", 0.5) * old_size
        focus_y = getattr(self, "focus_y", 0.5) * old_size

        # Adjust the focus point to keep the canvas center consistent
        canvas_center_x = canvas_width / 2
        canvas_center_y = canvas_height / 2

        focus_x = (focus_x + canvas_center_x * (scale_factor - 1)) / new_size
        focus_y = (focus_y + canvas_center_y * (scale_factor - 1)) / new_size

        # Update the focus point
        self.focus_x = max(0.0, min(1.0, focus_x))
        self.focus_y = max(0.0, min(1.0, focus_y))

        # Update the current size
        self.current_size = new_size

        # Update the preview
        self.update_noise_preview()

    def _create_noise_preview(self):
        # Create a frame for the preview and controls
        preview_frame = ttk.Frame(self.noise_tab)
        preview_frame.pack(side="right", pady=(20, 0))
        
        # Add a title for the preview section
        preview_title = ttk.Label(preview_frame, text="NOISE PREVIEW", 
                                font=("Segoe UI", 12, "bold"))
        preview_title.pack(side="top", pady=(0, 10))
        
        # Add zoom and position indicators
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(side="top", fill="x", pady=(0, 5))
        
        # Create a style for info labels
        self.style.style.configure("Info.TLabel", background=THEME_COLOR, foreground=ACCENT_COLOR)
        
        # Scale/zoom display
        scale_frame = ttk.Frame(info_frame)
        scale_frame.pack(side="right")
        ttk.Label(scale_frame, text="Scale: ", style="Info.TLabel").pack(side="left")
        self.scale_var = tk.StringVar()
        self.scale_var.set(f"{self.vars['scale'].get():.2f}")
        ttk.Label(scale_frame, textvariable=self.scale_var, style="Info.TLabel").pack(side="left")
        self.vars["scale"].trace_add("write", lambda *args: self.scale_var.set(f"{self.vars['scale'].get():.2f}"))
        
        # Create styled canvas with grid pattern
        self.noise_preview_canvas = self._create_styled_canvas(preview_frame, 600, 600)
        
        self.preview_photo = None  # Persistent reference to image
        self.noise_preview_canvas.focus_set()
        
        # Remove cursor hint for panning
        self.noise_preview_canvas.configure(cursor="arrow")  # Changed from "fleur"
        
        # Bind mouse events for click-and-drag
        self.noise_preview_canvas.bind("<Button-1>", self._on_canvas_click)
        self.noise_preview_canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.noise_preview_canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        
        # Add control buttons below the canvas
        controls_frame = ttk.Frame(preview_frame)
        controls_frame.pack(side="top", fill="x", pady=10)
        
        # Reset view button
        reset_btn = ttk.Button(controls_frame, text="Reset View", 
                            command=self._reset_view, style="TButton")
        reset_btn.pack(side="left", padx=5)
        
        # Zoom controls
        zoom_frame = ttk.Frame(controls_frame)
        zoom_frame.pack(side="right")
        
        zoom_out_btn = ttk.Button(zoom_frame, text="−", width=2,
                                command=lambda: self._adjust_zoom(-1))
        zoom_out_btn.pack(side="left", padx=2)
        
        zoom_in_btn = ttk.Button(zoom_frame, text="+", width=2,
                            command=lambda: self._adjust_zoom(1))
        zoom_in_btn.pack(side="left", padx=2)
        
        # Add tooltip instructions
        tip_text = "Click and drag to pan. Use zoom buttons or mouse wheel to zoom."
        ttk.Label(preview_frame, text=tip_text, foreground="#95a5a6", 
                font=("Segoe UI", 8)).pack(side="top", pady=(5, 0))
        
        # Bind mouse wheel for zooming
        self.noise_preview_canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        # For Linux/Mac
        self.noise_preview_canvas.bind("<Button-4>", lambda e: self._on_mouse_wheel(e, 120))
        self.noise_preview_canvas.bind("<Button-5>", lambda e: self._on_mouse_wheel(e, -120))

    def _reset_view(self):
        """Reset the view to default position and scale."""
        self.focus_x = 0.5
        self.focus_y = 0.5
        self.vars["scale"].set(150.0)  # Reset to default scale
        self.update_noise_preview()
        
    def _adjust_zoom(self, direction):
        """Adjust zoom level."""
        current_scale = self.vars["scale"].get()
        if direction > 0:
            # Zoom in (increase scale value)
            new_scale = min(500.0, current_scale * 1.25)
        else:
            # Zoom out (decrease scale value)
            new_scale = max(1.0, current_scale * 0.8)

        self.vars["scale"].set(new_scale)
        self.scale_var.set(f"{new_scale:.2f}")
        self.update_noise_preview()
        
    def _on_mouse_wheel(self, event, delta=None):
        """Handle mouse wheel events for zooming."""
        if delta is None:
            delta = event.delta
        
        if delta > 0:
            self._adjust_zoom(1)  # Zoom in
        else:
            self._adjust_zoom(-1)  # Zoom out

    def _on_canvas_click(self, event):
        # Store the initial click position
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
        # Only store initial position, don't immediately update focus point
        # This prevents immediate jumps in the display

    def _on_canvas_drag(self, event):
        # Calculate the exact drag distance in canvas space
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
    
        # Convert drag distance to world space movement
        # Use floating point arithmetic to ensure smooth movement
        canvas_width, canvas_height = 600, 600
        world_dx = dx / canvas_width
        world_dy = dy / canvas_height
    
        # Update the focus point (move in opposite direction of drag)
        self.focus_x = max(0.0, min(1.0, getattr(self, "focus_x", 0.5) - world_dx))
        self.focus_y = max(0.0, min(1.0, getattr(self, "focus_y", 0.5) - world_dy))
    
        # Update drag start to current position
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
        # Generate new preview with updated focus
        self.update_noise_preview()

    def _on_canvas_release(self, event):
        # Finalize the drag operation (optional, can be used for cleanup)
        pass

    def generate_greyscale_heightmap(self):
        """Generate and save the heightmap in greyscale."""
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            return  # User canceled

        size = self.vars["noise_size"].get()
        num_workers = multiprocessing.cpu_count()

        # Capture all parameters
        focus_x = getattr(self, "focus_x", 0.5)
        focus_y = getattr(self, "focus_y", 0.5)

        vars_dict = {k: v.get() for k, v in self.vars.items()}
        vars_dict["focus_x"] = focus_x
        vars_dict["focus_y"] = focus_y

        # Generate noise data
        noise_data = self._generate_full_noise_data(size, vars_dict, num_workers)

        # Create greyscale heightmap
        heightmap = self._create_heightmap(noise_data)

        # Convert heightmap to greyscale (using the red channel)
        greyscale_image = Image.fromarray(heightmap[:, :, 0])  # Use the red channel for greyscale

        # Save it
        greyscale_image.save(file_path)
        messagebox.showinfo("Success", f"Greyscale heightmap saved to {file_path}")

    def _create_heightmap(self, height_data):
        # Create RGB image with height in red channel
        heightmap = np.zeros((height_data.shape[0], height_data.shape[1], 3), dtype=np.uint8)
        
        # Get min and max height values
        min_height = self.vars["min_height"].get()  # Get min height from the slider
        max_height = self.vars["max_height"].get()
        
        # Adjust height data based on min/max settings
        if min_height != 0.0:
            # Shift the entire height range up or down
            height_data = height_data + min_height
        
        if max_height != 1.0:
            # Scale the height range
            current_max = height_data.max()
            if current_max > 0:
                height_data = height_data * (max_height / current_max)
        
        # Ensure values are within valid range
        height_data = np.clip(height_data, 0.0, 1.0)
        
        # Scale to 0-255 range
        height_scaled = (height_data * 255).astype(np.uint8)
        
        # Apply vignette if strength > 0
        vignette_strength = self.vars["vignette_strength"].get()
        if vignette_strength > 0:
            vignette_radius = self.vars["vignette_radius"].get()
            height_scaled = self._apply_vignette(height_scaled, vignette_strength, vignette_radius)
        
        # Set channels according to Teardown's format
        heightmap[:, :, 0] = height_scaled  # Red channel = height
        if self.vars["use_noise_grass"].get():
            # Generate grass noise
            grass_noise = self._generate_grass_noise(height_data.shape[0], height_data.shape[1])
            heightmap[:, :, 1] = grass_noise  # Green channel = grass with noise
        else:
            # Use uniform grass amount
            heightmap[:, :, 1] = self.vars["grass_amount"].get()  # Green channel = grass amount

        # Fill with hard blue by default
        special_val = self.vars["special_value"].get()
        heightmap[:, :, 2] = special_val

        return heightmap
    
    def _generate_grass_noise(self, height, width):
        """Generate grass noise using exactly the same coordinate system as the main noise."""

        # === 1. Grass-specific parameters ===
        octaves = self.vars["grass_noise_octaves"].get()
        persistence = self.vars["grass_noise_persistence"].get()
        grass_scale = self.vars["grass_noise_scale"].get()
        density = self.vars["noise_grass_density"].get()
        grass_amount = self.vars["grass_amount"].get()
        seed = self.vars["seed"].get() + 1000  # Offset seed to differentiate grass

        # === 2. Scaling and resolution matching ===
        base_scale = self.vars["scale"].get()
        preview_res = self.vars["noise_size"].get()  # Size used in preview
        export_res = width  # Export width — assume square

        zoom_factor = export_res / preview_res
        adjusted_scale = base_scale * zoom_factor * 0.05  # 🔧 Tame zoom with 0.05 multiplier

        # === 3. Use current focus point ===
        focus_x = max(0.0, min(1.0, getattr(self, "focus_x", 0.5)))
        focus_y = max(0.0, min(1.0, getattr(self, "focus_y", 0.5)))

        # === 4. Coordinate offset matching main noise ===
        world_offset_x = (focus_x - 0.5) * width
        world_offset_y = (focus_y - 0.5) * height

        base_offset_x = 1000.0
        base_offset_y = 1000.0

        # === 5. Output grass map ===
        grass_map = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                # Match coordinate sampling with base texture
                sample_x = base_offset_x + (x - world_offset_x) / adjusted_scale
                sample_y = base_offset_y + (y - world_offset_y) / adjusted_scale

                # Apply grass-specific scaling
                grass_sample_x = sample_x / grass_scale
                grass_sample_y = sample_y / grass_scale

                noise_value = snoise2(
                    grass_sample_x,
                    grass_sample_y,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=2.0,
                    base=seed
                )

                normalized_noise = (noise_value + 1) / 2

                if normalized_noise < density:
                    grass_map[y, x] = grass_amount
                else:
                    grass_map[y, x] = 0

        return grass_map




    def _apply_vignette(self, image, strength, radius):
        """Apply vignette effect to the image."""
        # Support both grayscale and color images
        if image.ndim == 2:
            # Grayscale image
            height, width = image.shape
            channels = 1
            is_gray = True
        else:
            # Color image
            height, width, channels = image.shape
            is_gray = False
        
        # Create vignette mask
        y, x = np.ogrid[:height, :width]
        center_x, center_y = width / 2, height / 2
        # Calculate distance from center
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        # Create vignette mask with adjustable radius
        vignette = 1 - np.clip((distance / (max_distance * radius)), 0, 1) * strength
        vignette = np.clip(vignette, 0, 1)
        # Apply vignette mask
        if is_gray:
            # For grayscale images, directly multiply and return 2D array
            return (image * vignette).astype(np.uint8)
        else:
            # For color images, apply per-channel and return image
            for i in range(channels):
                image[:, :, i] = (image[:, :, i] * vignette).astype(np.uint8)
            return image

    def _generate_noise_data(self, size, noise_type=None, octaves=None, persistence=None, scale=None):
        self.generator = TextureGenerator(seed=self.vars["seed"].get())

        # If noise_type is not provided, use the default from the noise tab
        if noise_type is None:
            noise_type = {
                "perlin": NoiseTypeEnum.PERLINNOISE,
                "fractal": NoiseTypeEnum.FRACTALNOISE,
                "turbulence": NoiseTypeEnum.TURBULENCE,
                "shape": NoiseTypeEnum.SHAPE_NOISE
            }[self.vars["noise_type"].get()]

        if noise_type == NoiseTypeEnum.SHAPE_NOISE:
            shape_type = self.vars["shape_type"].get()
            shape_size = self.vars["shape_size"].get()
            shape_spacing = self.vars["shape_spacing"].get()
            noise_data = self.generator.generate_shape_noise(size, shape_type, shape_size, shape_spacing)
            print(f"Generated Shape Noise:\n{noise_data}")
            return noise_data

        # Create output array
        noise_data = np.zeros((size, size), dtype=np.float32)

        # Get focus point coordinates
        focus_x = max(0.0, min(1.0, getattr(self, "focus_x", 0.5)))  # Clamp to [0, 1]
        focus_y = max(0.0, min(1.0, getattr(self, "focus_y", 0.5)))  # Clamp to [0, 1]

        # Calculate the world offset
        world_offset_x = (focus_x - 0.5) * size
        world_offset_y = (focus_y - 0.5) * size

        # Use the exact scale value from the UI - don't apply any adjustments
        adjusted_scale = scale if scale is not None else self.vars["scale"].get()

        base_offset_x = 1000.0  # Large offset to avoid zero
        base_offset_y = 1000.0  # Large offset to avoid zero

        # Sample noise with precise floating-point coordinates
        for y in range(size):
            for x in range(size):
                sample_x = base_offset_x + (x - world_offset_x) / adjusted_scale
                sample_y = base_offset_y + (y - world_offset_y) / adjusted_scale

                noise_data[y, x] = self.generator.noise.simplexNoise(
                    noise_type,
                    size,
                    octaves if octaves is not None else self.vars["octaves"].get(),
                    persistence if persistence is not None else self.vars["persistence"].get(),
                    self.vars["lacunarity"].get(),
                    1.0,  # Use 1.0 as scale here since we're adjusting coordinates directly
                    sample_x, sample_y
                )

        return noise_data

    def update_noise_preview(self):
        try:
            # Set the preview resolution to high quality (e.g., 256)
            preview_res = 256  # Always use high quality

            # Debugging: Print focus points and scale for preview
            focus_x = getattr(self, "focus_x", 0.5)
            focus_y = getattr(self, "focus_y", 0.5)

            noise_data = self._generate_noise_data(preview_res)
            heightmap = self._create_heightmap(noise_data)
            self.full_heightmap = Image.fromarray(heightmap)

            self._update_preview_canvas()
        except Exception as e:
            print(f"Preview generation error: {e}")

    def _update_preview_canvas(self):
        if self.full_heightmap is None:
            return

        canvas_width, canvas_height = 600, 600

        # Resize full heightmap to fit canvas
        resized_img = self.full_heightmap.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)

        self.preview_photo = ImageTk.PhotoImage(resized_img)
        self.noise_preview_canvas.delete("all")

        # Center the image on the canvas
        img_width, img_height = resized_img.size
        offset_x = (canvas_width - img_width) // 2
        offset_y = (canvas_height - img_height) // 2

        self.noise_preview_canvas.create_image(offset_x, offset_y, anchor="nw", image=self.preview_photo)

    def generate_noise(self):
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            return  # User canceled

        def worker(file_path):
            try:
                self.root.after(0, lambda: self.generate_button.config(state="disabled"))

                size = self.vars["noise_size"].get()
                num_workers = multiprocessing.cpu_count()

                # Use the same focus points as the preview
                focus_x = getattr(self, "focus_x", 0.5)
                focus_y = getattr(self, "focus_y", 0.5)

                # Create a complete vars dictionary including all parameters
                vars_dict = {k: v.get() for k, v in self.vars.items()}
                vars_dict["focus_x"] = focus_x
                vars_dict["focus_y"] = focus_y

                # Generate noise data using multiprocessing
                noise_data = self._generate_full_noise_data(size, vars_dict, num_workers)

                # Create heightmap
                heightmap = self._create_heightmap(noise_data)

                # Save the heightmap as an image
                img = Image.fromarray(heightmap)
                img.save(file_path)

                self.root.after(0, lambda: messagebox.showinfo("Success", f"Noise saved to {file_path}"))

            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))

            finally:
                self.root.after(0, lambda: self.generate_button.config(state="normal"))

        threading.Thread(target=worker, args=(file_path,), daemon=True).start()

    def _generate_full_noise_data(self, size, vars_dict, num_workers):
        tile_size = size // num_workers

        tasks = []
        for i in range(num_workers):
            start_row = i * tile_size
            end_row = (i + 1) * tile_size if i < num_workers - 1 else size
            tasks.append((start_row, end_row, size, vars_dict))

        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.map(TextureGeneratorGUI._generate_chunk, tasks)

        return np.vstack(results)

    @staticmethod
    def _generate_chunk(args):
        start_row, end_row, size, vars_dict = args
    
        from texture_generator import TextureGenerator, NoiseTypeEnum  # Re-import in child process
        generator = TextureGenerator(seed=vars_dict["seed"])
    
        noise_type = {
            "perlin": NoiseTypeEnum.PERLINNOISE,
            "fractal": NoiseTypeEnum.FRACTALNOISE,
            "turbulence": NoiseTypeEnum.TURBULENCE,
            "shape": NoiseTypeEnum.SHAPE_NOISE
        }[vars_dict["noise_type"]]
    
        # Initialize the chunk
        chunk = np.zeros((end_row - start_row, size), dtype=np.float32)
    
        # Handle shape noise differently
        if noise_type == NoiseTypeEnum.SHAPE_NOISE:
            # Get shape parameters
            shape_type = vars_dict.get("shape_type", "circle")
            shape_size = vars_dict.get("shape_size", 10)
            shape_spacing = vars_dict.get("shape_spacing", 5)
        
            # Generate only the required chunk of shape noise
            # Note: This approach needs to generate the entire pattern to ensure consistency
            # but only returns the requested chunk
            full_shape_noise = generator.generate_shape_noise(size, shape_type, shape_size, shape_spacing)
            chunk = full_shape_noise[start_row:end_row, :]
        
            print(f"Generated {shape_type} shape noise chunk from rows {start_row} to {end_row}")
        else:
            # Get focus point coordinates
            focus_x = max(0.0, min(1.0, vars_dict["focus_x"]))  # Clamp to [0, 1]
            focus_y = max(0.0, min(1.0, vars_dict["focus_y"]))  # Clamp to [0, 1]
        
            # Calculate the world offset
            world_offset_x = (focus_x - 0.5) * size  # Center on focus_x
            world_offset_y = (focus_y - 0.5) * size  # Center on focus_y
        
            # Apply zoom factor to the scale
            preview_res = vars_dict.get("preview_res", 256)  # Default preview resolution
            zoom_factor = size / preview_res  # Scale export to match preview zoom
            adjusted_scale = vars_dict["scale"] * zoom_factor
        
            base_offset_x = 1000.0
            base_offset_y = 1000.0
        
            # Generate noise data for each pixel in the chunk
            for y in range(start_row, end_row):
                for x in range(size):
                    sample_x = base_offset_x + (x - world_offset_x) / adjusted_scale
                    sample_y = base_offset_y + (y - world_offset_y) / adjusted_scale
                
                    chunk[y - start_row, x] = generator.noise.simplexNoise(
                        noise_type,
                        size,
                        vars_dict["octaves"],
                        vars_dict["persistence"],
                        vars_dict["lacunarity"],
                        1.0,
                        sample_x, sample_y
                    )
    
        return chunk
    
def _mp_worker_initializer():
    """Prevent worker processes from capturing keyboard interrupts."""
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def main():
    # Windows-specific fix for multiprocessing
    if __name__ == "__main__":
        multiprocessing.freeze_support()  # Needed for PyInstaller
        root = tk.Tk()
        app = TextureGeneratorGUI(root)
        root.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Critical for PyInstaller on Windows
    main()