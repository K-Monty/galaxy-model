"""
This module use SpiralArm superclass, with some modifications,
 to create 3-kpc arm.
"""

from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch

from .spiral_parameters import Three_Kpc
from . import spiral_property as spiral_eq
from .spiral_arm_superclass import SpiralArm


class ThreeKpcArm(SpiralArm):
    def __init__(self):
        self.params = Three_Kpc
        self._color = 'yellow'
        self.tuning_window = 3
        self._spine_r_kpc, self.x_spine, self.y_spine, self._B_spine, \
            self._width_kpc = \
            self.spine_radii_coords_b_range_and_width_with_smoothing()
        self._poly_coords_inner, self._poly_coords_outer = self._poly_coords()
        self._polygon_near = Polygon(self._poly_coords_inner)
        self._polygon_far = Polygon(self._poly_coords_outer)
        self.polypatch_near = PolygonPatch(self._polygon_near,
                                           color=self._color,
                                           alpha=0.2)
        self.polypatch_far = PolygonPatch(self._polygon_far,
                                          color=self._color,
                                          alpha=0.2)

    def __repr__(self):
        return "ThreeKpc"

    def _radii_factory(self, B):
        return self._spine_radius_at_B_and_psi(
            B, self.params['B-kink'],
            self.params['psi'],
            self.params['R-kink'])

    def _width_factory(self, B, r):
        return spiral_eq.CylinderSize.width_kpc(
            self.params['w-kink'], r, self.params['R-kink']) + 0.1

    def spine_radii_coords_b_range_and_width_with_smoothing(self):
        r_spine_near = []
        x_spine_near = []
        y_spine_near = []
        width_kpc_near = []
        B_list_near = [x for x in range(self.params['B-begin-near'],
                                        self.params['B-end-near'])]
        r_spine_far = []
        x_spine_far = []
        y_spine_far = []
        width_kpc_far = []
        B_list_far = [x for x in range(self.params['B-begin-far'],
                                       self.params['B-end-far'])]

        for B_near in B_list_near:
            r_near = self._radii_factory(B_near)
            w_near = self._width_factory(B_near, r_near)
            r_spine_near.append(r_near)
            width_kpc_near.append(w_near)

        for B_far in B_list_far:
            r_far = self._radii_factory(B_far)
            w_far = self._width_factory(B_far, r_far)
            r_spine_far.append(r_far)
            width_kpc_far.append(w_far)

        for B_near, r_near in zip(B_list_near, r_spine_near):
            cartesian_coords = spiral_eq.polar_to_cartesian(r_near, B_near)
            x_spine_near.append(cartesian_coords[0])
            y_spine_near.append(cartesian_coords[1])

        for B_far, r_far in zip(B_list_far, r_spine_far):
            cartesian_coords = spiral_eq.polar_to_cartesian(r_far, B_far)
            x_spine_far.append(cartesian_coords[0])
            y_spine_far.append(cartesian_coords[1])

        r_spine = [r_spine_near, r_spine_far]
        x_spine = [x_spine_near, x_spine_far]
        y_spine = [y_spine_near, y_spine_far]
        B_list = [B_list_near, B_list_far]
        width_kpc = [width_kpc_near, width_kpc_far]
        return (r_spine, x_spine, y_spine, B_list, width_kpc)

    def _poly_coords(self):
        x_border_inner_near, y_border_inner_near, x_border_outer_near, \
            y_border_outer_near = \
            self._border_coords(self.x_spine[0],
                                self.y_spine[0],
                                self._B_spine[0],
                                self._width_kpc[0])
        x_border_inner_far, y_border_inner_far, x_border_outer_far, \
            y_border_outer_far = \
            self._border_coords(self.x_spine[1],
                                self.y_spine[1],
                                self._B_spine[1],
                                self._width_kpc[1])

        x_poly_edge_coords_near = x_border_inner_near \
            + x_border_outer_near[::-1]
        y_poly_edge_coords_near = y_border_inner_near \
            + y_border_outer_near[::-1]
        poly_edge_coords_near = [xy for xy in zip(x_poly_edge_coords_near,
                                 y_poly_edge_coords_near)]

        x_poly_edge_coords_far = x_border_inner_far + x_border_outer_far[::-1]
        y_poly_edge_coords_far = y_border_inner_far + y_border_outer_far[::-1]
        poly_edge_coords_far = [xy for xy in zip(x_poly_edge_coords_far,
                                y_poly_edge_coords_far)]

        return poly_edge_coords_near, poly_edge_coords_far
