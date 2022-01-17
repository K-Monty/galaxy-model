import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
import matplotlib.pyplot as plt # noqa

from galaxy_model.spiral_arms.sct_cen import SctCenArm # noqa
from galaxy_model.spiral_arms.norma_outer import NormaOuterArm # noqa
from galaxy_model.spiral_arms.perseus import PerseusArm # noqa
from galaxy_model.spiral_arms.local import LocalArm # noqa
from galaxy_model.spiral_arms.three_kpc import ThreeKpcArm # noqa
from galaxy_model.spiral_arms.sgr_car import SgrCarArm # noqa


def test_plot_local_arm():
    poly = LocalArm()
    my_polypatch = poly.polypatch
    print(type(my_polypatch))
    print(type(poly.x_spine))
    ax.add_patch(my_polypatch)
    plt.plot(poly.x_spine[1:], poly.y_spine[1:], color='cyan')


def test_plot_3kpc_arm():
    poly = ThreeKpcArm()
    my_polypatch_near = poly.polypatch_near
    my_polypatch_far = poly.polypatch_far
    ax.add_patch(my_polypatch_near)
    ax.add_patch(my_polypatch_far)
    plt.plot(poly.x_spine[0][1:], poly.y_spine[0][1:], color='yellow')
    plt.plot(poly.x_spine[1][1:], poly.y_spine[1][1:], color='yellow')


def test_plot_sgr_car_arm():
    poly = SgrCarArm()
    my_polypatch = poly.polypatch
    ax.add_patch(my_polypatch)
    plt.plot(poly.x_spine[1:], poly.y_spine[1:], color='purple')


def test_plot_sct_cen_arm():
    poly = SctCenArm()
    my_polypatch = poly.polypatch
    ax.add_patch(my_polypatch)
    plt.plot(poly.x_spine[1:], poly.y_spine[1:], color='blue')


def test_plot_perseus_arm():
    poly = PerseusArm()
    my_polypatch = poly.polypatch
    ax.add_patch(my_polypatch)
    plt.plot(poly.x_spine[1:], poly.y_spine[1:], color='black')


def test_plot_norma_outer_arm():
    poly = NormaOuterArm()
    my_polypatch = poly.polypatch
    ax.add_patch(my_polypatch)
    plt.plot(poly.x_spine[1:], poly.y_spine[1:], color='red')


def test_plot_all():
    test_plot_local_arm()
    test_plot_3kpc_arm()
    test_plot_sgr_car_arm()
    test_plot_sct_cen_arm()
    test_plot_perseus_arm()
    test_plot_norma_outer_arm()


if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8.88, 8.88))
    # call any test function here
    test_func = test_plot_all()
    plt.xlim(-16, 16)
    plt.ylim(-16, 16)
    plt.show()
