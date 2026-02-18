# SDL

## Get the data
The data is expected to be in the `data` folder at the root of the project.
1. The data for the task of setting the table can be downloaded from: https://studentuml-my.sharepoint.com/:f:/r/personal/andrea_pierre_student_uml_edu/Documents/table-task?csf=1&web=1&e=nAn7l5. You need to be granted access first. We use the 4 BAG files from September 8 (except the `rosbag2_[...]_okayish.bag`).
2. The data for the task of setting the table with pouring and drawer opening can be downloaded from: https://studentuml-my.sharepoint.com/:f:/r/personal/andrea_pierre_student_uml_edu/Documents/IROS2026?csf=1&web=1&e=xjC2mH. You need to be granted access first.

## Ground truth segmentation
To build the ground truth segmentation file, run the following script: `panel serve ground_truth_segm_synchro_video_ts.py`, and open the URL (e.g. http://localhost:5006/ground_truth_segm_synchro_video_ts) in your browser.

## Code requirements

The following code is required to run the notebook:
``` sh
git clone git@github.com:brenhertel/ElasticMaps.git
```

