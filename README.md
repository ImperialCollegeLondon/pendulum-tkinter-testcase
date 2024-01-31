# Pendulum Tkinter testcase

This is a simple test case to show how to build a Graphical User Interface (GUI) using [Tkinter](https://docs.python.org/3/library/tkinter.html) in Python.

The rationale for choosing Tkinter is that it's included in any modern distribution of Python, it's easy to use, and it works cross-platform. There are other more expressive frameworks available (e.g., [guikit](https://github.com/ImperialCollegeLondon/guikit/tree/develop)), but this is a simple solution for putting together simple and portable interfaces for teaching and research.

## Code

The single *pendulum_tkinter_testcase.py* Python file contains two classes and the main function.
The classes are:

* **Pendulum**: simple simulation of the movement of a pendulum given its mass, wire length, and starting angle. The simulation runs in a separated thread. The Pendulum class is not aware of the GUI.
* **Window**: Tkinter management, from layout to user events, from canvas animation to Matplotlib plotting.

There are class constants that can be tweaked as needed, especially about the simulation and animation update rates.

### Widgets

The code shows how to create an interactive GUI with [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html) [buttons](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Button.html), [checkboxes](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Checkbutton.html), [sliders](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Scale.html), and [text fields](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Entry.html) arranged using tk [grid](https://tkdocs.com/tutorial/grid.html) and pack layouts.

In addition, it shows how to add a tk [canvas](https://tkdocs.com/tutorial/canvas.html), use it to draw simple shapes, and animate them.

Finally it [embeds](https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html) a [Matplotlib](https://matplotlib.org/) plot that is updated while the animation runs. 

## Environment

The code has been developed and tested on Ubuntu 22.04 LTS with [conda](https://docs.conda.io/en/latest/). In the *conda* directory of this repository there is a file that can be used to create the same setup on different systems. 

You can create a working *pendulum_tkinter_testcase* conda environment by running:
```
conda env create -f environment.yml
```

If you prefer to create the environment by yourself, you can run
```
conda create --name pendulum_tkinter_testcase -c conda-forge python=3.11.3 tk matplotlib imageio imageio-ffmpeg
``` 
that will add all the required dependencies.

Please note that the two commands work with [mamba](https://github.com/mamba-org/mamba) as well.

If you do not want to use conda, you can just install the same required dependencies to your Python distribution. 

## Look

The code uses [tkinter](https://docs.python.org/3/library/tkinter.html) and [tkinter.ttk](https://docs.python.org/3/library/tkinter.ttk.html) modules. The second provides access to the Tk themed widget set, so it gives options to customise the look of your GUI. Ttk widgets often have less options than the equivalent Tkinter ones, but in this case they are good enough.

If you prefer a more modern style you can try [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) instead. It was not used for this test case because it isn't available in conda and should be installed using [pip](https://packaging.python.org/en/latest/key_projects/#pip). 

When it's available you can use it instead of tkinter.ttk by changing the line
```
from tkinter import ttk
```
in *pendulum_tkinter_testcase.py* with
```
import ttkbootstrap as ttk
```

## Packaging

If can use [PyInstaller](https://pyinstaller.org) to bundle the program and all its dependencies into a single package. 
You can install PyInstaller directly in conda by running
```
conda install pyinstaller
```

To use it, type
```
pyinstaller --onefile --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder pendulum_tkinter_testcase.py
```

PyInstaller will create the *dist* directory containing the single file to distribute. The additional parameters are required to include all the dependencies needed to support ImageTk (see this [post](https://stackoverflow.com/questions/52675162/pyinstaller-doesnt-play-well-with-imagetk-and-tkinter)). 

Please note that the resulting executable file is platform dependent, so you need to repeat the process in each operating system you plan to support.
On Windows, the resulting executable may be detected as malware by some antivirus. See this [post](https://stackoverflow.com/questions/77257748/pyinstaller-exe-marked-as-virus) for additional details. 

## Limitations

The simulation and the GUI are quite minimal. The main thing missing is the possibility to interactively see the changes in the pendulum bob weight and wire length before starting the simulation. The main idea was to show how to create a useful test case in less than 300 lines of code (comments included). This is the reason why thre are also long lines that could be splitted. 

Improving the code is a nice way to experiment with Tkinter and understand how it works, so it's left to the user.

