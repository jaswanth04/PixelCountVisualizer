import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from os.path import splitext
import multiprocessing as mp
import enum


class ColorSpaces(enum.Enum):
    RGB = 1
    YCbCr = 2
    HSV = 3
    CMY = 4


class PixelCountVisualizer:
    def __init__(self, input, colorspace=ColorSpaces.RGB, ylimit=100000) -> None:
        self._filename = input
        self._ylim = ylimit
        self._color_space = colorspace

        if self._color_space not in [ColorSpaces.RGB, ColorSpaces.YCbCr, ColorSpaces.CMY, ColorSpaces.HSV]:
            raise ValueError(
                "Value not found !!!, choose values from visualizer.ColorSpaces !!! Using RGB instead")

    def _create_and_run_viz(self, i, inp):
        fig = plt.figure(i)
        viz = IndividualPixelCountVisualizer(
            input=inp, fig=fig, colorspace=self._color_space, ylimit=self._ylim)
        viz.run()
        fig.show()
        plt.show()

    def run(self):
        if isinstance(self._filename, list):
            for i, f in enumerate(self._filename):
                p = mp.Process(target=self._create_and_run_viz, args=(i, f))
                p.start()
        else:
            fig = plt.figure(1)
            viz = IndividualPixelCountVisualizer(
                input=self._filename, colorspace=self._color_space, fig=fig, ylimit=self._ylim)
            viz.run()
            plt.show()


