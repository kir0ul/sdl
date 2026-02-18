import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

colors = list(mcolors.TABLEAU_COLORS)
import h5py
from .sim_metrics import *
import math

# Implementation for Library of Motion Primitives
# takes in primitives and organizes them into classes
# assumes demonstrations are already preprocessed (smoothed & resampled)


# get smallest (a, b) such that a * golden ratio = b (approximately) and a*b > n
def golden_ratio_factors(n):
    a = math.ceil((n / 1.618) ** 0.5)
    b = math.ceil(n / a)
    return a, b


class MP_Library(object):
    def __init__(self, metric=COS_metric, threshold=1.0, debug=False):
        self.DEBUG = debug
        self.library = {}
        self.translation_dict = {}
        self.threshold = threshold
        self.metric = metric

    def add_primitive(self, demo, name=None):
        similarities = []
        out = None
        for class_key, demo_list in self.library.items():
            similarities.append(
                min([self.metric(demo, old_demo) for old_demo in demo_list])
            )
            if self.DEBUG:
                print(f"Class: '{class_key}' - Similarity: {similarities[-1]:.3f}")
        if len(similarities) > 0 and min(similarities) < self.threshold:
            class_id = list(self.library.keys())[np.argmin(similarities)]
            self.library[class_id].append(demo)
            out = class_id
            if self.DEBUG:
                print(f"Class matched: '{class_id}'")
        else:
            if name is None:
                name = "Skill_" + str(self.get_num_demos())
            self.library[name] = [demo]
            out = name
            if self.DEBUG:
                print(f"Class not matched, new class: '{name}'")
        return out

    def get_num_demos(self):
        sum = 0
        for class_key, demo_list in self.library.items():
            sum += len(demo_list)
        return sum

    def display(self):
        print("------------------")
        print("--- MP Library ---")
        print("------------------")
        for class_key, demo_list in self.library.items():
            print(f"+ {class_key}: {len(demo_list)}")
        print("------------------")
        return

    def plot(self):
        if self.get_num_demos() < 1:
            print("Nothing to plot!")
            return
        n_pts, n_dims = np.shape(list(self.library.values())[0][0])
        if n_dims == 2:
            fig = plt.figure()
            idx = 0
            for class_key, demo_list in self.library.items():
                demo = demo_list[0]
                plt.plot(
                    demo[:, 0],
                    demo[:, 1],
                    color=colors[idx % len(colors)],
                    lw=5,
                    alpha=0.8,
                    label=class_key,
                )
                if len(demo_list) > 1:
                    for demo in demo_list[1:]:
                        plt.plot(
                            demo[:, 0],
                            demo[:, 1],
                            color=colors[idx % len(colors)],
                            lw=5,
                            alpha=0.8,
                        )
                idx += 1
            plt.legend()
            plt.show()
        else:
            print("Plotting not implemented for more than 2 dimensions!")
        return

    def plot_separate(self):
        if self.get_num_demos() < 1:
            print("Nothing to plot!")
            return

        with plt.style.context("ggplot"):
            n_pts, n_dims = np.shape(list(self.library.values())[0][0])
            n_classes = len(self.library)
            fig, axs = plt.subplots(
                nrows=n_classes, ncols=n_dims, figsize=(3 * n_dims, n_classes)
            )
            if len(axs.shape) < 2:
                axs = axs[np.newaxis, :]
            for skill_i, (class_key, demo_list) in enumerate(self.library.items()):
                for demo_i, demo in enumerate(demo_list):
                    for dim_i in range(n_dims):
                        axs[skill_i, dim_i].plot(
                            demo[:, dim_i],
                            color=colors[demo_i % len(colors)],
                            # alpha=0.8,
                            # label=class_key,
                        )
                        # axs[row, col].legend()
                        if dim_i == 0:
                            axs[skill_i, dim_i].set_ylabel(class_key, fontsize=12)
                        if skill_i == 0:
                            axs[skill_i, dim_i].set_title(
                                f"Dimension {dim_i}", fontsize=12
                            )
            fig.tight_layout()
            plt.show()
            return

    def save_h5(self, filename="library.h5"):
        hf = h5py.File(filename, "w")
        for class_key, demo_list in self.library.items():
            for i in range(len(demo_list)):
                hf.create_dataset("/" + class_key + "/demo" + str(i), data=demo_list[i])
        hf.close()
        return

    def load_h5(self, filename):
        hf = h5py.File(filename, "r")
        if self.DEBUG:
            print(f"Keys in `{hf}` file:")
            print(list(hf.keys()))
        for class_key in list(hf.keys()):
            key_group = hf.get(class_key)
            if self.DEBUG:
                print(f"Keys in `{key_group}` group:")
                print(list(key_group.keys()))
            demo_names = list(key_group.keys())
            if class_key not in self.library:
                self.library[class_key] = []
            for name in demo_names:
                demo = np.array(key_group.get(name))
                self.library[class_key].append(demo)
        hf.close()
        return


def gen_traj(exponent):
    x = np.linspace(0, 1, 100)
    y = x**exponent
    return x, y


def main():
    x1, y1 = gen_traj(0.5)
    demo1 = np.hstack((np.reshape(x1, (len(x1), 1)), np.reshape(y1, (len(y1), 1))))
    x1, y1 = gen_traj(0.6)
    demo2 = np.hstack((np.reshape(x1, (len(x1), 1)), np.reshape(y1, (len(y1), 1))))
    x1, y1 = gen_traj(1.0)
    demo3 = np.hstack((np.reshape(x1, (len(x1), 1)), np.reshape(y1, (len(y1), 1))))
    x1, y1 = gen_traj(1.5)
    demo4 = np.hstack((np.reshape(x1, (len(x1), 1)), np.reshape(y1, (len(y1), 1))))
    x1, y1 = gen_traj(1.6)
    demo5 = np.hstack((np.reshape(x1, (len(x1), 1)), np.reshape(y1, (len(y1), 1))))

    library = MP_Library(metric=COS_metric, threshold=2.0, debug=True)
    library.add_primitive(demo1)
    library.add_primitive(demo2)
    library.add_primitive(demo3)
    library.add_primitive(demo4)
    library.add_primitive(demo5)
    library.display()
    library.plot()
    library.plot_separate()
    library.save_h5("test.h5")

    print("\n~~~ New library ~~~\n")

    new_library = MP_Library(metric=COS_metric, threshold=2.0, debug=True)
    new_library.load_h5("test.h5")
    new_library.display()
    new_library.plot()
    new_library.plot_separate()


if __name__ == "__main__":
    main()
