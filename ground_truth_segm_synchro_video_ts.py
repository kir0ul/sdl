#!/usr/bin/env python3
#
# Run: `panel serve ground_truth_segm_synchro_video_ts.py`

from pathlib import Path
import hvplot.pandas  # noqa: F401
import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn

from PIL import Image
import cv2

import warnings
import datetime as dt
from tqdm.auto import tqdm
from segmentation_utils import get_gtdict_filenames, read_h5_data, ts2df


# PRIMARY_COLOR = "#0072B5"
# SECONDARY_COLOR = "#B54300"
# CSV_FILE = (
#     "https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv"
# )
# hv.extension('bokeh')

pn.extension()
pn.extension(design="material", sizing_mode="stretch_width")
pn.config.inline = True  # Make the app work offline
warnings.filterwarnings("ignore", category=UserWarning)


##### To be changed #####
DATA_PATH_ROOT = Path(".") / "data"
GROUND_TRUTH_SEGM_FILE = DATA_PATH_ROOT.parent / "segm_ground_truth.json"
FILENUM = 1
##### To be changed #####


def get_line_plot(traj, epoch_queried, gt_segm_dict=None, show_segments=None):
    slider_ts = dt.datetime.fromtimestamp(epoch_queried)  # - dt.timedelta(hours=1)
    vline = hv.VLine(slider_ts).opts(color="black", line_dash="dashed", line_width=3)
    lineplot_tf = traj.hvplot(x="timestamp", y=["x", "y", "z"], height=400).opts(
        xlabel="Time", ylabel="Position"
    )
    lineplot_grip = traj.hvplot(x="timestamp", y=["gripper"], label="gripper")
    # overlay.opts(opts.VLine(color="red", line_dash='dashed', line_width=6))
    overlay = lineplot_tf * lineplot_grip * vline

    y_low = np.min([traj.x.min(), traj.y.min(), traj.z.min(), traj.gripper.min()])
    y_high = np.max([traj.x.max(), traj.y.max(), traj.z.max(), traj.gripper.max()])
    y_range = np.abs(y_high - y_low) / 2
    y_top = y_high + 0.1 * y_range
    y_bottom = y_low - 0.1 * y_range

    palette = hv.Palette.default_cycles["Set1"]
    if show_segments == "Segmented":
        for idx, sect_key in enumerate(gt_segm_dict["segments"]):
            sect_val = gt_segm_dict["segments"][sect_key]
            if isinstance(sect_val, list):
                for sect_cur in sect_val:
                    xs = traj.timestamp[
                        (
                            traj.timestamp
                            > pd.Timestamp(
                                dt.datetime.fromtimestamp(sect_cur["ini"]),
                                # - dt.timedelta(hours=1),
                                tz="EST",
                            )
                        )
                        & (
                            traj.timestamp
                            < pd.Timestamp(
                                dt.datetime.fromtimestamp(sect_cur["end"]),
                                # - dt.timedelta(hours=1),
                                tz="EST",
                            )
                        )
                    ] - dt.timedelta(hours=5)
                    spread = hv.Spread(
                        (
                            xs,
                            y_range,
                            y_range - y_bottom,
                            y_range + y_top,
                        ),
                        label=sect_key,
                    ).opts(fill_alpha=0.15, color=palette[idx])
                    overlay = overlay * spread
            elif isinstance(sect_val, dict):
                xs = traj.timestamp[
                    (
                        traj.timestamp
                        > pd.Timestamp(
                            dt.datetime.fromtimestamp(sect_val["ini"]),
                            # - dt.timedelta(hours=1),
                            tz="EST",
                        )
                    )
                    & (
                        traj.timestamp
                        < pd.Timestamp(
                            dt.datetime.fromtimestamp(sect_val["end"]),
                            # - dt.timedelta(hours=1),
                            tz="EST",
                        )
                    )
                ] - dt.timedelta(hours=5)
                spread = hv.Spread(
                    (
                        xs,
                        y_range,
                        y_range - y_bottom,
                        y_range + y_top,
                    ),
                    label=sect_key,
                ).opts(fill_alpha=0.15, color=palette[idx])
                overlay = overlay * spread
            else:
                raise ValueError("Unexpected value in ground truth JSON file")

    return overlay.opts(ylim=(y_bottom, y_top))


