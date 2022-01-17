"""
This module use SpiralArm superclass to create local arm.
"""

from .spiral_parameters import Local
from .spiral_property import CylinderSize
from .spiral_arm_superclass import SpiralArm


class LocalArm(SpiralArm):

    def __init__(self):
        super(LocalArm, self).__init__(Local, 'cyan', 3)

    def __repr__(self):
        return "Local"

    def _radii_factory(self, B):
        return self._spine_radius_at_B_and_psi(
            B, self.params['B-kink'],
            self.params['psi'],
            self.params['R-kink'])

    def _width_factory(self, B, r):
        return CylinderSize.width_kpc(
            self.params['w-kink'], r, self.params['R-kink']) + 0.2
