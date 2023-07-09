from gettext import install
from setuptools import setup

long_description = """

      Visualizing the color spaces of a video or an image is difficult. 

      v 1.0:

      Used to visualize color spaces images, videos. Also can be used to compare certain videos
"""

setup(name="pixel_count_visualizer",
      version="1.0",
      description="A package to interactively visualize color spaces of a video or an Image",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Jaswant Jonnada",
      packages=['src/visualizer'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
          ],
      py_modules="pixel_visualizer",
      install_requires=['opencv-python', 'matplotlib'])
