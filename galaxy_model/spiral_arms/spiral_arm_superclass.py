"""
This module contains the superclass for all existing spiral arm classes.
All spiral arms should inherit from this superclass.
"""

import numpy as np
from shapely.geometry.polygon import Polygon  # TODO: use pygeos instead
from descartes import PolygonPatch
from scipy.signal import savgol_filter

from .spiral_property import get_galactocentric_radius_at_B, polar_to_cartesian


class SpiralArm:
    """
    Spiral arm model created with the information in Reid et al (2019), using a
    basic formula:

    ln(R/R_kink) = -(B-B_kink)*tan(psi)

    Paremeters
    ----------
    spiral_params: dict
        Parameters defining the spiral arm (e.g. angles where kinks and
        tangencies are, psi before and after kinks/tangencies).
        See spiral_parameters.py for some examples.
    polypatch_color: str
        Matplotlib color for the spiral arm created
    tuning_window: int
        Length of the filter(smoothing in this case) window used to smooth the
        spiral arm. See scipy.signal.salgov_filter for more info.

    Attributes
    ----------
    self._color: str
        store polypatch_color parameter
    self.tuning_window: int
        store tuning_window parameter
    self.x_spine, self.y_spine: list, list
        calculated spinal coordinates of the spiral arm
    self.polypatch: matplotlib.patches.PathPatch
        patch object to be plotted, along with self.x_spine and self.y_spine,
        onto matplotlib
        by: ax.add_patch(self.polypatch)

    Returns
    -------
    Coordinates of spines and (ambiguous) borders for spiral arms are
    calculated, and the resulting spinal coordinates and polypatch are stored
    in self.x_spine, self.y_spine and self.polypatch.

    Note: for ThreeKpcArm in three_kpc.py, self.polypatch are split into
         _near and _far. Its self.x_spine and self.y_spine are also
         lists-within-list, of len(2). I.e. while plotting, need to specify

         plt.plot(self.x_spine[0], self.y_spine[0])  # near-side
         plt.plot(self.x_spine[1], self.y_spine[1])  # far-side

         separately.
    """

    def __init__(self, spiral_params, polypatch_color, tuning_window):
        self.params = spiral_params
        self._color = polypatch_color
        self.tuning_window = tuning_window
        self._spine_r_kpc, self.x_spine, self.y_spine, self._B_spine, \
            self._width_kpc = \
            self.spine_radii_coords_b_range_and_width_with_smoothing()
        self._poly_coords = self._poly_coords()
        self._polygon = Polygon(self._poly_coords)
        self.polypatch = PolygonPatch(self._polygon,
                                      color=self._color,
                                      alpha=0.2)

    def _spine_radius_at_B_and_psi(self, B, B_kink, psi, R_kink):
        return get_galactocentric_radius_at_B(
            B, B_kink, psi, R_kink)

    def _radii_factory(self, B):
        raise NotImplementedError()

    def _width_factory(self, B, r):
        raise NotImplementedError()

    def spine_radii_coords_b_range_and_width_with_smoothing(self):
        r_spine = []
        x_spine = []
        y_spine = []
        width_kpc = []

        num_blist = (self.params['B-end']
                     - self.params['B-begin']) + 1
        B_list = np.linspace(
                            self.params['B-begin'],
                            self.params['B-end'],
                            num_blist)
        for B in B_list:
            r = self._radii_factory(B)
            w = self._width_factory(B, r)
            r_spine.append(r)
            width_kpc.append(w)
        r_spine_moving_average = savgol_filter(r_spine, self.tuning_window, 1)
        width_kpc_moving_average = savgol_filter(width_kpc,
                                                 self.tuning_window, 1)
        for B, r in zip(B_list, r_spine_moving_average):
            cartesian_coords = polar_to_cartesian(r, B)
            x_spine.append(cartesian_coords[0])
            y_spine.append(cartesian_coords[1])
        return (r_spine_moving_average,
                x_spine, y_spine, B_list, width_kpc_moving_average)

    def _spine_normal_unit_vectors(self, x_spine, y_spine, B_list):
        dx_list = np.diff(x_spine)
        dy_list = np.diff(y_spine)
        normal_inner_list = []
        normal_outer_list = []
        theta = np.radians(90)
        c, s = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array(((c, -s), (s, c)))
        for dx, dy in zip(dx_list, dy_list):
            normal_inner_vector = np.matmul(rotation_matrix, np.array(
                                                                    [dx, dy]))
            normal_inner_unit_vector = normal_inner_vector/np.linalg.norm(
                                                        normal_inner_vector)
            normal_outer_unit_vector = -normal_inner_unit_vector
            normal_inner_list.append(normal_inner_unit_vector)
            normal_outer_list.append(normal_outer_unit_vector)
        return normal_inner_list, normal_outer_list

    def _border_coords(self, x_spine, y_spine, b_list, width_kpc):
        x_border_inner = []
        y_border_inner = []
        x_border_outer = []
        y_border_outer = []
        normal_inner, normal_outer = self._spine_normal_unit_vectors(
            x_spine, y_spine, b_list)
        for x, y, w, ni, no in zip(
            x_spine[1:], y_spine[1:], width_kpc[1:], normal_inner, normal_outer
                ):
            vector_length = w
            x_outer = x + (no[0] * vector_length)
            y_outer = y + (no[1] * vector_length)
            x_inner = x + (ni[0] * vector_length)
            y_inner = y + (ni[1] * vector_length)
            x_border_inner.append(x_inner)
            y_border_inner.append(y_inner)
            x_border_outer.append(x_outer)
            y_border_outer.append(y_outer)
        return x_border_inner, y_border_inner, x_border_outer, y_border_outer

    def _poly_coords(self):
        x_border_inner, y_border_inner, x_border_outer, y_border_outer = \
            self._border_coords(self.x_spine,
                                self.y_spine,
                                self._B_spine,
                                self._width_kpc)
        x_poly_edge_coords = x_border_inner + x_border_outer[::-1]
        y_poly_edge_coords = y_border_inner + y_border_outer[::-1]
        poly_edge_coords = [xy for xy in zip(x_poly_edge_coords,
                            y_poly_edge_coords)]
        return poly_edge_coords
