import numpy as np
import h5py


def curvature_weighting(demos):
    n_demos = len(demos)
    ind_weights = []
    for i in range(n_demos):
        traj = demos[i]
        n_pts, n_dims = np.shape(traj)
        crv_weights = np.zeros((n_pts,))
        for j in range(1, n_pts - 1):
            crv_weights[j] = np.linalg.norm(traj[j - 1] - 2 * traj[j] + traj[j + 1])
        ind_weights.append(crv_weights)
    return np.hstack(ind_weights)


def jerk_weighting(demos):
    n_demos = len(demos)
    ind_weights = []
    for i in range(n_demos):
        traj = demos[i]
        n_pts, n_dims = np.shape(traj)
        jrk_weights = np.zeros((n_pts,))
        for j in range(1, n_pts - 2):
            jrk_weights[j] = np.linalg.norm(
                traj[j - 1] - 3 * traj[j] + 3 * traj[j + 1] - traj[j + 2]
            )
        ind_weights.append(jrk_weights)
    return np.hstack(ind_weights)


def read_data(fname):

    hf = h5py.File(fname, "r")

    print(list(hf.keys()))

    js = hf.get("joint_state_info")

    joint_time = np.array(js.get("joint_time"))

    joint_pos = np.array(js.get("joint_positions"))

    joint_vel = np.array(js.get("joint_velocities"))

    joint_eff = np.array(js.get("joint_effort"))

    joint_data = [joint_time, joint_pos, joint_vel, joint_eff]

    tf = hf.get("transform_info")

    tf_time = np.array(tf.get("transform_time"))

    tf_pos = np.array(tf.get("transform_positions"))

    tf_rot = np.array(tf.get("transform_orientations"))

    tf_data = [tf_time, tf_pos, tf_rot]

    wr = hf.get("wrench_info")

    wrench_time = np.array(wr.get("wrench_time"))

    wrench_frc = np.array(wr.get("wrench_force"))

    wrench_trq = np.array(wr.get("wrench_torque"))

    wrench_data = [wrench_time, wrench_frc, wrench_trq]

    gp = hf.get("gripper_info")

    gripper_time = np.array(gp.get("gripper_time"))

    gripper_pos = np.array(gp.get("gripper_position"))

    # gripper_time = []

    # gripper_pos = []

    gripper_data = [gripper_time, gripper_pos]

    hf.close()

    return np.hstack((tf_pos, gripper_pos / 100))
