"""
This module use SpiralArm superclass to create Sct-Cen arm.
"""

from .spiral_parameters import Sct_Cen
from . import spiral_property as spiral_eq
from .spiral_arm_superclass import SpiralArm


class SctCenArm(SpiralArm):
    def __init__(self):
        super(SctCenArm, self).__init__(Sct_Cen, 'blue', 51)

    def __repr__(self):
        return "SctCen"

    def _radii_factory(self, B):
        if B <= self.params['B-kink']:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-before'],
                self.params['R-kink'])
        elif B > self.params['B-kink'] and B < self.params['l-tangency']:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-between'],
                self.params['R-kink'])
        elif B >= self.params['l-tangency'] and B < 292:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-after'],
                self.params['R-kink'])
        else:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-after']+0.75,
                self.params['R-kink'])

    def _width_factory(self, B, r):
        return spiral_eq.CylinderSize.width_kpc(
            self.params['w-kink'], r, self.params['R-kink']) + 0.2
