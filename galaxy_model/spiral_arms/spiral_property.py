import numpy as np


class CylinderSize:
    @staticmethod
    def width_kpc(w_kink, r, rkink, sigma=1.65):
        w = w_kink + 0.042*(r-rkink)*sigma
        return w

    @staticmethod
    def height_kpc(r_galactocentric):
        if r_galactocentric <= 7:
            h = 0.02
        else:
            h = (20+(36*(r_galactocentric-7)))/1000
        return h


def get_galactocentric_radius_at_B(B, B_kink, psi, R_kink):
    exponential_element = (np.deg2rad(B_kink-B))*np.tan(np.deg2rad(psi))
    r = np.exp(exponential_element)*R_kink
    return r


def polar_to_cartesian(r, glon, glat=None):
    if glat is None:
        x = r*np.cos(np.deg2rad(glon))
        y = r*np.sin(np.deg2rad(glon))
        return x, y
    else:
        x = r*np.sin(np.deg2rad(90-abs(glat)))*np.cos(np.deg2rad(glon))
        y = r*np.sin(np.deg2rad(90-abs(glat)))*np.sin(np.deg2rad(glon))
        z = r*np.cos(np.deg2rad(90-abs(glat)))
        return x, y, z
