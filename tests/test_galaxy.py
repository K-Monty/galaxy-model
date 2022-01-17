import os
import sys
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))

from galaxy_model.galaxy import Galaxy # noqa

gal = Galaxy()


def test_add_and_remove_coords():
    gal.add_coord([0.5, 0.5], [10, 10])
    assert gal.src_x_coords == [0.5, 0.5]
    assert gal.src_y_coords == [10, 10]
    gal.remove_coord([0.5], [10])
    assert gal.src_x_coords == [0.5]
    assert gal.src_y_coords == [10]
    gal.remove_coord([0.5], [10])
    assert gal.src_x_coords == []
    assert gal.src_y_coords == []
    print("Test add_and_remove_coord passed!")


def test_plot_galaxy_basic():
    gal.add_coord([0.5], [10])
    gal.plot()
    plt.show()


def test_on_spur():
    assert gal._on_spur(0.5, 10) is False
    assert gal._on_spur(1.54, 4.35) is True
    print("Test on_spur passed!")


def test_on_spiral_arm():
    assert gal._on_spiral_arm(0.5, 10)[0] is True
    assert gal._on_spiral_arm(1.54, 4.35)[0] is True
    print("Test on_spiral_arm passed!")


def test_on_anything():
    assert gal.isOnSpiralArmOrSpur([6.5, 0.5, -2.27, 1.54],
                                   [1, 10, 4.62, 4.35]) == [0, 1, 2, 3]
    print(gal.isOnSpiralArmOrSpur([6.5, 0.5, -2.27, 1.54],
                                  [1, 10, 4.62, 4.35], verbose=True))
    print("Test on_anything passed!")


if __name__ == "__main__":
    test_add_and_remove_coords()
    test_plot_galaxy_basic()
    test_on_spur()
    test_on_spiral_arm()
    test_on_anything()
