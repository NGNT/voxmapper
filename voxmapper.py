import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import threading
import multiprocessing
from texture_generator import TextureGenerator, NoiseTypeEnum
from noise import snoise2, pnoise2
import traceback

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
        self.root.title("voxmapper v1.4.1")
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
        
        # Create mountain generation tab
        self.mountain_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.mountain_tab, text="Mountain Generation")
        
        self.vars = {
            "noise_size": tk.IntVar(value=512),
            "scale": tk.DoubleVar(value=150.0),
            "seed": tk.IntVar(value=42),
            "min_height": tk.DoubleVar(value=1.0),  # Changed to tk.DoubleVar
            "max_height": tk.DoubleVar(value=0.5),
            "noise_type": tk.StringVar(value="perlin noise"),
            "octaves": tk.IntVar(value=7),
            "lacunarity": tk.DoubleVar(value=2.0),
            "persistence": tk.DoubleVar(value=0.6),
            "height_scale": tk.IntVar(value=255),
            "grass_amount": tk.IntVar(value=0),
            "special_value": tk.IntVar(value=0),
            "vignette_strength": tk.DoubleVar(value=0.0),
            "vignette_radius": tk.DoubleVar(value=0.5),
            # Landmass variables are now part of the noise tab section
            "landmass_size": tk.IntVar(value=256),
            "landmass_land_proportion": tk.DoubleVar(value=0.6),
            "landmass_water_level": tk.DoubleVar(value=0.12),
            "landmass_plain_factor": tk.DoubleVar(value=2.5),
            "landmass_shore_height": tk.DoubleVar(value=0.05),
            "landmass_seed": tk.IntVar(value=0),
            "landmass_noise_scale": tk.DoubleVar(value=100.0),
            "landmass_octaves": tk.IntVar(value=6)
        }

        self.vars.update({
            "grass_noise_type": tk.StringVar(value="perlin noise"),  # Default noise type for grass
            "grass_octaves": tk.IntVar(value=5),  # Default octaves for grass noise
            "grass_persistence": tk.DoubleVar(value=0.5),  # Default persistence for grass noise
            "grass_scale": tk.DoubleVar(value=50.0),  # Default scale for grass noise
            "perlin_noise_amount": tk.DoubleVar(value=0.5),  # Default value for Perlin noise amount
            "simple_noise_amount": tk.DoubleVar(value=0.5),  # Default value for simple noise amount
            # "noise_type" is already in the main self.vars dictionary
            "fractal_noise_amount": tk.DoubleVar(value=0.5),  # Default value for fractal noise amount
            "use_noise_grass": tk.BooleanVar(value=False),  # Toggle for noise-based grass
            "grass_noise_scale": tk.DoubleVar(value=50.0),  # Scale for grass noise
            "grass_noise_octaves": tk.IntVar(value=4),      # Octaves for grass noise
            "grass_noise_persistence": tk.DoubleVar(value=0.5),  # Persistence for grass noise
            "grass_density": tk.DoubleVar(value=0.5),       # Grass density threshold for noise-based grass
            "noise_grass_density": tk.DoubleVar(value=0.5),  # Grass density threshold for noise-based grass
            "image_brightness": tk.DoubleVar(value=1.0),
            "image_contrast": tk.DoubleVar(value=1.0),
            "image_gamma": tk.DoubleVar(value=1.0),
            "green_channel_value": tk.DoubleVar(value=0.5),
            "green_lightness": tk.DoubleVar(value=0.5),
            "invert_green": tk.BooleanVar(value=False),
            "red_channel_weight": tk.DoubleVar(value=0.299),  # Standard RGB to grayscale weights
            "green_channel_weight": tk.DoubleVar(value=0.587),
            "blue_channel_weight": tk.DoubleVar(value=0.114),
            "hill_count": tk.IntVar(value=600),
            "base_radius": tk.DoubleVar(value=16.0),
            "radius_variation": tk.DoubleVar(value=0.7)
            # Removed: "landmass_weight", "terrain_size", "terrain_seed"
        })

        self.slider_active = {}

        self.imported_image = None
        self.processed_image = None
        self.image_preview = None
        
        # Create controls and preview for noise tab
        self._create_noise_controls()
        self._create_noise_preview()

        # Create grass map tab
        self._create_grass_map_tab()

        # Create image import tab
        self.image_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_tab, text="Image Import")
        self._create_image_import_tab()
        
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
            header_canvas.create_text(200, gradient_height//2 + 15, text="v1.4.1 by NGNT", 
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
        """Creates the controls panel for the noise generation tab."""
        # Create left panel for controls
        left_panel = ttk.Frame(self.mountain_tab)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Make the controls frame scrollable
        scroll_canvas = tk.Canvas(left_panel, borderwidth=0, highlightthickness=0, bg=BACKGROUND_COLOR, width=400)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=scroll_canvas.yview)
        scrollable_frame = ttk.Frame(scroll_canvas, style="TFrame")

        # Set a minimum width for the scrollable frame to ensure controls have enough space
        scrollable_frame.columnconfigure(0, minsize=380)

        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        )

        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Group 1: Basic Settings
        basic_frame = ttk.LabelFrame(scrollable_frame, text="Basic Settings", padding=10)
        basic_frame.pack(fill="x", pady=10)

        # Noise type selection
        noise_type_frame = ttk.Frame(basic_frame)
        noise_type_frame.pack(fill="x", pady=5)
        ttk.Label(noise_type_frame, text="Noise Type:").pack(side="left")
        noise_combo = ttk.Combobox(noise_type_frame, textvariable=self.vars["noise_type"],
                                values=["perlin noise", "fractal noise", "turbulence noise", "landmass"],
                                state="readonly", width=20)
        noise_combo.pack(side="left", padx=5)
        noise_combo.bind("<<ComboboxSelected>>", lambda e: [self._toggle_landmass_controls(), self.update_noise_preview()])

        # Size and scale sliders
        self._create_slider(basic_frame, "Size", "noise_size", 64, 4096, 64).bind("<ButtonRelease-1>", lambda e: self._on_size_change())
        self._create_slider(basic_frame, "Scale", "scale", 1.0, 500.0, 1.0)
        self._create_slider(basic_frame, "Seed", "seed", 1.0, 500.0, 1.0)

        # Reset view button
        ttk.Button(basic_frame, text="Reset View", command=self._reset_view).pack(fill="x", pady=5)

        # Group 2: Teardown Heightmap Settings
        heightmap_frame = ttk.LabelFrame(scrollable_frame, text="Teardown Heightmap Settings", padding=10)
        heightmap_frame.pack(fill="x", pady=10)

        self._create_slider(heightmap_frame, "Min Height", "min_height", -1.0, 1.0, 0.1)
        self._create_slider(heightmap_frame, "Max Height", "max_height", 0.0, 2.0, 0.1)
        self._create_slider(heightmap_frame, "Height Scale", "height_scale", 1, 255, 1)
        self._create_slider(heightmap_frame, "Grass Amount", "grass_amount", 0, 255, 1)
        self._create_slider(heightmap_frame, "Special Value", "special_value", 0, 255, 1)

        # Add grass type toggle (uniform vs noise-based)
        grass_type_frame = ttk.Frame(heightmap_frame)
        grass_type_frame.pack(fill="x", pady=5)
        ttk.Label(grass_type_frame, text="Grass Type:").pack(side="left", padx=5)
        ttk.Radiobutton(grass_type_frame, text="Uniform", variable=self.vars["use_noise_grass"], value=False).pack(side="left")
        ttk.Radiobutton(grass_type_frame, text="Noise", variable=self.vars["use_noise_grass"], value=True).pack(side="left")

        # Add noise-based grass parameters (initially hidden)
        self.grass_noise_frame = ttk.LabelFrame(heightmap_frame, text="Grass Noise Settings", padding=10)
        self.vars["use_noise_grass"].trace_add("write", self._toggle_grass_noise_controls)

        self._create_slider(self.grass_noise_frame, "Scale", "grass_noise_scale", 1.0, 200.0, 0.1)
        self._create_slider(self.grass_noise_frame, "Octaves", "grass_noise_octaves", 1, 8, 1)
        self._create_slider(self.grass_noise_frame, "Persistence", "grass_noise_persistence", 0.1, 1.0, 0.1)
        self._create_slider(self.grass_noise_frame, "Density", "noise_grass_density", 0.0, 1.0, 0.01)

        # Group 3: Noise Algorithm Settings
        noise_settings_frame = ttk.LabelFrame(scrollable_frame, text="Noise Algorithm Settings", padding=10)
        noise_settings_frame.pack(fill="x", pady=10)

        # Store reference to noise settings frame
        self.noise_settings_frame = noise_settings_frame

        self._create_slider(noise_settings_frame, "Octaves", "octaves", 1, 10, 1)
        self._create_slider(noise_settings_frame, "Lacunarity", "lacunarity", 1.0, 4.0, 0.1)
        self._create_slider(noise_settings_frame, "Persistence", "persistence", 0.1, 1.0, 0.01)

        # Group 4: Canyon Settings (new)
        canyon_frame = ttk.LabelFrame(scrollable_frame, text="Canyon Settings", padding=10)
        canyon_frame.pack(fill="x", pady=10)
        self.vars["canyon_strength"] = tk.DoubleVar(value=0.0)
        self.vars["canyon_length"] = tk.DoubleVar(value=0.7)
        self.vars["canyon_branch_density"] = tk.DoubleVar(value=0.15)  # Default branch density
        self.vars["canyon_count"] = tk.IntVar(value=6)  # Default canyon count (6 per edge)
        self.vars["canyon_seed"] = tk.IntVar(value=42)  # Add canyon-specific seed
        self._create_slider(canyon_frame, "Canyon Intensity", "canyon_strength", 0.0, 1.0, 0.05)
        self._create_slider(canyon_frame, "Canyon Length", "canyon_length", 0.3, 0.9, 0.05)
        self._create_slider(canyon_frame, "Branch Density", "canyon_branch_density", 0.0, 0.5, 0.01)
        self._create_slider(canyon_frame, "Canyon Count", "canyon_count", 1, 15, 1)
        self._create_slider(canyon_frame, "Canyon Seed", "canyon_seed", 1, 1000, 1)

        # Add a random seed button for canyon seeds
        canyon_seed_btn_frame = ttk.Frame(canyon_frame)
        canyon_seed_btn_frame.pack(fill="x", pady=5)
        self._create_styled_button(canyon_seed_btn_frame, "Random Canyon Seed", 
                                  lambda: [self.vars["canyon_seed"].set(np.random.randint(1, 1000)), 
                                          self.update_noise_preview()],
                                  style='TButton')

        # Group 5: Vignette Settings
        vignette_frame = ttk.LabelFrame(scrollable_frame, text="Vignette Effect", padding=10)
        vignette_frame.pack(fill="x", pady=10)
        self._create_slider(vignette_frame, "Strength", "vignette_strength", 0.0, 1.0, 0.01)
        self._create_slider(vignette_frame, "Radius", "vignette_radius", 0.0, 1.0, 0.01)
        self._create_slider(vignette_frame, "Smoothness", "vignette_smoothness", 0.0, 1.0, 0.01)

        # Group 6: Landmass Settings (this will be toggled based on noise type)
        self.landmass_controls_frame = ttk.LabelFrame(scrollable_frame, text="Landmass Settings", padding=10)

        self._create_slider(self.landmass_controls_frame, "Landmass Size", "landmass_size", 64, 2048, 64)
        self._create_slider(self.landmass_controls_frame, "Land Proportion", "landmass_land_proportion", 0.0, 1.0, 0.01)
        self._create_slider(self.landmass_controls_frame, "Plain Factor", "landmass_plain_factor", 1.0, 5.0, 0.1)
        self._create_slider(self.landmass_controls_frame, "Shore Height", "landmass_shore_height", 0.0, 0.2, 0.01)
        self._create_slider(self.landmass_controls_frame, "Noise Scale", "landmass_noise_scale", 1.0, 1000.0, 1.0)
        self._create_slider(self.landmass_controls_frame, "Octaves", "landmass_octaves", 1, 16, 1)

        landmass_seed_frame = ttk.Frame(self.landmass_controls_frame)
        landmass_seed_frame.pack(fill="x", pady=5)
        ttk.Label(landmass_seed_frame, text="Seed:").pack(side="left")
        landmass_seed_entry = ttk.Entry(landmass_seed_frame, textvariable=self.vars["landmass_seed"])
        landmass_seed_entry.pack(side="left", padx=5)
        landmass_seed_entry.bind("<Return>", lambda e: self.update_noise_preview()) 
        self._create_styled_button(landmass_seed_frame, "Random", 
                                lambda: [self.vars["landmass_seed"].set(np.random.randint(0, 1000000)), 
                                        self.update_noise_preview()],
                                style='TButton').pack(side="right")

        # Group 7: Action Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill="x", pady=10)

        self.generate_button = ttk.Button(button_frame, text="Generate Heightmap", command=self.generate_noise)
        self.generate_button.pack(fill="x", pady=5)

        self.generate_greyscale_button = ttk.Button(button_frame, text="Generate Greyscale Heightmap", 
                                               command=self.generate_greyscale_heightmap)
        self.generate_greyscale_button.pack(fill="x", pady=5)

        # Initially toggle landmass controls
        self._toggle_landmass_controls()

    def _create_noise_preview(self):
        """Creates the preview panel for the noise generation tab."""
        # Create preview frame on the right side
        preview_frame = ttk.Frame(self.mountain_tab)
        preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
        # Add a title for the preview section
        preview_title = ttk.Label(preview_frame, text="NOISE PREVIEW", 
                                font=("Segoe UI", 12, "bold"))
        preview_title.pack(side="top", pady=(0, 10))
    
        # Add zoom and position indicators
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(side="top", fill="x", pady=(0, 5))
    
        # Position indicator
        pos_frame = ttk.Frame(info_frame)
        pos_frame.pack(side="left", fill="x", expand=True)
        ttk.Label(pos_frame, text="Position:").pack(side="left")
        self.position_label = ttk.Label(pos_frame, text="Center")
        self.position_label.pack(side="left", padx=5)
    
        # Zoom indicator
        zoom_frame = ttk.Frame(info_frame)
        zoom_frame.pack(side="right")
        ttk.Label(zoom_frame, text="Zoom:").pack(side="left")
        self.zoom_label = ttk.Label(zoom_frame, text="100%")
        self.zoom_label.pack(side="left", padx=5)
    
        # Create the canvas for the preview
        self.noise_preview_canvas = self._create_styled_canvas(preview_frame, width=600, height=600)
    
        # Bind mouse events for panning
        self.noise_preview_canvas.bind("<ButtonPress-1>", self._on_canvas_click)
        self.noise_preview_canvas.bind("<B1-Motion>", self._on_canvas_drag)
    
        # Add zoom controls
        zoom_controls = ttk.Frame(preview_frame)
        zoom_controls.pack(side="top", pady=5)
    
        # Zoom buttons
        zoom_out_btn = ttk.Button(zoom_controls, text="-", width=3, 
                                command=lambda: [self.vars["scale"].set(max(1.0, self.vars["scale"].get() - 10.0)), 
                                                self.update_noise_preview()])
        zoom_out_btn.pack(side="left", padx=2)
    
        zoom_reset_btn = ttk.Button(zoom_controls, text="Reset", 
                                  command=self._reset_view)
        zoom_reset_btn.pack(side="left", padx=10)
    
        zoom_in_btn = ttk.Button(zoom_controls, text="+", width=3, 
                               command=lambda: [self.vars["scale"].set(min(500.0, self.vars["scale"].get() + 10.0)), 
                                               self.update_noise_preview()])
        zoom_in_btn.pack(side="left", padx=2)
    
        # Add help text
        ttk.Label(preview_frame, text="Click and drag to pan. Use zoom buttons or mouse wheel to zoom.", 
                foreground="#95a5a6", font=("Segoe UI", 8)).pack(side="top", pady=(5, 0))
    
        # Bind mouse wheel for zooming
        self.noise_preview_canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        # For Linux/Mac
        self.noise_preview_canvas.bind("<Button-4>", lambda e: self._on_mouse_wheel(e, 120))
        self.noise_preview_canvas.bind("<Button-5>", lambda e: self._on_mouse_wheel(e, -120))

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

    def _reset_view(self):
        """Reset the view to default position and scale."""
        self.focus_x = 0.5
        self.focus_y = 0.5
        self.vars["scale"].set(150.0)  # Reset to default scale
        self._update_position_indicator()  # Update position indicator
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
    
        # Update the zoom indicator
        zoom_percentage = int(150.0 / new_scale * 100)  # Calculate zoom percentage based on default scale
        self.zoom_label.config(text=f"{zoom_percentage}%")
    
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
    
        # Update position indicator
        self._update_position_indicator()
    
        # Generate new preview with updated focus
        self.update_noise_preview()

    def _update_position_indicator(self):
        """Update the position indicator label based on current focus point."""
        if hasattr(self, "position_label"):
            # Calculate position as percentage from center
            x_percent = int((self.focus_x - 0.5) * 200)  # Convert to +/- 100% range
            y_percent = int((self.focus_y - 0.5) * 200)
        
            # Format with plus sign for positive values
            x_str = f"+{x_percent}%" if x_percent > 0 else f"{x_percent}%"
            y_str = f"+{y_percent}%" if y_percent > 0 else f"{y_percent}%"
        
            position_text = f"X:{x_str}, Y:{y_str}"
            self.position_label.config(text=position_text)

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
        """Create RGB heightmap from raw height data with proper canyon application."""
        # Create RGB image with height in red channel
        heightmap = np.zeros((height_data.shape[0], height_data.shape[1], 3), dtype=np.uint8)

        # Get min and max height values
        min_height = self.vars["min_height"].get()
        max_height = self.vars["max_height"].get()

        # Adjust height data based on min/max settings
        if min_height != 0.0:
            height_data = height_data + min_height

        if max_height != 1.0:
            current_max = height_data.max()
            if current_max > 0:
                height_data = height_data * (max_height / current_max)

        # Ensure values are within valid range
        height_data = np.clip(height_data, 0.0, 1.0)

        # Get necessary parameters
        size = height_data.shape[0]  # Assuming square heightmap
        seed = self.vars["seed"].get()
        canyon_strength = self.vars["canyon_strength"].get()
        canyon_length = self.vars["canyon_length"].get()
        canyon_branch_density = self.vars["canyon_branch_density"].get()
        canyon_count = self.vars["canyon_count"].get()
        canyon_seed = self.vars["canyon_seed"].get()  # Get canyon-specific seed
        vignette_strength = self.vars["vignette_strength"].get()
        vignette_radius = self.vars["vignette_radius"].get()

        # Apply canyon effect
        if canyon_strength > 0:
            # Create canyon mask image using the same approach as mountain tab
            from PIL import Image, ImageDraw, ImageFilter
            import math
            import multiprocessing
    
            canyon_img = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(canyon_img)
    
            # Fixed random generator with canyon-specific seed instead of main seed
            fixed_rng = np.random.RandomState(canyon_seed)
    
            # Center point for canyons
            cx, cy = size / 2, size / 2
    
            # Number of canyons per edge - now using the slider value
            canyons_per_edge = canyon_count
    
            # Generate edge points
            edge_points = []
    
            # Generate evenly distributed edge points with consistent randomness
            def generate_edge_points(edge_type, count):
                points = []
                spacing = size / count
        
                if edge_type == "top":
                    y = 0
                    for i in range(count):
                        offset = fixed_rng.uniform(0.2, 0.8)
                        x = int((i + offset) * spacing)
                        points.append((x, y))
                elif edge_type == "bottom":
                    y = size - 1
                    for i in range(count):
                        offset = fixed_rng.uniform(0.2, 0.8)
                        x = int((i + offset) * spacing)
                        points.append((x, y))
                elif edge_type == "left":
                    x = 0
                    for i in range(count):
                        offset = fixed_rng.uniform(0.2, 0.8)
                        y = int((i + offset) * spacing)
                        points.append((x, y))
                elif edge_type == "right":
                    x = size - 1
                    for i in range(count):
                        offset = fixed_rng.uniform(0.2, 0.8)
                        y = int((i + offset) * spacing)
                        points.append((x, y))
                
                return points
    
            # Get points from all four edges
            edge_points.extend(generate_edge_points("top", canyons_per_edge))
            edge_points.extend(generate_edge_points("bottom", canyons_per_edge))
            edge_points.extend(generate_edge_points("left", canyons_per_edge))
            edge_points.extend(generate_edge_points("right", canyons_per_edge))
    
            # Create arguments for parallel processing
            worker_args = [(start_x, start_y, cx, cy, canyon_length, canyon_branch_density, canyon_seed, size) 
                          for start_x, start_y in edge_points]
        
            # Use multiprocessing to generate canyon paths
            try:
                ctx = multiprocessing.get_context('spawn')
                num_workers = min(ctx.cpu_count(), 4)  # Use at most 4 workers
            
                with ctx.Pool(processes=num_workers) as pool:
                    canyon_paths_results = pool.map(_create_canyon_path_worker, worker_args)
                
                # Filter out None results
                all_canyon_paths = [path for path in canyon_paths_results if path is not None]
            except Exception as e:
                # Fallback to single-process if multiprocessing fails
                print(f"Multiprocessing error for canyons: {e}. Using single-process mode.")
                all_canyon_paths = []
            
                # Process each starting point sequentially as fallback
                for start_x, start_y in edge_points:
                    result = _create_canyon_path_worker((start_x, start_y, cx, cy, canyon_length, 
                                                       canyon_branch_density, canyon_seed, size))
                    if result is not None:
                        all_canyon_paths.append(result)
    
            # Now apply the actual canyon_length parameter to draw only portions of each path
            for canyon in all_canyon_paths:
                # Get the main path
                path_points = canyon['main_path']
            
                # Calculate the actual path length based on canyon_length parameter
                length_variation = fixed_rng.uniform(-0.05, 0.05)
                length_ratio = canyon_length + length_variation
                length_ratio = max(0.2, min(0.95, length_ratio))
            
                # Get the number of points to use based on length_ratio
                points_to_use = max(2, int(len(path_points) * length_ratio))
                used_path = path_points[:points_to_use]
            
                # Smooth the main path
                if len(used_path) > 3:
                    smoothed_path = []
                    window_size = 3
                
                    for i in range(len(used_path)):
                        if i < window_size // 2 or i >= len(used_path) - window_size // 2:
                            smoothed_path.append(used_path[i])
                        else:
                            x_avg = sum(p[0] for p in used_path[i-window_size//2:i+window_size//2+1]) / window_size
                            y_avg = sum(p[1] for p in used_path[i-window_size//2:i+window_size//2+1]) / window_size
                            smoothed_path.append((int(x_avg), int(y_avg)))
                    
                    # Draw the main path with width scaled by canyon_strength
                    for j in range(len(smoothed_path) - 1):
                        progress = j / (len(smoothed_path) - 1)
                        width = max(2, int((1.0 - progress * 0.7) * canyon_strength * 15))
                        intensity = int(255 * (1.0 - progress * 0.2))
                        draw.line([smoothed_path[j], smoothed_path[j+1]], 
                                fill=intensity,
                                width=width)
            
                # Now draw branches - only those that connect to the used portion of the main path
                for branch_points in canyon['branches']:
                    # Get the starting point of the branch
                    branch_start = branch_points[0]
                
                    # Check if this branch connects to the used portion of the path
                    # by comparing the starting point to all points in the used path
                    is_connected = False
                    for p in used_path:
                        if abs(p[0] - branch_start[0]) <= 1 and abs(p[1] - branch_start[1]) <= 1:
                            is_connected = True
                            break
                
                    # Only draw branches that connect to the used path
                    if is_connected:
                        # Calculate how much of the branch to use based on main path length ratio
                        branch_length_ratio = length_ratio * 1.2  # Branches can be a bit longer
                        branch_length_ratio = min(1.0, branch_length_ratio)  # Cap at 100%
                    
                        # Get the points to use
                        branch_points_to_use = max(2, int(len(branch_points) * branch_length_ratio))
                        used_branch = branch_points[:branch_points_to_use]
                    
                        # Smooth the branch
                        if len(used_branch) > 3:
                            smoothed_branch = []
                            window_size = 3
                    
                            for i in range(len(used_branch)):
                                if i < window_size // 2 or i >= len(used_branch) - window_size // 2:
                                    smoothed_branch.append(used_branch[i])
                                else:
                                    x_avg = sum(p[0] for p in used_branch[i-window_size//2:i+window_size//2+1]) / window_size
                                    y_avg = sum(p[1] for p in used_branch[i-window_size//2:i+window_size//2+1]) / window_size
                                    smoothed_branch.append((int(x_avg), int(y_avg)))
                            
                            # Draw the branch
                            for k in range(len(smoothed_branch) - 1):
                                prog = k / (len(smoothed_branch) - 1)
                                branch_width = max(1, int((1.0 - prog * 0.7) * canyon_strength * 5))
                                intensity = int(220 * (1.0 - prog * 0.3))
                                draw.line([smoothed_branch[k], smoothed_branch[k+1]], 
                                        fill=intensity, 
                                        width=branch_width)
    
            # Apply Gaussian blur scaled with canyon_strength
            blur_radius = max(1.0, min(3.0, size / 256 * canyon_strength * 2))
            canyon_img = canyon_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
            # Convert to numpy array
            canyon_mask = np.array(canyon_img) / 255.0
    
            # Apply to heightmap with canyon_strength
            height_data = height_data * (1.0 - canyon_mask * min(1.0, canyon_strength * 1.2))

        # Scale to 0-255 range AFTER canyon application
        height_scaled = (height_data * 255).astype(np.uint8)

        # Apply vignette if strength > 0
        if vignette_strength > 0:
            height_scaled = self._apply_vignette(height_scaled, vignette_strength, vignette_radius)

        # Set channels according to Teardown format
        heightmap[:, :, 0] = height_scaled  # Red channel = height

        if self.vars["use_noise_grass"].get():
            # Generate grass noise
            grass_noise = self._generate_grass_noise(height_data.shape[0], height_data.shape[1])
            heightmap[:, :, 1] = grass_noise  # Green channel = grass with noise
        else:
            # Use uniform grass amount
            heightmap[:, :, 1] = self.vars["grass_amount"].get()  # Green channel = grass amount

        # Fill with special value
        special_val = self.vars["special_value"].get()
        heightmap[:, :, 2] = special_val

        return heightmap

    def _toggle_grass_noise_controls(self, *args):
        """Toggle visibility of grass noise controls based on the use_noise_grass variable."""
        if self.vars["use_noise_grass"].get():
            self.grass_noise_frame.pack(fill="x", pady=5)
        else:
            self.grass_noise_frame.pack_forget()

    def _toggle_landmass_controls(self, *args):
        """Show or hide the Landmass Settings section above the Generate buttons."""
        if self.vars["noise_type"].get() == "landmass":
            # Get reference to the button frame
            button_frame = None
            for child in self.mountain_tab.winfo_children():
                if isinstance(child, ttk.Frame):  # Left panel
                    for frame in child.winfo_children():
                        if isinstance(frame, tk.Canvas):  # Scroll canvas
                            for item in frame.winfo_children():
                                for subitem in item.winfo_children():
                                    if isinstance(subitem, ttk.Frame) and hasattr(subitem, 'winfo_children'):
                                        if self.generate_button in subitem.winfo_children():
                                            button_frame = subitem
                                            break
        
            # Pack the landmass controls either before the button frame or at the end if not found
            if button_frame:
                self.landmass_controls_frame.pack(fill="x", pady=5, before=button_frame)
            else:
                # Fallback: simply pack at the end
                self.landmass_controls_frame.pack(fill="x", pady=5)
        else:
            self.landmass_controls_frame.pack_forget()
        
        # Force update of the scrollregion after toggling controls
        self.mountain_tab.update_idletasks()
        # Find the scroll_canvas by traversing the widget hierarchy
        for child in self.mountain_tab.winfo_children():
            if isinstance(child, ttk.Frame):  # This is the controls_frame
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Canvas):  # This is the scroll_canvas
                        grandchild.configure(scrollregion=grandchild.bbox("all"))
                        break

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
        slider_label = ttk.Label(frame, text=label, anchor="w", width=20)
        slider_label.pack(side="left", padx=(0, 5))

        # Create the slider with expanded width
        slider = ttk.Scale(frame, from_=from_, to=to_, variable=self.vars[var_name],
                          orient="horizontal")
        slider.pack(side="left", fill="x", expand=True, padx=5)

        # Create the value display entry
        value_display = ttk.Entry(frame, width=8, justify="right")
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
        
        # Manual entry handling for the value display
        def on_value_change(event):
            try:
                new_value = value_display.get()
                if isinstance(resolution, int):
                    self.vars[var_name].set(int(new_value))
                else:
                    self.vars[var_name].set(float(new_value))
                self.update_noise_preview()
            except (tk.TclError, ValueError):
                # Reset to current value if invalid input
                update_value()
        
        # Slider event handling
        def on_slider_press(event):
            self.slider_active[var_name] = True
            update_value()
            
        def on_slider_release(event):
            self.slider_active[var_name] = False
            update_value()
            self.update_noise_preview()
        
        # Bind events
        self.vars[var_name].trace_add("write", update_value)
        slider.bind("<ButtonPress-1>", on_slider_press)
        slider.bind("<ButtonRelease-1>", on_slider_release)
        value_display.bind("<Return>", on_value_change)
        value_display.bind("<FocusOut>", on_value_change)
        
        # Initialize the display
        update_value()
        
        return slider


    def _make_scrollable_tab_left_scroll(self, parent):
        container = ttk.Frame(parent)
        container.pack(side="left", fill="both", expand=True)

        # Scrollbar on the left
        scrollbar = ttk.Scrollbar(container, orient="vertical")
        scrollbar.pack(side="left", fill="y")

        # Canvas to contain scrollable content
        canvas = tk.Canvas(container, yscrollcommand=scrollbar.set, borderwidth=0, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        # Scrollable content frame inside canvas
        scroll_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Configure scroll region dynamically
        def on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_frame_config)

        # Allow resizing the canvas when the window resizes
        def on_canvas_config(event):
            canvas.itemconfig("all", width=event.width)
        canvas.bind("<Configure>", on_canvas_config)

        return scroll_frame


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
        """Creates the grass map tab with controls and preview."""
        # Create the grass map tab
        self.grass_map_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.grass_map_tab, text="Grass Map")

        # Create left panel for controls with fixed width
        left_panel = ttk.Frame(self.grass_map_tab)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Group noise settings in a labeled frame
        noise_frame = ttk.LabelFrame(left_panel, text="Noise Settings", padding=10)
        noise_frame.pack(fill="x", pady=10)

        # Add sliders for grass density
        self.vars["grass_density"] = tk.DoubleVar(value=0.5)  # Default value for grass density
        density_slider = self._create_slider(noise_frame, "Grass Density", "grass_density", 0.0, 1.0, 0.01)
        # Override default binding to use grass map preview update
        density_slider.bind("<ButtonRelease-1>", lambda e: self.update_grass_map_preview())

        # Add sliders for noise amounts
        perlin_slider = self._create_slider(noise_frame, "Perlin Noise Amount", "perlin_noise_amount", 0.0, 4.0, 0.01)
        perlin_slider.bind("<ButtonRelease-1>", lambda e: self.update_grass_map_preview())
    
        simple_slider = self._create_slider(noise_frame, "Simple Noise Amount", "simple_noise_amount", 0.0, 2.0, 0.01)
        simple_slider.bind("<ButtonRelease-1>", lambda e: self.update_grass_map_preview())

        # Create appearance settings frame
        appearance_frame = ttk.LabelFrame(left_panel, text="Appearance", padding=10)
        appearance_frame.pack(fill="x", pady=10)

        # Add a slider for lightness adjustment
        self.vars["lightness"] = tk.DoubleVar(value=0.0)  # Default lightness value
        lightness_slider = self._create_slider(appearance_frame, "Lightness", "lightness", 0.0, 1.0, 0.01)
        lightness_slider.bind("<ButtonRelease-1>", lambda e: self.update_grass_map_preview())

        # Create buttons frame
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill="x", pady=10)

        # Add a button to generate/update the preview
        self._create_styled_button(button_frame, "Update Preview", self.update_grass_map_preview, style='TButton')
    
        # Add a button to export the grass map
        self._create_styled_button(button_frame, "Export Grass Map", self.export_grass_map, style='TButton')

        # Create the right panel for preview
        preview_frame = ttk.Frame(self.grass_map_tab)
        preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
        # Add a title for the preview section
        preview_title = ttk.Label(preview_frame, text="GRASS MAP PREVIEW", 
                                font=("Segoe UI", 12, "bold"))
        preview_title.pack(side="top", pady=(0, 10))
    
        # Create a styled canvas for the preview
        self.grass_map_preview_canvas = self._create_styled_canvas(preview_frame, width=600, height=600)
    
        # Add a note for the preview
        ttk.Label(preview_frame, text="Adjust the settings on the left to customize the grass distribution", 
                foreground="#95a5a6", font=("Segoe UI", 8)).pack(side="top", pady=(5, 0))

        self.grass_map_preview_photo = None  # Persistent reference to image
    
        # Generate initial preview
        self.update_grass_map_preview()

    def _create_image_import_tab(self):
        """Creates the image import tab with controls and preview"""
        # Create left panel for controls with fixed width
        left_panel = ttk.Frame(self.image_tab)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Import button
        import_frame = ttk.Frame(left_panel)
        import_frame.pack(fill="x", pady=5)
        self._create_styled_button(import_frame, "Import Image", self._import_image, style='TButton')

        # Add resize slider frame
        resize_frame = ttk.LabelFrame(left_panel, text="Image Size", padding=10)
        resize_frame.pack(fill="x", pady=10)

        # Add resize slider
        self.vars["image_size"] = tk.IntVar(value=512)  # Default size
        size_slider = self._create_slider(resize_frame, "Size", "image_size", 64, 4096, 64)
        # Remove the trace and add release binding for the size slider
        size_slider.bind("<ButtonRelease-1>", lambda e: self._update_image_preview())
    
        ttk.Label(resize_frame, text="Note: Aspect ratio will be preserved", 
                font=("Segoe UI", 8), foreground="#95a5a6").pack(pady=(5,0))

        # Create red channel controls frame
        red_frame = ttk.LabelFrame(left_panel, text="Red Channel", padding=10)
        red_frame.pack(fill="x", pady=10)

        # Add red channel sliders with delayed updates
        red_value_slider = self._create_slider(red_frame, "Red Value", "red_channel_value", 0.0, 1.0, 0.01)
        self.vars["red_channel_value"].set(0.5)  # Default to neutral value
        # Remove the trace and add release binding for the red value slider
        red_value_slider.bind("<ButtonRelease-1>", lambda e: self._update_image_preview())
    
        red_lightness_slider = self._create_slider(red_frame, "Lightness", "red_lightness", 0.0, 1.0, 0.01)
        self.vars["red_lightness"].set(0.5)  # Default to neutral value
        # Remove the trace and add release binding for the lightness slider
        red_lightness_slider.bind("<ButtonRelease-1>", lambda e: self._update_image_preview())

        # Add invert checkbox
        invert_frame = ttk.Frame(red_frame)
        invert_frame.pack(fill="x", pady=5)
        self.vars["invert_red"] = tk.BooleanVar(value=False)
        ttk.Checkbutton(invert_frame, text="Invert Values", variable=self.vars["invert_red"], 
                    command=self._update_image_preview).pack(side="left")

        # Green channel controls frame
        green_frame = ttk.LabelFrame(left_panel, text="Green Channel", padding=10)
        green_frame.pack(fill="x", pady=10)

        green_value_slider = self._create_slider(green_frame, "Green Value", "green_channel_value", 0.0, 1.0, 0.01)
        self.vars["green_channel_value"].set(0.5)  # Default to neutral value
        # Remove the trace and add release binding for the green value slider
        green_value_slider.bind("<ButtonRelease-1>", lambda e: self._update_image_preview())

        # Create blur controls frame
        blur_frame = ttk.LabelFrame(left_panel, text="Effects", padding=10)
        blur_frame.pack(fill="x", pady=10)

        # Add blur slider with delayed update
        blur_slider = self._create_slider(blur_frame, "Gaussian Blur", "gaussian_blur", 0.0, 50.0, 1.0)
        self.vars["gaussian_blur"].set(0.0)  # Default to no blur
        blur_slider.bind("<ButtonRelease-1>", lambda e: self._update_image_preview())

        # Create grayscale controls frame
        gray_frame = ttk.LabelFrame(left_panel, text="Grayscale Conversion", padding=10)
        gray_frame.pack(fill="x", pady=10)

        # Add grayscale conversion button
        self._create_styled_button(gray_frame, "Convert to Grayscale", self._convert_to_grayscale, style='TButton')

        # Add exposure slider with delayed update
        exposure_slider = self._create_slider(gray_frame, "Exposure", "grayscale_exposure", 0.5, 2.0, 0.05)
        self.vars["grayscale_exposure"].set(1.0)  # Default to neutral exposure
        # Remove the trace and add release binding for the exposure slider
        exposure_slider.bind("<ButtonRelease-1>", lambda e: self._update_exposure() if hasattr(self, 'is_grayscale') and self.is_grayscale else None)

        # Add export button in its own frame
        export_frame = ttk.Frame(left_panel)
        export_frame.pack(fill="x", pady=10)
        self._create_styled_button(export_frame, "Export Image", self._export_image, style='TButton')

        # Create preview frame on the right side
        preview_frame = ttk.Frame(self.image_tab)
        preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
        # Add a title for the preview section
        preview_title = ttk.Label(preview_frame, text="IMAGE PREVIEW", 
                                font=("Segoe UI", 12, "bold"))
        preview_title.pack(side="top", pady=(0, 10))
    
        # Create a styled canvas for the preview
        self.image_canvas = self._create_styled_canvas(preview_frame, width=600, height=600)
    
        # Add a note for the preview
        ttk.Label(preview_frame, text="Import an image using the button on the left", 
                foreground="#95a5a6", font=("Segoe UI", 8)).pack(side="top", pady=(5, 0))

    def _export_image(self):
        """Handle image export"""
        if not hasattr(self, 'processed_image'):
            messagebox.showwarning("Warning", "No image to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), 
                      ("JPEG files", "*.jpg;*.jpeg"),
                      ("All files", "*.*")])
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", "Image exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export image: {str(e)}")

    def _import_image(self):
        """Handle image import"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")])
        
        if file_path:
            try:
                # Load original image
                self.original_image = Image.open(file_path)
                self.imported_image = self.original_image.copy()
                
                # Calculate resize dimensions while maintaining aspect ratio
                target_size = self.vars["image_size"].get()
                width, height = self.original_image.size
                aspect_ratio = width / height
                
                if width > height:
                    new_width = min(target_size, 4096)
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = min(target_size, 4096)
                    new_width = int(new_height * aspect_ratio)
                    
                # Resize image
                self.imported_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self._update_image_preview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def _convert_to_grayscale(self, *args):
        """Convert the current red channel image to grayscale"""
        if self.processed_image is None:
            return

        try:
            # Convert the red channel to grayscale
            img_array = np.array(self.processed_image)
            
            # If the image is already grayscale (2D), use it directly
            if len(img_array.shape) == 2:
                values = img_array
            else:
                # Otherwise, get the red channel from RGB
                values = img_array[:, :, 0]
            
            # Store original grayscale values
            self.original_grayscale = values.copy()
            self.is_grayscale = True
            
            # Apply initial exposure
            self._update_exposure()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to grayscale: {str(e)}")

    def _update_exposure(self):
        """Update the exposure of the grayscale image"""
        if not hasattr(self, 'original_grayscale'):
            return

        try:
            # Convert to float for calculations
            values = self.original_grayscale.astype(float)
            
            # Apply exposure with improved control
            exposure = self.vars["grayscale_exposure"].get()
            if exposure != 1.0:
                values = values * exposure
                values = values.clip(0, 255)
            
            # Convert back to uint8
            values = values.astype(np.uint8)
            
            # Create grayscale image
            self.processed_image = Image.fromarray(values)

            # Create preview at consistent size (512x512)
            preview_size = 512
            width, height = self.processed_image.size
            aspect_ratio = width / height
            
            if width > height:
                preview_width = preview_size
                preview_height = int(preview_width / aspect_ratio)
            else:
                preview_height = preview_size
                preview_width = int(preview_height * aspect_ratio)
                
            preview_img = self.processed_image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
            preview = ImageTk.PhotoImage(preview_img)
            self.image_preview = preview
            
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                self.image_canvas.winfo_width() // 2,
                self.image_canvas.winfo_height() // 2,
                image=preview,
                anchor="center"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update exposure: {str(e)}")
        
    def _update_image_preview(self, *args):
        """Update the image preview with current settings"""
        if not hasattr(self, 'original_image'):
            return

        try:
            # Resize the actual imported image based on slider
            target_size = self.vars["image_size"].get()
            width, height = self.original_image.size
            aspect_ratio = width / height

            if width > height:
                new_width = min(target_size, 4096)
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = min(target_size, 4096)
                new_width = int(new_height * aspect_ratio)

            self.imported_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create a copy of the resized image for processing
            img = self.imported_image.copy()

            # Convert to numpy array for red channel processing
            img_array = np.array(img)
            rgb_array = np.zeros((img_array.shape[0], img_array.shape[1], 3), dtype=np.uint8)

            red_channel = img_array[:, :, 0].astype(float)
            if self.vars["invert_red"].get():
                red_channel = 255 - red_channel
            lightness = self.vars["red_lightness"].get()
            if lightness > 0:
                red_channel = red_channel + (255 - red_channel) * lightness
            red_value = self.vars["red_channel_value"].get()
            red_channel = (red_channel * red_value).clip(0, 255).astype(np.uint8)
            rgb_array[:, :, 0] = red_channel

            # Convert to RGBA for overlay
            img_rgba = Image.fromarray(rgb_array, mode="RGB").convert("RGBA")

            # Create green overlay
            alpha_val = int(self.vars["green_channel_value"].get() * 255)
            green_overlay = Image.new('RGBA', img_rgba.size, (0, 255, 0, alpha_val))

            # Composite green overlay
            img_with_overlay = Image.alpha_composite(img_rgba, green_overlay)
            self.processed_image = img_with_overlay.convert("RGB")

            # Apply Gaussian blur if set
            blur_radius = self.vars["gaussian_blur"].get()
            if blur_radius > 0:
                self.processed_image = self.processed_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            # Create preview image at consistent size (512x512)
            preview_size = 512
            if width > height:
                preview_width = preview_size
                preview_height = int(preview_width / aspect_ratio)
            else:
                preview_height = preview_size
                preview_width = int(preview_height * aspect_ratio)

            preview_img = self.processed_image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
            preview = ImageTk.PhotoImage(preview_img)
            self.image_preview = preview

            # Update canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                self.image_canvas.winfo_width() // 2,
                self.image_canvas.winfo_height() // 2,
                image=preview,
                anchor="center"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def _generate_landmass(self):
        """Generate heightmap with landmass shape, returning a 2D float numpy array normalized 0-1."""
        try:
            # Get parameters
            size = self.vars["landmass_size"].get()
            land_proportion = self.vars["landmass_land_proportion"].get()
            # water_level is not directly used in this version of landmass shaping, but kept for potential future use
            # water_level = self.vars["landmass_water_level"].get() 
            plain_factor = self.vars["landmass_plain_factor"].get()
            shore_height = self.vars["landmass_shore_height"].get()
            noise_scale = self.vars["landmass_noise_scale"].get()
            octaves = self.vars["landmass_octaves"].get()
            seed = self.vars["landmass_seed"].get()

            # Generate base terrain using FBM noise
            heightmap = generate_landmass_parallel(
                size=size,
                land_proportion=land_proportion,
                plain_factor=plain_factor,
                shore_height=shore_height,
                noise_scale=noise_scale,
                octaves=octaves,
                seed=seed
            )
            
            # Normalize heightmap to 0-1 range initially
            h_min_initial = np.min(heightmap)
            h_max_initial = np.max(heightmap)
            if h_max_initial == h_min_initial:
                heightmap = np.full((size, size), 0.5, dtype=np.float32)
            else:
                heightmap = (heightmap - h_min_initial) / (h_max_initial - h_min_initial)

            # Determine water threshold using np.percentile
            # (1.0 - land_proportion) gives the percentile of water.
            # E.g., if land_proportion is 0.7 (70% land), water is 30%, so we find the 30th percentile.
            if len(heightmap.flatten()) == 0: # Should not happen with proper size
                water_threshold = 0.5
            else:
                water_threshold = np.percentile(heightmap.flatten(), (1.0 - land_proportion) * 100.0)

            # --- Vectorized Shaping Logic ---
            under_water_mask = heightmap < water_threshold
            above_water_mask = ~under_water_mask

            # Process underwater areas
            # Lower underwater terrain by shore_height (relative to current 0-1 range)
            heightmap[under_water_mask] = heightmap[under_water_mask] - shore_height

            # Process above-water areas
            # Temporarily store above-water heights to avoid modifying them in place during calculation
            h_above = heightmap[above_water_mask]
            
            # Handle case where water_threshold might be 1.0 (all water or flat terrain at max)
            denominator = 1.0 - water_threshold
            if np.isclose(denominator, 0): # Avoid division by zero
                # If denominator is close to zero, it means water_threshold is very close to 1.0
                # This implies very little or no land above water_threshold to apply plain_factor to.
                # Or, all land is effectively at water_threshold.
                # Set h_norm_above to 0 to avoid issues, or handle as appropriate (e.g., no change).
                h_norm_above = np.zeros_like(h_above) # Or 0.0 if h_above could be scalar
            else:
                h_norm_above = (h_above - water_threshold) / denominator
            
            h_norm_above = np.clip(h_norm_above, 0.0, 1.0) # Ensure h_norm is in [0,1] before power
            h_shaped_above = h_norm_above ** plain_factor
            
            # Apply shaped heights back
            heightmap[above_water_mask] = water_threshold + h_shaped_above * (1.0 - water_threshold)
            # --- End of Vectorized Shaping Logic ---
            
            # Final normalization to ensure output is strictly 0-1
            heightmap = heightmap.astype(np.float32) 
            final_h_min = np.min(heightmap)
            final_h_max = np.max(heightmap)
            if final_h_max == final_h_min:
                heightmap = np.full((size, size), 0.5, dtype=np.float32)
            else:
                heightmap = (heightmap - final_h_min) / (final_h_max - final_h_min)

            return heightmap

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate landmass: {str(e)}\\nTraceback: {traceback.format_exc()}")
            # Return a default array in case of error to prevent None return
            default_size_val = 512 # Default fallback size
            try:
                default_size_val = self.vars.get("landmass_size", tk.IntVar(value=512)).get()
            except: # Broad except if self.vars or get() fails during error handling
                pass
            return np.full((default_size_val, default_size_val), 0.5, dtype=np.float32)

    def _normalize_dir(self, dx, dy):
        """Normalize a direction vector, returning random unit vector if zero"""
        length = np.sqrt(dx * dx + dy * dy)
        if length < 1e-6:
            angle = np.random.uniform(0, 2 * np.pi)
            return np.cos(angle), np.sin(angle)
        return dx / length, dy / length

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
        # Determine the noise type string from the UI
        current_noise_type_str = self.vars["noise_type"].get()

        if current_noise_type_str == "landmass":
            # Landmass generation uses its own parameters (including size) from self.vars
            return self._generate_landmass()

        # For other noise types, use the existing mapping and parameters
        if noise_type is None: # This noise_type is an enum, different from current_noise_type_str
            noise_type_map = {
                "perlin noise": NoiseTypeEnum.PERLINNOISE,
                "fractal noise": NoiseTypeEnum.FRACTALNOISE,
                "turbulence noise": NoiseTypeEnum.TURBULENCE
            }
            if current_noise_type_str not in noise_type_map:
                messagebox.showerror("Error", f"Unknown noise type: {current_noise_type_str}")
                return np.full((size, size), 0.5, dtype=np.float32) # Return default
            noise_type = noise_type_map[current_noise_type_str]

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

    def update_noise_preview(self, event=None):
        try:
            # Set the preview resolution 
            preview_res = 256  # Always use high quality

            # Generate the raw noise data
            noise_data = self._generate_noise_data(preview_res)
        
            # Create heightmap with canyons and other effects
            heightmap = self._create_heightmap(noise_data)
        
            # Convert to PIL image for display
            self.full_heightmap = Image.fromarray(heightmap)
        
            # Display the preview
            self._update_preview_canvas()
        except Exception as e:
            print(f"Preview generation error: {e}")
            import traceback
            traceback.print_exc()

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
            
                # Use the same focus points as the preview
                focus_x = getattr(self, "focus_x", 0.5)
                focus_y = getattr(self, "focus_y", 0.5)

                # Create a complete vars dictionary including all parameters
                vars_dict = {k: v.get() for k, v in self.vars.items()}
                vars_dict["focus_x"] = focus_x
                vars_dict["focus_y"] = focus_y

                # For landmass mode, generate using the existing function
                if vars_dict["noise_type"] == "landmass":
                    # For landmass, use the existing function which handles its own multiprocessing
                    noise_data = self._generate_landmass()
                else:
                    # For other noise types, use multiprocessing
                    num_workers = min(multiprocessing.cpu_count(), 4)
                    noise_data = self._generate_full_noise_data(size, vars_dict, num_workers)

                # Create heightmap with canyons applied (handled in _create_heightmap)
                heightmap = self._create_heightmap(noise_data)

                # Save the heightmap as an image
                img = Image.fromarray(heightmap)
                img.save(file_path)

                self.root.after(0, lambda: messagebox.showinfo("Success", f"Noise saved to {file_path}"))

            except Exception as e:
                self.root.after(0, lambda e=e: messagebox.showerror("Error", str(e)))
                import traceback
                traceback.print_exc()

            finally:
                self.root.after(0, lambda: self.generate_button.config(state="normal"))

        threading.Thread(target=worker, args=(file_path,), daemon=True).start()

    def _generate_full_noise_data(self, size, vars_dict, num_workers):
        # Check if the requested noise type is landmass
        if vars_dict.get("noise_type") == "landmass":
            # Landmass generation is not currently chunkable and uses self.vars directly.
            # Ensure self.vars is up-to-date if called from a context where vars_dict is the source of truth.
            # For now, assume self.vars accurately reflects UI settings for landmass when this is called.
            return self._generate_landmass() # This will use self.vars["landmass_size"], etc.

        # Proceed with chunk-based multiprocessing for other noise types
        tile_size = size // num_workers

        tasks = []
        for i in range(num_workers):
            start_row = i * tile_size
            end_row = (i + 1) * tile_size if i < num_workers - 1 else size
            # Pass the original size of the full image, not the potentially different landmass_size
            tasks.append((start_row, end_row, size, vars_dict))

        # Ensure TextureGenerator and NoiseTypeEnum are available to the child processes
        # This is handled by the re-import within _generate_chunk
        with multiprocessing.Pool(processes=num_workers) as pool:
            results = pool.map(TextureGeneratorGUI._generate_chunk, tasks)

        return np.vstack(results)

    @staticmethod
    def _generate_chunk(args):
        start_row, end_row, size, vars_dict = args
    
        from texture_generator import TextureGenerator, NoiseTypeEnum  # Re-import in child process
        generator = TextureGenerator(seed=vars_dict["seed"])
    
        noise_type = {
            "perlin noise": NoiseTypeEnum.PERLINNOISE,
            "fractal noise": NoiseTypeEnum.FRACTALNOISE,
            "turbulence noise": NoiseTypeEnum.TURBULENCE
        }[vars_dict["noise_type"]]
    
        # Initialize the chunk
        chunk = np.zeros((end_row - start_row, size), dtype=np.float32)
   
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

def _create_canyon_path_worker(args):
    """Worker function to generate a canyon path in parallel."""
    start_x, start_y, cx, cy, canyon_length, canyon_branch_density, canyon_seed, size = args
    import math
    from noise import snoise2
    import numpy as np
    
    # Direction vector toward center
    to_center_x = cx - start_x
    to_center_y = cy - start_y
    
    # Skip if already at center
    if abs(to_center_x) < 1 and abs(to_center_y) < 1:
        return None
    
    # Fixed random generator with canyon-specific seed
    fixed_rng = np.random.RandomState(canyon_seed)
    
    # Get distance to center
    dist_to_center = math.sqrt(to_center_x**2 + to_center_y**2)
    
    # Normalize direction vector
    if dist_to_center > 0:
        to_center_x /= dist_to_center
        to_center_y /= dist_to_center
    
    # Add slight random angle deviation
    angle_deviation = fixed_rng.uniform(-0.1, 0.1)
    rotated_x = to_center_x * math.cos(angle_deviation) - to_center_y * math.sin(angle_deviation)
    rotated_y = to_center_x * math.sin(angle_deviation) + to_center_y * math.cos(angle_deviation)
    to_center_x, to_center_y = rotated_x, rotated_y
    
    # Calculate max possible path length
    max_path_length = int(dist_to_center * 0.95)  # Maximum allowed length
    
    # Generate wiggle parameters from fixed RNG
    wiggle_freq = fixed_rng.uniform(30.0, 50.0)
    wiggle_amp = fixed_rng.uniform(0.2, 0.5)
    wiggle_phase = fixed_rng.uniform(0, 100)
    
    # Initialize canyon path
    path_points = [(start_x, start_y)]
    x, y = start_x, start_y
    
    # Draw path with wiggles
    step_count = 0
    
    # Generate the FULL path up to max_path_length
    while len(path_points) < max_path_length:
        step_count += 1
    
        # Get perlin noise value for wiggles
        perlin_val = snoise2(step_count/wiggle_freq, wiggle_phase, octaves=1)
    
        # Add random jitter
        jitter = fixed_rng.uniform(-0.05, 0.05)
    
        # Calculate wiggle angle
        wiggle_angle = perlin_val * wiggle_amp * math.pi + jitter
    
        # Add periodic larger bends
        if step_count % 8 == 0:
            wiggle_angle += fixed_rng.uniform(-0.2, 0.2)
        
        # Apply wiggle to direction
        dx = to_center_x * math.cos(wiggle_angle) - to_center_y * math.sin(wiggle_angle)
        dy = to_center_x * math.sin(wiggle_angle) + to_center_y * math.cos(wiggle_angle)
    
        # Use consistent step size
        step_size = fixed_rng.uniform(1.0, 2.0)
    
        # Move along path
        x += dx * step_size
        y += dy * step_size
    
        # Keep in bounds
        x = min(max(0, x), size-1)
        y = min(max(0, y), size-1)
    
        # Add point to path
        path_points.append((int(x), int(y)))
        
        # Stop if we're very close to center
        if math.sqrt((x - cx)**2 + (y - cy)**2) < 10:
            break
        
    # Create and store branch paths as well
    branches = []
    
    # Generate all potential branches (with fixed seed based on canyon seed)
    for i, (px, py) in enumerate(path_points):
        # Only generate branches beyond a certain point along main path
        path_progress = i / len(path_points)
        if 0.3 < path_progress < 0.7 and fixed_rng.random() < canyon_branch_density:
            # Use canyon_seed instead of main seed for branch seeds
            branch_seed = canyon_seed + i + int(px * 100 + py)
            branch_rng = np.random.RandomState(branch_seed)
            
            # Branch parameters
            branch_angle = branch_rng.uniform(-math.pi/4, math.pi/4)
            
            # Get direction vector of main path at this point
            if i < len(path_points) - 1:
                main_dx = path_points[i+1][0] - px
                main_dy = path_points[i+1][1] - py
            else:
                main_dx = path_points[i][0] - path_points[i-1][0]
                main_dy = path_points[i][1] - path_points[i-1][1]
            
            # Normalize
            length = math.sqrt(main_dx**2 + main_dy**2)
            if length > 0:
                main_dx /= length
                main_dy /= length
            
            # Rotate to get branch direction
            branch_dx = main_dx * math.cos(branch_angle) - main_dy * math.sin(branch_angle)
            branch_dy = main_dx * math.sin(branch_angle) + main_dy * math.cos(branch_angle)
            
            branch_length = branch_rng.uniform(20, 50)
            branch_points = [(int(px), int(py))]
            
            # Branch wiggle parameters
            branch_freq = branch_rng.uniform(20.0, 40.0)
            branch_amp = branch_rng.uniform(0.2, 0.4)
            branch_phase = branch_rng.uniform(0, 100)
            
            branch_x, branch_y = px, py
            
            # Create branch path
            for step in range(int(branch_length)):
                branch_perlin = snoise2(step/branch_freq, branch_phase, octaves=1)
                branch_wiggle = branch_perlin * branch_amp * math.pi + branch_rng.uniform(-0.05, 0.05)
                
                branch_dir_x = branch_dx * math.cos(branch_wiggle) - branch_dy * math.sin(branch_wiggle)
                branch_dir_y = branch_dx * math.sin(branch_wiggle) + branch_dy * math.cos(branch_wiggle)
                
                step_size = branch_rng.uniform(1.0, 1.5)
                branch_x += branch_dir_x * step_size
                branch_y += branch_dir_y * step_size
                
                # Keep in bounds
                if branch_x < 0 or branch_x >= size or branch_y < 0 or branch_y >= size:
                    break
                
                branch_points.append((int(branch_x), int(branch_y)))
            
            # Save this branch
            if len(branch_points) > 5:  # Only save non-trivial branches
                branches.append(branch_points)
    
    return {
        'main_path': path_points,
        'branches': branches
    }

def generate_landmass_chunk(start_y, end_y, size, noise_scale, octaves, seed):
        chunk = np.zeros((end_y - start_y, size), dtype=np.float32)
        for y in range(start_y, end_y):
            for x in range(size):
                nx = x / noise_scale
                ny = y / noise_scale
                chunk[y - start_y, x] = snoise2(nx, ny, octaves=octaves, persistence=0.5, lacunarity=2.0, base=seed)
        return chunk

def generate_landmass_parallel(size, land_proportion, plain_factor,
                                shore_height, noise_scale, octaves, seed):
    ctx = multiprocessing.get_context("spawn")
    num_workers = min(ctx.cpu_count(), 4)
    chunk_size = size // num_workers
    ranges = [
        (i * chunk_size,
        (i + 1) * chunk_size if i < num_workers - 1 else size,
        size, noise_scale, octaves, seed)
        for i in range(num_workers)
    ]

    with ctx.Pool(processes=num_workers) as pool:
        results = pool.starmap(generate_landmass_chunk, ranges)

    heightmap = np.vstack(results)

    # Normalize to [0, 1]
    h_min, h_max = heightmap.min(), heightmap.max()
    if h_max != h_min:
        heightmap = (heightmap - h_min) / (h_max - h_min)
    else:
        heightmap[:] = 0.5

    # Water threshold
    water_threshold = np.percentile(heightmap, (1.0 - land_proportion) * 100.0)
    under = heightmap < water_threshold
    above = ~under

    # Shore and plain shaping
    heightmap[under] -= shore_height
    denom = 1.0 - water_threshold
    h_above = heightmap[above]
    norm_above = np.clip((h_above - water_threshold) / denom, 0.0, 1.0) if denom > 1e-6 else np.zeros_like(h_above)
    heightmap[above] = water_threshold + norm_above**plain_factor * denom

    # Final normalization
    h_min, h_max = heightmap.min(), heightmap.max()
    return (heightmap - h_min) / (h_max - h_min) if h_max != h_min else np.full_like(heightmap, 0.5)
    
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