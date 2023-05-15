import threading
import time
import math

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

from PIL import ImageGrab
import imageio

class Pendulum:
    TIME_STEP = 0.05 # Time step in seconds

    def __init__(self, length, angle, mass):
        # Set parameters
        self.length = length
        self.angle = angle
        self.mass = mass

        # Default values
        self.is_running = False
        self.__angular_velocity = 0
        self.__dt = self.TIME_STEP

    # Update simulation
    def update(self):
        t0 = time.perf_counter()
        self.total_time_t0 = t0

        # Simulation loop
        while self.is_running:
            # Update the position of the pendulum
            acceleration = -9.81 / self.length * math.sin(self.angle)
            self.__angular_velocity += acceleration * self.__dt
            self.angle += self.__angular_velocity * self.__dt

            # Compute the time taken by this iteration of the simulation
            t1 = time.perf_counter()
            self.total_time = t1 - self.total_time_t0
            elapsed_time = t1 - t0
            t0 = t1

            # Sleep for the remaining time until dt is reached
            time.sleep(max(0, self.__dt - elapsed_time))

    # Start simulation
    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            # Create and start the simulation thread 
            self.thread = threading.Thread(target=self.update)
            self.thread.start()

    # Stop simulation
    def stop_simulation(self):
        if self.is_running:
            # Stop thread
            self.is_running = False
            self.thread.join()


