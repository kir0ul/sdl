import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import UnivariateSpline

from LfD_Library.MP_Library import MP_Library
from ElasticMaps.elmap_EM import ElmapEM
from LfD_Library.utils import *
from LfD_Library.sim_metrics import *

fname = "recorded_demo 2026-01-29 16_38_27.h5"
idxs = [3601, 5598, 6596, 8595, 10095, 11595, 12095, 14093, 15590]


# get demos from h5 file
def get_segmented_demo(filename):
    pos_data = read_recorded_demo(filename)
    raw_segments = []
    for i in range(len(idxs) - 1):
        seg_demo = pos_data[idxs[i] : idxs[i + 1], :]
        print(np.shape(seg_demo))
        raw_segments.append(seg_demo)
    return raw_segments


# resample & smooth a trajectory, use a univariate spline for each dimension
def resample(traj, n=200):
    n_pts, n_dims = np.shape(traj)
    new_traj = np.zeros((n, n_dims + 1))
    t = np.linspace(0, 1, n_pts)
    tt = np.linspace(0, 1, n)
    new_traj[:, 0] = tt
    for i in range(n_dims):
        sp = UnivariateSpline(t, traj[:, i].flatten())
        sp.set_smoothing_factor(1e-3)
        smooth_resampled = sp(tt)
        new_traj[:, i + 1] = smooth_resampled
    return new_traj


# resample each segment using above function
def resample_segments(raw_segments, n=200):
    return [resample(traj, n) for traj in raw_segments]


# use LTE to meet constraints
def LTE_transform(traj, constraints, indices):

    fixedWeight = 1e9

    (n_pts, n_dims) = np.shape(traj)
    L = (
        2.0 * np.diag(np.ones((n_pts,)))
        - np.diag(np.ones((n_pts - 1,)), 1)
        - np.diag(np.ones((n_pts - 1,)), -1)
    )
    L[0, 1] = -2.0
    L[-1, -2] = -2.0
    L = L / 2.0

    delta = np.matmul(L, traj)

    to_append_L = np.zeros((len(indices), n_pts))
    for i in range(len(indices)):
        to_append_L[[i], indices[i]] = fixedWeight
        to_append_delta = fixedWeight * constraints[i]
        delta = np.vstack((delta, to_append_delta))
    L = np.vstack((L, to_append_L))
    new_traj, _, _, _ = np.linalg.lstsq(L, delta, rcond=-1)
    # new_traj, _, _, _ = np.linalg.solve(L, delta)
    return new_traj


# transform all segments (I tried using LTE to normalize before adding to library, didn't work great so now just set all starts to 0)
def transform_segments(segments):
    # transformed_segments = []
    # for segment in segments:
    #    n_pts, n_dims = np.shape(segment)
    #    start = np.zeros((1, n_dims))
    #    end = np.zeros((1, n_dims))
    #    for i in range(n_dims):
    #        if segment[0, i] < segment[-1, i]:
    #            end[0, i] = 1
    #        elif segment[0, i] > segment[-1, i]:
    #            start[0, i] = 1
    #    constraints = [start, end]
    #    indices = [0, n_pts-1]
    #    transform_traj = LTE_transform(segment, constraints, indices)
    #    transformed_segments.append(transform_traj)
    #    print(np.shape(transform_traj))
    # return transformed_segments

    transformed_segments = []
    for segment in segments:
        new_segment = segment - segment[0, :]
        transformed_segments.append(new_segment)
    return transformed_segments


def main():
    # get the raw data segments
    raw_segments = get_segmented_demo(fname)

    # resample & smooth each segment
    resampled_segments = resample_segments(raw_segments)

    # transform each segment (set all starts to 0)
    transformed_segments = transform_segments(resampled_segments)

    # add all primitives to library
    classes = []
    library = MP_Library(metric=SSE_metric, threshold=10.0, debug=True)
    for i in range(len(transformed_segments)):
        if i == 5:  # this primitive I'm making its own class for safety reasons
            class_name = library.add_primitive(
                transformed_segments[i], name="segment" + str(i + 1), force_class=True
            )
        else:
            class_name = library.add_primitive(
                transformed_segments[i], name="segment" + str(i + 1)
            )
        classes.append(class_name)
    library.display()
    library.plot()
    library.plot_separate()
    print(classes)

    # learn each class with elastic maps

    n_pts_elmap = 100

    learned_trajs = {}
    for class_key in library.library:
        demo_list = library.library[class_key]
        elmap = ElmapEM(
            demo_list,
            n=n_pts_elmap,
            weighting="uniform",
            downsampling="distance",
            stretch=0.01,
            bend=10.0,
        )  # stretching and bending may require some tuning with trial and error
        # set start and end to mean start and end of all primitives in class
        start = np.mean(np.array([demo[0, :] for demo in demo_list]), axis=0)
        end = np.mean(np.array([demo[-1, :] for demo in demo_list]), axis=0)
        new_traj = elmap.optimize_map(
            [start.flatten(), end.flatten()], [0, n_pts_elmap - 1]
        )
        new_traj = elmap.optimize_map()
        learned_trajs[class_key] = new_traj

        ## plotting
        # print(class_key)
        # fig, axs = plt.subplots(3, 1)
        # for d in range(3):
        #    for i in range(len(demo_list)):
        #        #t = np.linspace(0, 1, len(demo_list[i]))
        #        axs[d].plot(demo_list[i][:, 0], demo_list[i][:, d+1], lw=5, alpha=0.8)
        #    #tt = np.linspace(0, 1, len(new_traj))
        #    axs[d].plot(new_traj[:, 0], new_traj[:, d+1], 'k', lw=4, alpha=0.8)
        # plt.show()

    # adjust learned trajectories to constraints using LTE
    generated_trajs = []
    for i in range(len(classes)):
        start = raw_segments[i][0, :]
        end = raw_segments[i][-1, :]
        elmap_traj = learned_trajs[classes[i]][:, 1:]
        gen_traj = LTE_transform(elmap_traj, [start, end], [0, n_pts_elmap - 1])
        time_elmap = learned_trajs[classes[i]][:, 0]
        generated_trajs.append(
            np.hstack((time_elmap.reshape((n_pts_elmap, 1)), gen_traj))
        )

        ## plotting
        # fig, axs = plt.subplots(3, 1)
        # for d in range(3):
        #    axs[d].plot(elmap_traj[:, d], lw=5, alpha=0.8)
        #    axs[d].plot(gen_traj[:, d], 'k', lw=4, alpha=0.8)
        # plt.show()

    # plot & save results

    fig, axs = plt.subplots(3, 1)
    for d in range(3):
        for i in range(len(raw_segments)):
            t = np.linspace(i, i + 1, len(raw_segments[i]))
            # tt = np.linspace(i, i+1, len(resampled_segments[i]))
            # ttt = np.linspace(i, i+1, len(generated_trajs[i]))
            axs[d].plot(t, raw_segments[i][:, d], lw=5, alpha=0.8)
            axs[d].plot(
                resampled_segments[i][:, 0] + i,
                resampled_segments[i][:, d + 1],
                "--",
                lw=5,
                alpha=0.8,
            )
            axs[d].plot(
                generated_trajs[i][:, 0] + i,
                generated_trajs[i][:, d + 1],
                "k",
                lw=4,
                alpha=0.8,
            )
        np.savetxt("pickplace_segment" + str(i) + ".txt", generated_trajs[i][:, 1:])
    plt.show()


if __name__ == "__main__":
    main()
