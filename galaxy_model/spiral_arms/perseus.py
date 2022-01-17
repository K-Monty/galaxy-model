"""
This module use SpiralArm superclass to create Perseus arm.
"""

from .spiral_parameters import Perseus
from . import spiral_property as spiral_eq
from .spiral_arm_superclass import SpiralArm


class PerseusArm(SpiralArm):
    def __init__(self):
        super(PerseusArm, self).__init__(Perseus, 'black', 3)

    def __repr__(self):
        return "Perseus"

    def _radii_factory(self, B):
        if B <= self.params['B-kink']:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-before'],
                self.params['R-kink'])
        else:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-after'],
                self.params['R-kink'])

    def _width_factory(self, B, r):
        return spiral_eq.CylinderSize.width_kpc(
            self.params['w-kink'], r, self.params['R-kink'])+0.3