class Window(tk.Frame):
    # Constants
    DEFAULT_ANGLE = 45 # Degees
    DEFAULT_MASS = 10
    DEFAULT_LENGTH = 100
    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 300
    CANVAS_UPDATE_INTERVAL = 200 # ms

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Pendulum Animation')
        self.frames = [] # Define empty frame list for animation recording

        # Create the left side of the window
        self.frame_animation = ttk.Frame(self.master)

        # Create the canvas (drawable area) on top
        self.bob = None
        self.wire = None
        self.canvas = tk.Canvas(self.frame_animation, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg='white')
        self.canvas.pack(side=tk.TOP)

        # Create the angle widgets
        self.frame_angle = ttk.Frame(self.frame_animation)
        # Angle label
        self.label_angle = ttk.Label(self.frame_angle, text='Angle (deg)')
        self.label_angle.pack(side=tk.LEFT, padx=10)
        # Angle text field
        self.angle_string = tk.StringVar(value=str(self.DEFAULT_ANGLE))
        self.entry = ttk.Entry(self.frame_angle, textvariable=self.angle_string)
        self.entry.pack(side=tk.LEFT)
        self.frame_angle.pack(pady=10)
        
        # Create the mass widgets
        self.frame_mass = ttk.Frame(self.frame_animation)
        # Mass label
        self.label_mass = ttk.Label(self.frame_mass, text='Mass (kg)')
        self.label_mass.pack(side=tk.LEFT, padx=10)
        # Mass slider
        self.slider_mass = ttk.Scale(self.frame_mass, from_=0, to=self.DEFAULT_MASS, value=self.DEFAULT_MASS, command=self.slider_mass_change)
        self.slider_mass.pack(side=tk.LEFT)
        self.label_mass_value = ttk.Label(self.frame_mass, text=str(self.DEFAULT_MASS))
        self.label_mass_value.pack(side=tk.LEFT)
        self.frame_mass.pack(pady=10)
        
        # Create the length widgets
        self.frame_length = ttk.Frame(self.frame_animation)
        # Length label
        self.label_length = ttk.Label(self.frame_length, text='Length (m)')
        self.label_length.pack(side=tk.LEFT, padx=10)
        # Length slider
        self.slider_length = ttk.Scale(self.frame_length, from_=0.5, to=self.DEFAULT_LENGTH, value=self.DEFAULT_LENGTH, command=self.slider_length_change)
        self.slider_length.pack(side=tk.LEFT)
        self.label_length_value = ttk.Label(self.frame_length, text=str(self.DEFAULT_LENGTH))        
        self.label_length_value.pack(side=tk.LEFT)
        self.frame_length.pack(pady=10)

        # Place the left side of the window
        self.frame_animation.grid(row=0, column=0, padx=5)

        ## Create the right side of the window
        self.frame_matplotlib = ttk.Frame(self.master)
        # Create the canvas for matplotlib
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas_matplotlib = FigureCanvasTkAgg(self.fig, self.frame_matplotlib)  # A tk.DrawingArea.
        self.canvas_matplotlib.draw()
        # Matplotlibe toolbar
        toolbar = NavigationToolbar2Tk(self.canvas_matplotlib, self.frame_matplotlib)
        toolbar.update()
        self.canvas_matplotlib.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Place the right side of the window
        self.frame_matplotlib.grid(row=0, column=1, padx=5, pady=15)

        # Create the bottom part of the window
        self.frame_commands = ttk.Frame(self.master)
        # Create the start/stop button
        self.start_button = ttk.Button(self.frame_commands, text='Start', command=self.toggle_animation)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        # Create the animation checkbox
        self.animation_checkbox_value = tk.BooleanVar();
        self.animation_checkbox = ttk.Checkbutton(self.frame_commands, text="Save animation", variable=self.animation_checkbox_value)
        self.animation_checkbox.pack(side=tk.LEFT, padx=10, pady=10)
        # Place the bottom part of the window
        self.frame_commands.grid(row=1, column=0, columnspan=2, pady=20)

        # Create the pendulum simulation with parameters
        self.pendulum = Pendulum(self.DEFAULT_LENGTH, math.radians(self.DEFAULT_ANGLE), self.DEFAULT_MASS)

    # Callback for mass slider modification
    def slider_mass_change(self, value):
        # Set slider text value
        self.label_mass_value['text'] = '{:.1f}'.format(self.slider_mass.get())
        # Get the slider value
        self.pendulum.mass = self.slider_mass.get()

    # Callback for length slider modification
    def slider_length_change(self, value):
        # Set slider text value
        self.label_length_value['text'] = '{:.1f}'.format(self.slider_length.get())
        # Get the slider value
        self.pendulum.length = self.slider_length.get()

    # Callback for button click
    def toggle_animation(self):
        if self.pendulum.is_running:
            # Stop simulation
            self.pendulum.stop_simulation()
            # Enable angle text field and save animation checkbox
            self.entry['state'] = "enabled"
            self.animation_checkbox['state'] = "enabled"
            # Toggle button label
            self.start_button.config(text='Start')
            # Stop canvas update
            self.canvas.after_cancel(self.after_id)
            # Save grabbed animation in a video if requested
            if self.animation_checkbox_value.get():
                # Open a dialog
                savepath = filedialog.asksaveasfilename(initialdir=".", title="Save animation video", filetypes=(("Mp4 video files","*.mp4"),("All files","*.*")))
                if savepath:
                    self.start_button["state"] = "disabled"
                    with imageio.get_writer(savepath,fps=int(len(self.frames)/self.pendulum.total_time)) as video_writer:
                        for frame in self.frames:
                            # Convert the PIL image to a numpy array
                            frame_array = imageio.core.util.asarray(frame)

                            # Add the numpy array to the video writer
                            video_writer.append_data(frame_array)
                    self.start_button["state"] = "enabled"
                self.frames = []
        else:
            self.initialise_plot()
            # Set angle value from text field
            self.pendulum.angle = math.radians(int(self.angle_string.get()))
            # Start simulation
            self.pendulum.start_simulation()
            # Disable angle text field and save animation checkbox becasue they cannot be changed during simulation
            self.entry['state'] = "disabled"
            self.animation_checkbox['state'] = "disabled"
            # Toggle button label
            self.start_button.config(text='Stop')
            # Start canvas update
            self.__t0 = time.perf_counter()
            self.update_canvas()

    # Function to draw the pendulum
    def update_canvas(self):
        # Convert angle to pixel coordinates
        x = self.CANVAS_WIDTH/2 + self.pendulum.length * math.sin(self.pendulum.angle)
        y = self.CANVAS_HEIGHT/2 + self.pendulum.length * math.cos(self.pendulum.angle)

        # Update the canvas and matplotlib plot
        if self.wire is None:
            self.wire = self.canvas.create_line(self.CANVAS_WIDTH/2, self.CANVAS_HEIGHT/2, x, y, width=2, fill='black')
        else:
            self.canvas.coords(self.wire, self.CANVAS_WIDTH/2, self.CANVAS_HEIGHT/2, x, y)    
        if self.bob is None:
            self.bob = self.canvas.create_oval(x - self.pendulum.mass, y - self.pendulum.mass, x + self.pendulum.mass, y + self.pendulum.mass, fill='blue')
        else:
            self.canvas.coords(self.bob, x - self.pendulum.mass, y - self.pendulum.mass, x + self.pendulum.mass, y + self.pendulum.mass)        
        self.update_plot()

        if self.animation_checkbox_value.get():
            # Define the area to be grabbed
            x1 = self.master.winfo_rootx()
            y1 = self.master.winfo_rooty()
            x2 = x1 + self.master.winfo_width()
            y2 = y1 + self.master.winfo_height()
            # Grab the window
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            self.frames.append(img)

        # Redraw again after set interval
        t1 = time.perf_counter()
        elapsed_time = int((t1 - self.__t0)*1000)
        self.__t0 = t1
        wait_time = max(0, self.CANVAS_UPDATE_INTERVAL - elapsed_time)
        self.after_id = self.canvas.after(wait_time, self.update_canvas)

    # Initialise matplotlib plot
    def initialise_plot(self):
        # Cleanup existing plots
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [])
        # Set initial plot limits
        self.ax.set_ylim(-90, 90)
        self.ax.set_xlim(0, 10)
        # Set the first point pf the plot
        self.line.set_xdata([0])
        self.line.set_ydata([self.DEFAULT_ANGLE])

    # Add one simulation point to matplotlib plot
    def update_plot(self):
        # Append new point
        self.line.set_data(np.append(self.line.get_xdata(), self.pendulum.total_time), np.append(self.line.get_ydata(), math.degrees(self.pendulum.angle)))
        # Adjust plot x limits to show the entire plot
        self.ax.set_xlim(0, self.pendulum.total_time)
        # Redraw the plot
        self.fig.canvas.draw()


# Close app
def quit_app(root):
    root.quit() # Stop mainloop
    root.destroy() # This is necessary on Windows to prevent Fatal Python Error: PyEval_RestoreThread: NULL tstate


def main():
    # Initialise main window
    root = tk.Tk()
    window = Window(root)

    # Bind the eascape key to quit the program
    root.bind('<Escape>', lambda e: quit_app(root))

    # Set window close event
    root.protocol("WM_DELETE_WINDOW", lambda: quit_app(root))
    # Start GUI loop
    window.mainloop()

    # If you put root.destroy() here, it will cause an error if the window is closed with the window manager.

    # Wait for the simulation thread to stop
    if window.pendulum.is_running:
        window.pendulum.stop_simulation()


if __name__ == '__main__':
    main()
