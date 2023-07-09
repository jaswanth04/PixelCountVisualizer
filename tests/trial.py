from src.visualizer import visualizer as viz
import matplotlib.pyplot as plt
# from ../visualizer/visualizer import PixelCountVisualizer


def main():
    image_name = "data/hand.jpeg"
    # video_path = "/Users/jaswantjonnada/Documents/BP_anamoly_detection/data/AnomalyDetectionExps1/MPOPPCPH21790001/random_background_followed_by_finger_placement/video_snap_16512063555422022-04-29T04:26:03Z.mp4"

    video_path = "data/160330_5_Compass1_Mpeg4_4K.mov"
    subway_path = "data/subway.mp4"
    robber = "data/robber.mp4"
    racoon = "data/racoon.mp4"
    delivery_red_video_path = "data/delivery_red.mp4"
    delivery_blue_video_path = "data/delivery_blue.mp4"
    im_list = ["data/5face5ed3e7962e463209568-1605167646002.JPEG",
               "data/train_data/5face4a3e9a6c8325cb2f826-1605166899755.JPEG",
               "data/train_data/5facdced6360b67c4b54142d-1605166559036.JPEG"]

    red_pixel_visualizer = viz.PixelCountVisualizer(
        delivery_red_video_path, ylimit=5000)

    red_pixel_visualizer.run()

    blue_pixel_visualizer = viz.PixelCountVisualizer(
        robber, ylimit=5000)
    blue_pixel_visualizer.run()

    image_viz = viz.PixelCountVisualizer(input=image_name,  ylimit=5000)
    image_viz.run()

    multi_im_viz = viz.PixelCountVisualizer(
        im_list, colorspace=viz.ColorSpaces.CMY, ylimit=10000)
    multi_im_viz.run()

    multi_im_viz_rgb = viz.PixelCountVisualizer(
        im_list, colorspace=viz.ColorSpaces.RGB, ylimit=10000)
    multi_im_viz_rgb.run()

    multi_video_viz_rgb = viz.PixelCountVisualizer(
        [delivery_blue_video_path, delivery_red_video_path], colorspace=viz.ColorSpaces.RGB, ylimit=5000)
    multi_video_viz_rgb.run()

    multi_video_viz = viz.PixelCountVisualizer(
        [delivery_blue_video_path, delivery_red_video_path], colorspace="ads", ylimit=5000)
    multi_video_viz.run()

    robber_viz_ycbcr = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.YCbCr, ylimit=80000)
    robber_viz_ycbcr.run()

    robber_viz_hsv = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.HSV, ylimit=20000)
    robber_viz_hsv.run()

    robber_viz_cmy = viz.PixelCountVisualizer(
        robber, colorspace=viz.ColorSpaces.CMY, ylimit=4000)
    robber_viz_cmy.run()


if __name__ == "__main__":
    main()