class IndividualPixelCountVisualizer:
    def __init__(self, input, fig, colorspace=ColorSpaces.RGB, ylimit=100000) -> None:
        """Initializes the class, a video name is given as input"""
        self._filename = input

        self._ch1_pixel_values = []
        self._ch2_pixel_values = []
        self._ch3_pixel_values = []

        self._color_space = colorspace

        if self._color_space == ColorSpaces.RGB:
            self._colors = ['red', 'green', 'blue']
            self._legend_names = ['red', 'green', 'blue']
        elif self._color_space == ColorSpaces.YCbCr:
            self._colors = ['yellow', 'red', 'blue']
            self._legend_names = ['Yellow', 'Chromium Red', 'Chromium Blue']
        elif self._color_space == ColorSpaces.HSV:
            self._colors = ['orange', 'lightgray', 'darkgray']
            self._legend_names = ['Hue', 'Saturation', 'Value']
        elif self._color_space == ColorSpaces.CMY:
            self._colors = ['cyan', 'magenta', 'yellow']
            self._legend_names = ['Cyan', 'Magenta', 'Yellow']
        else:
            raise ValueError(
                "Value not found !!!, choose values from visualizer.ColorSpaces !!!")

        self._ylim = ylimit

        self._figure = fig

        # _, ax = self._figure.subplots(2)
        self._intensity_plot = self._figure.add_subplot(2, 1, 1)
        self._image_plot = self._figure.add_subplot(2, 1, 2)

        self._count = 0
        self._frames = []
        # plt.subplots_adjust(bottom=0.25)

    def _plot_frame(self) -> None:
        """Plots each frame on the matplotlib widget"""
        t = range(256)
        lw = 3
        alpha = 0.5

        self._image_plot.axes.get_xaxis().set_visible(False)
        self._image_plot.axes.get_yaxis().set_visible(False)

        self._intensity_plot.set_xlim([0, 255])
        self._intensity_plot.set_ylim([0, self._ylim])

        histogram_ch1 = self._ch1_pixel_values[0]
        histogram_ch2 = self._ch2_pixel_values[0]
        histogram_ch3 = self._ch3_pixel_values[0]

        self._line_ch1, = self._intensity_plot.plot(
            t, histogram_ch1, c=self._colors[0], lw=lw, alpha=alpha)
        self._line_ch2, = self._intensity_plot.plot(
            t, histogram_ch2, c=self._colors[1], lw=lw, alpha=alpha)
        self._line_ch3, = self._intensity_plot.plot(
            t, histogram_ch3, c=self._colors[2], lw=lw, alpha=alpha)

        img = self._frames[0]

        if self._color_space == ColorSpaces.YCbCr:
            self._im_plot = self._image_plot.imshow(
                cv2.cvtColor(img, cv2.COLOR_YCR_CB2RGB))
        elif self._color_space == ColorSpaces.RGB:
            self._im_plot = self._image_plot.imshow(img)
        elif self._color_space == ColorSpaces.HSV:
            self._im_plot = self._image_plot.imshow(
                cv2.cvtColor(img, cv2.COLOR_HSV2RGB))
        elif self._color_space == ColorSpaces.CMY:
            rgb_image = 255 - img
            self._im_plot = self._image_plot.imshow(rgb_image)

        self._intensity_plot.legend((self._line_ch1, self._line_ch2, self._line_ch3),
                                    self._legend_names, loc="upper right", shadow=True)

        self._figure.show()

    def _update(self, frame_num) -> None:
        """Updates the value of the frame, based on the frame number in the graph"""

        frame_num = int(frame_num - 1)
        self._line_ch1.set_ydata(self._ch1_pixel_values[frame_num])
        self._line_ch2.set_ydata(self._ch2_pixel_values[frame_num])
        self._line_ch3.set_ydata(self._ch3_pixel_values[frame_num])

        if self._color_space == ColorSpaces.YCbCr:
            self._im_plot.set_data(cv2.cvtColor(
                self._frames[frame_num], cv2.COLOR_YCR_CB2RGB))
        elif self._color_space == ColorSpaces.RGB:
            self._im_plot.set_data(self._frames[frame_num])
        elif self._color_space == ColorSpaces.HSV:
            self._im_plot.set_data(cv2.cvtColor(
                self._frames[frame_num], cv2.COLOR_HSV2RGB))
        elif self._color_space == ColorSpaces.CMY:
            rgb_im = 255 - self._frames[frame_num]
            self._im_plot.set_data(rgb_im)

    def _process_image(self) -> None:
        img = cv2.imread(self._filename)

        if self._color_space == ColorSpaces.RGB:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        elif self._color_space == ColorSpaces.YCbCr:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        elif self._color_space == ColorSpaces.HSV:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        elif self._color_space == ColorSpaces.CMY:
            img = 255 - img

        (ch1, ch2, ch3) = cv2.split(img)

        histogram_ch1 = cv2.calcHist([ch1], [0], None, [256], [0, 255])
        histogram_ch2 = cv2.calcHist([ch2], [0], None, [256], [0, 255])
        histogram_ch3 = cv2.calcHist([ch3], [0], None, [256], [0, 255])

        t = range(256)
        lw = 3
        alpha = 0.5

        self._image_plot.axes.get_xaxis().set_visible(False)
        self._image_plot.axes.get_yaxis().set_visible(False)

        self._intensity_plot.set_xlim([0, 255])
        self._intensity_plot.set_ylim([0, self._ylim])

        line_ch1, = self._intensity_plot.plot(
            t, histogram_ch1, c=self._colors[0], lw=lw, alpha=alpha)
        line_ch2, = self._intensity_plot.plot(
            t, histogram_ch2, c=self._colors[1], lw=lw, alpha=alpha)
        line_ch3, = self._intensity_plot.plot(
            t, histogram_ch3, c=self._colors[2], lw=lw, alpha=alpha)

        self._intensity_plot.legend(
            (line_ch1, line_ch2, line_ch3), self._legend_names, loc="upper right", shadow=True)

        if self._color_space == ColorSpaces.YCbCr:
            im_plot = self._image_plot.imshow(
                cv2.cvtColor(img, cv2.COLOR_YCR_CB2RGB))
        elif self._color_space == ColorSpaces.RGB:
            im_plot = self._image_plot.imshow(img)
        elif self._color_space == ColorSpaces.HSV:
            im_plot = self._image_plot.imshow(
                cv2.cvtColor(img, cv2.COLOR_HSV2RGB))
        elif self._color_space == ColorSpaces.CMY:
            rgb_im = 255 - img
            im_plot = self._image_plot.imshow(rgb_im)

        self._figure.show()
        # return self._figure

    def _process_video(self) -> None:
        capture = cv2.VideoCapture(self._filename)

        while True:
            (grabbed, frame) = capture.read()

            if not grabbed:
                break

            if self._color_space == ColorSpaces.RGB:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            elif self._color_space == ColorSpaces.YCbCr:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            elif self._color_space == ColorSpaces.HSV:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            elif self._color_space == ColorSpaces.CMY:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = 255 - frame

            (ch1, ch2, ch3) = cv2.split(frame)

            histogram_ch1 = cv2.calcHist([ch1], [0], None, [256], [0, 255])
            histogram_ch2 = cv2.calcHist([ch2], [0], None, [256], [0, 255])
            histogram_ch3 = cv2.calcHist([ch3], [0], None, [256], [0, 255])

            self._frames.append(frame)

            self._ch1_pixel_values.append(histogram_ch1)
            self._ch2_pixel_values.append(histogram_ch2)
            self._ch3_pixel_values.append(histogram_ch3)

            self._count += 1

        pixel_axis = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor="White")
        self._pixel_slider = Slider(pixel_axis, 'Frame',
                                    0, self._count, valinit=0)
        self._pixel_slider.on_changed(self._update)
        self._plot_frame()

    def run(self) -> None:
        """Public. Should be used to run the plot, once the object is shown"""

        _, file_ext = splitext(self._filename)

        if (file_ext.lower() == '.jpg') or (file_ext.lower() == '.jpeg'):
            self._process_image()
        elif (file_ext == '.mp4') or (file_ext == '.mov'):
            self._process_video()
        else:
            raise TypeError("Only jpeg and mp4, mov are supported")
