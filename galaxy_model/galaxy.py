"""
This module uses all the spiral arm models created in the spiral_arms folder,
along with Galactic Centre, spurs etc, to 'draw' the Galaxy model. It allows
user to add/remove cartesian coordinates to be plotted onto the model, and
check whether some arbitrary coordinates (independent on the coord plotting)
belong to any spiral arm(s) or spur.
"""

# Module level dunder names
__author__ = 'K-Monty'
__copyright__ = 'Copyright 2022, galaxy-model'
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'K-Monty'
__email__ = 'kmgoh1995@gmail.com'


from numbers import Number
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from shapely.geometry import Point
from shapely.ops import unary_union
from warnings import warn

from .spiral_arms.sct_cen import SctCenArm
from .spiral_arms.norma_outer import NormaOuterArm
from .spiral_arms.perseus import PerseusArm
from .spiral_arms.local import LocalArm
from .spiral_arms.three_kpc import ThreeKpcArm
from .spiral_arms.sgr_car import SgrCarArm


class Galaxy:
    """
    2D graphical representation of Galaxy, according to the description in
    Reid(2019).

    Attributes
    ----------
    self.gcbar: matplotlib.patches.Ellipse
        a simplified ellipse representing Galactic Bar
    self.spurs: list
        simplified circles representing a few spurious regions
        (roughly) estimated mainly by using ALMAGAL data
    self.src_x_coords, self.src_y_coords: list, list
        user-inserted lists of x- and y- coordinates
        see add_coords and remove_coords (methods)

    Methods
    -------
    add_coords(x_coord: list, y_coord: list)
        add coordinates into self.src_x_coords, self.src_y_coords
    remove_coords(x_coord: list, y_coord: list)
        remove coordinates from self.src_x_coords, self.src_y_coords
    plot(x_radius=16, y_radius=16, plotSrc=False)
        plot the Galaxy with indicated x- and y- radius (kpc),
        starting from the Galactic Centre
        if plotSrc is True, the coordinates in the lists
        self.src_x_coords, self.src_y_coords will also be plotted
    isOnSpiralArmOrSpur(x_coord: list, y_coord: list, verbose=False)
        check if the coordinates are on any spiral arm(s) or spur(s)
        if verbose is True, more details, e.g. on what spiral arms,
        will be printed out
    """

    def __init__(self):
        # the keys doesn't matter; this dict is only created for
        # looping of the spiral arm objects within some private functions
        self.spiral_arm_obj = {"3-kpc": ThreeKpcArm,
                               "Norma-Outer": NormaOuterArm,
                               "Sct-Cen": SctCenArm,
                               "Sgr-Car": SgrCarArm,
                               "Perseus": PerseusArm,
                               "Local": LocalArm}
        self.gcbar = Ellipse(xy=(0, 0), width=4.5*2, height=1.6*2, angle=60,
                             color='grey', zorder=1)
        self.spurs = [Point(-1.66, 4.85).buffer(1.15),
                      Point(1.1, 4.4).buffer(0.8),
                      Point(2.2, 3.75).buffer(0.5),
                      Point(2.8, 3.1).buffer(0.5)]
        self.src_x_coords = []
        self.src_y_coords = []

    def add_coord(self, x_coord: list, y_coord: list):
        """
        Parameters
        ----------
        x_coord, y_coord: lists of numericals
        """
        assert len(x_coord) == len(y_coord)
        assert len(x_coord) > 0
        self.src_x_coords += x_coord
        self.src_y_coords += y_coord

    def remove_coord(self, x_coord: list, y_coord: list):
        """
        Parameters
        ----------
        x_coord, y_coord: lists of numericals

        Note
        ----
        if two or more identical coordinates are found within the list,
        only the first one found will be removed
        """
        assert len(x_coord) == len(y_coord)
        assert len(x_coord) > 0
        to_delete_indices = []
        for x_todel, y_todel in zip(x_coord, y_coord):
            x_match_indices = [i for i, x in enumerate(self.src_x_coords)
                               if x == x_todel]
            y_match_indices = [i for i, y in enumerate(self.src_y_coords)
                               if y == y_todel]
            to_delete_index = list(set(x_match_indices) & set(y_match_indices))
            if len(to_delete_index) == 0:
                warn("Nothing found for the coordinate ({}, {}).".format(
                    x_todel, y_todel))
                continue
            # TODO: Instead of the first one found, maybe all?
            if len(to_delete_index) > 1:
                warn("More than 1 elements found for the coordinate ({}, {}). \
                     The first element found will be removed.".format(
                         x_todel, y_todel))
            to_delete_index = to_delete_index[0]
            to_delete_indices.append(to_delete_index)
        self.src_x_coords = [x for i, x in enumerate(self.src_x_coords)
                             if i not in to_delete_indices]
        self.src_y_coords = [y for i, y in enumerate(self.src_y_coords)
                             if i not in to_delete_indices]

    def _draw_spiral_arms(self, ax):
        for arm in list(self.spiral_arm_obj.values()):
            arm_obj = arm()
            # ThreeKpc arm has two (half-circle) parts
            if repr(arm_obj) == "ThreeKpc":
                plt.plot(arm_obj.x_spine[0], arm_obj.y_spine[0],
                         color=arm_obj._color, alpha=0.3, label=repr(arm_obj))
                ax.add_patch(arm_obj.polypatch_near)
                plt.plot(arm_obj.x_spine[1], arm_obj.y_spine[1],
                         color=arm_obj._color, alpha=0.3)
                ax.add_patch(arm_obj.polypatch_far)
                continue

            plt.plot(arm_obj.x_spine, arm_obj.y_spine, color=arm_obj._color,
                     alpha=0.3, label=repr(arm_obj))
            ax.add_patch(arm_obj.polypatch)

    def _draw_spurs(self, ax):
        for spur in self.spurs:
            x_spur, y_spur = spur.exterior.xy
            ax.fill(x_spur, y_spur, alpha=0.3, color='mediumblue')

    def _draw_gc(self, ax):
        ax.add_patch(self.gcbar)
        plt.scatter(0, 0, marker='x', color='black', zorder=100, s=200)

    def _label_galactic_quadrant(self, ax, x_radius=16, y_radius=16):
        plt.axhline(8.15, color='grey', alpha=0.5, ls='--')
        plt.axvline(0, color='grey', alpha=0.5, ls='--')
        ax.annotate("1st Quadrant", (x_radius*0.6, -y_radius+0.5), size=12)
        ax.annotate("4th Quadrant", (-x_radius+0.5, -y_radius+0.5), size=12)
        # an arbitrary number approximating the y-location of the sun
        # for this plotting scheme
        if y_radius > 8.2:
            ax.annotate("2nd Quadrant", (x_radius*0.6, y_radius-1), size=12)
            ax.annotate("3rd Quadrant", (-x_radius+0.5, y_radius-1), size=12)

    def _plot_src(self):
        assert len(self.src_x_coords) > 0
        plt.scatter(self.src_x_coords, self.src_y_coords, color='steelblue',
                    s=10, alpha=0.5, zorder=500)

    def _plot_basic(self, x_radius=16, y_radius=16):
        fig, ax = plt.subplots(figsize=(8, 8))
        self._draw_spiral_arms(ax)
        self._draw_gc(ax)
        self._draw_spurs(ax)
        self._label_galactic_quadrant(ax, x_radius, y_radius)
        plt.scatter(0, 8.15, marker='*', color='orange', s=200)
        plt.legend(bbox_to_anchor=(0.25, 0.93), loc=1)
        plt.xlim(-x_radius, x_radius)
        plt.ylim(-y_radius, y_radius)

    # TODO: use Pandas-Bokeh?
    def _plot_interactive(self, annotate=True):
        raise NotImplementedError

    # Interactive mode is not yet implemented!!!
    def plot(self, x_radius=16, y_radius=16, plotSrc=False,
             isInteractive=False):
        """
        Parameters
        ----------
        x_radius, y_radius: Number, Number
            x- and y-radius of the Galaxy (kpc), starting from
            the Galactic Centre (0, 0)
        """
        if isInteractive is False:
            self._plot_basic(x_radius, y_radius)
            if plotSrc is True:
                self._plot_src()
        else:
            try:
                self._plot_interactive()
            except NotImplementedError:
                print("Interactive mode is not yet implemented")

    def _on_spur(self, x: Number, y: Number):
        return any([s.contains(Point(x, y)) for s in self.spurs])

    def _on_spiral_arm(self, x: Number, y: Number):
        spiral_arms = []
        for arm in list(self.spiral_arm_obj.values()):
            if repr(arm()) == "ThreeKpc":
                poly_list = [arm()._polygon_near, arm()._polygon_far]
                poly = unary_union(poly_list)
            else:
                poly = arm()._polygon
            on_spiral_arm = poly.contains(Point(x, y))
            if on_spiral_arm:
                spiral_arms.append(repr(arm()))
        if len(spiral_arms) > 0:
            on_spiral_arm = True
        else:
            on_spiral_arm = False
        return on_spiral_arm, spiral_arms

    # TODO: add _on_gc_bar???
    def isOnSpiralArmOrSpur(self, x_coord: list, y_coord: list, verbose=False):
        """
        Check if the coordinates in the given list are located on a
        spiral arm or a spur.

        Parameters
        ----------
        x_coord, y_coord: lists of numericals
        verbose: bool
            Elaborated explanation about the location of a coordinate.
            E.g. what spiral arm(s)/spur does a coordinate fall on.

        Returns
        -------
        List encoding locations of coordinates:

        0 if the coordinate is on neither;

        1 if the coordinate is on a spiral_arm;

        2 if the coordinate is on a spur;

        3 if the coordinate is on multiple "objects";
            e.g. multiple spiral arms, both a spur and a spiral arm

        Note
        ----
        In verbose mode, spiral arm information has higher priority than spur.
        If a coordinate is on both spiral arm and spur, only the spiral
        arm information will be printed.
        """

        def verbose_statements(x, y, on_spiral_arm, on_spur, spiral_arms):
            if on_spiral_arm:
                print(
                      "{} is on {} spiral arm".format(
                       (x, y), spiral_arms))
            elif on_spur:
                print("{} is on a spur".format((x, y)))
            else:
                print("{} is on nothing".format((x, y)))

        def coord_loc_encoding(on_spiral_arm, on_spur, spiral_arms):
            if on_spur and on_spiral_arm or len(spiral_arms) > 1:
                return 3
            elif on_spur:
                return 2
            elif on_spiral_arm:
                return 1
            else:
                return 0

        #######################################################################

        on_anything = []

        for x, y in zip(x_coord, y_coord):
            on_spiral_arm, spiral_arms = self._on_spiral_arm(x, y)
            on_spur = self._on_spur(x, y)

            if verbose:
                verbose_statements(x, y, on_spiral_arm, on_spur, spiral_arms)

            on_anything.append(coord_loc_encoding(on_spiral_arm, on_spur,
                                                  spiral_arms))

        return on_anything
