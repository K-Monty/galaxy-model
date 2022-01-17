"""
This module use SpiralArm superclass to create Sgr-Car arm.
"""

from .spiral_parameters import Sgr_Car
from . import spiral_property as spiral_eq
from .spiral_arm_superclass import SpiralArm


class SgrCarArm(SpiralArm):
    def __init__(self):
        super(SgrCarArm, self).__init__(Sgr_Car, 'purple', 51)

    def __repr__(self):
        return "SgrCar"

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
        else:
            return self._spine_radius_at_B_and_psi(
                B, self.params['B-kink'],
                self.params['psi-after'],
                self.params['R-kink']+0.6)

    def _width_factory(self, B, r):
        return spiral_eq.CylinderSize.width_kpc(
            self.params['w-kink'], r, self.params['R-kink'])+0.25
