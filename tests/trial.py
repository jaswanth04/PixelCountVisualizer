from src.visualizer import visualizer as viz
import matplotlib.pyplot as plt

def main():
    image_name = "data/hand.jpeg"
    
    video_path = "data/160330_5_Compass1_Mpeg4_4K.mov"
    subway_path = "data/subway.mp4"
    robber = "data/robber.mp4"
    racoon = "data/racoon.mp4"
    delivery_red_video_path = "data/delivery_red.mp4"
    delivery_blue_video_path = "data/delivery_blue.mp4"
    im_list = ["data/5face5ed3e7962e463209568-1605167646002.JPEG",
               "data/train_data/5face4a3e9a6c8325cb2f826-1605166899755.JPEG",
               "data/train_data/5facdced6360b67c4b54142d-1605166559036.JPEG"]


    # Visualizing the video of red delivery guy
    red_pixel_visualizer = viz.PixelCountVisualizer(
        delivery_red_video_path, ylimit=5000)

    red_pixel_visualizer.run()

    # Visualizing the video of blue delivery guy
    blue_pixel_visualizer = viz.PixelCountVisualizer(
        robber, ylimit=5000)
    blue_pixel_visualizer.run()


# Visualizing the image
    image_viz = viz.PixelCountVisualizer(input=image_name,  ylimit=5000)
    image_viz.run()

    # Visualizing multiple images using CMY Color Spaces
    multi_im_viz = viz.PixelCountVisualizer(
        im_list, colorspace=viz.ColorSpaces.CMY, ylimit=10000)
    multi_im_viz.run()

    # Visualizing multiple images in RGB Color Spaces
    multi_im_viz_rgb = viz.PixelCountVisualizer(
        im_list, colorspace=viz.ColorSpaces.RGB, ylimit=10000)
    multi_im_viz_rgb.run()

    # Visualizing multiple videos in RGB Color Spaces
    multi_video_viz_rgb = viz.PixelCountVisualizer(
        [delivery_blue_video_path, delivery_red_video_path], colorspace=viz.ColorSpaces.RGB, ylimit=5000)
    multi_video_viz_rgb.run()

    # Visualizing multiple videos in with wrong color spaces
    multi_video_viz = viz.PixelCountVisualizer(
        [delivery_blue_video_path, delivery_red_video_path], colorspace="ads", ylimit=5000)
    multi_video_viz.run()

    # Visualizing video in YCbCr color space
    robber_viz_ycbcr = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.YCbCr, ylimit=80000)
    robber_viz_ycbcr.run()

    # Visualizing video in HSV color space
    robber_viz_hsv = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.HSV, ylimit=20000)
    robber_viz_hsv.run()

    # Visualizing video in CMY color space
    robber_viz_cmy = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.CMY, ylimit=4000)
    robber_viz_cmy.run()


if __name__ == "__main__":
    main()