def conv_epoch2frame(
    epoch_queried, epoch_ini, total_frames, epoch_end, synchro_vid=None, synchro_ts=None
):
    frame_synchro_diff = abs(synchro_ts - synchro_vid)
    frame_idx = round(
        (epoch_queried - epoch_ini) * total_frames / (epoch_end - epoch_ini)
        - frame_synchro_diff
    )
    return frame_idx


def get_video_frame(frame_number, video_path):
    # read a single frame
    try:
        # Open the video file
        video = cv2.VideoCapture(video_path)

        # Set the video's current frame to the specified frame number
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        ret, frame = video.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Add frame number overlay on image
        font = cv2.FONT_HERSHEY_SIMPLEX
        txt = str(frame_number)
        fontScale = 3
        white = (255, 255, 255)
        fontthickness = 5
        cv2.putText(
            img=img,
            text=txt,
            org=(10, 100),
            fontFace=font,
            fontScale=fontScale,
            color=white,
            thickness=fontthickness,
        )

        # Release the video file and close all windows
        video.release()
        cv2.destroyAllWindows()
        return img
    except StopIteration:
        print("Reached the end of the video file")
        return np.asarray(Image.new("RGB", (3840, 2160), (0, 0, 0)))


@pn.cache
def get_frame_plot(epoch_queried, epoch_ini, total_frames, epoch_end, gt_segm_dict):
    frame_idx = conv_epoch2frame(
        epoch_queried=epoch_queried,
        epoch_ini=epoch_ini,
        total_frames=total_frames,
        epoch_end=epoch_end,
        synchro_vid=gt_segm_dict.get("synchro_vid"),
        synchro_ts=gt_segm_dict.get("synchro_ts"),
    )
    # idx = epoch_queried - epoch_ini
    img = get_video_frame(
        frame_number=frame_idx,
        video_path=video_path,
    )
    frame_plot = pn.pane.Image(Image.fromarray(img), width=480, align="center")
    return frame_plot


def count_video_frames(video_path):
    """
    Custom function to manually count
    total number of frames
    """
    # Capturing a video
    video = cv2.VideoCapture(video_path)

    # total frames set to 0
    total_frames = 0

    print("Counting video frames...")
    pbar = tqdm()
    # Using while statement
    while True:
        # Counting frames using loop
        ret, frame = video.read()
        if not ret:
            break
        total_frames += 1
        pbar.update(1)
    pbar.close()
    video.release()
    print(f"Total frames in video: {total_frames}")
    return total_frames


def get_video_fps(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f"Frames per second in video: {fps}")
    video.release()
    return fps


gt_segm_dict, video_file, hdf5_file = get_gtdict_filenames(
    ground_truth_segm_file=GROUND_TRUTH_SEGM_FILE, filenum=FILENUM
)
hdf5_path = DATA_PATH_ROOT / hdf5_file
video_path = DATA_PATH_ROOT / video_file
joint_data, tf_data, wrench_data, gripper_data = read_h5_data(fname=hdf5_path)

gt_file_keys = ["Raw", "Segmented"]
choice_dropdown = pn.widgets.Select(
    name="Segmentation", value=gt_file_keys[0], options=gt_file_keys
)

print(f"TS length: {tf_data[0].shape[0]}")
total_frames = count_video_frames(video_path)
video_fps = get_video_fps(video_path)
traj = ts2df(tf_data=tf_data, gripper_data=gripper_data)
print(traj)
epoch_ini = int(traj.timestamp.iloc[0].timestamp()) + 1
epoch_end = int(traj.timestamp.iloc[-1].timestamp())
slider_widget = pn.widgets.IntSlider(
    name="Time step",
    value=int((epoch_end - epoch_ini) / 2 + epoch_ini),
    start=epoch_ini,
    end=epoch_end - 1,
)


# Widgets & web app logic
line_plt = pn.bind(
    get_line_plot,
    traj=traj,
    epoch_queried=slider_widget,
    show_segments=choice_dropdown,
    gt_segm_dict=gt_segm_dict,
)
img_plt = pn.bind(
    get_frame_plot,
    epoch_queried=slider_widget,
    epoch_ini=epoch_ini,
    total_frames=total_frames,
    epoch_end=epoch_end,
    gt_segm_dict=gt_segm_dict,
)
centered_img = pn.Row(pn.layout.HSpacer(), img_plt, pn.layout.HSpacer())
pn.template.MaterialTemplate(
    site="Segmentation",
    title="Video vs. timeseries",
    sidebar=[choice_dropdown],
    main=[centered_img, slider_widget, line_plt],
).servable()  # The ; is needed in the notebook to not display the template. Its not needed in a script
