"""
This module use SpiralArm superclass, with some modifications,
 to create Norma-Outer arm.
"""

import numpy as np
from scipy.signal import savgol_filter

from .spiral_parameters import Norma, Outer
from . import spiral_property as spiral_eq
from .spiral_arm_superclass import SpiralArm


class NormaOuterArm(SpiralArm):
    def __init__(self):
        self.params_norma = Norma
        self.params_outer = Outer
        super(NormaOuterArm, self).__init__(Norma, 'red', 301)

    def __repr__(self):
        return "NormaOuter"

    def _radii_factory(self, B):
        if B <= self.params_norma['B-kink']:
            return self._spine_radius_at_B_and_psi(
                B, self.params_norma['B-kink'],
                self.params_norma['psi-before'],
                self.params_norma['R-kink'])
        elif (B > self.params_norma['B-kink']
              and B < self.params_norma['l-tangency']):
            return self._spine_radius_at_B_and_psi(
                B, self.params_norma['B-kink'],
                self.params_norma['psi-between'],
                self.params_norma['R-kink'])
        elif B > self.params_norma['l-tangency'] and B <= 300:
            return self._spine_radius_at_B_and_psi(
                B, self.params_norma['B-kink'],
                self.params_norma['psi-after'],
                self.params_norma['R-kink'])
        elif B > 300 and B < self.params_outer['B-kink']:
            return self._spine_radius_at_B_and_psi(
                B, self.params_outer['B-kink'],
                self.params_outer['psi-before'],
                self.params_outer['R-kink'])
        else:
            return self._spine_radius_at_B_and_psi(
                B, self.params_outer['B-kink'],
                self.params_outer['psi-after'],
                self.params_outer['R-kink'])

    def _width_factory(self, B, r):
        if B < 350:
            return spiral_eq.CylinderSize.width_kpc(
                self.params_norma['w-kink'], r, self.params_norma['R-kink']) \
                + 0.2
        else:
            return spiral_eq.CylinderSize.width_kpc(
                self.params_outer['w-kink'], r, self.params_outer['R-kink']) \
                + 0.2

    def _fine_tuning(self, B, centre, param_cent, param_influence):
        distance = abs(centre-B)
        reduced_radii = param_cent-distance/param_influence
        if reduced_radii > 0:
            return reduced_radii
        else:
            return 0

    # overwrhte this function to reduce the smoothing around tangent
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
            final_r = r - self._fine_tuning(
                                B, self.params_norma['l-tangency'], 0.7, 200)
            if B <= self.params_norma['B-kink']:
                final_r -= self._fine_tuning(
                                B, self.params['B-begin'], 0.8, 50)

            cartesian_coords = spiral_eq.polar_to_cartesian(final_r, B)
            x_spine.append(cartesian_coords[0])
            y_spine.append(cartesian_coords[1])
        return (r_spine_moving_average,
                x_spine, y_spine, B_list, width_kpc_moving_average)
