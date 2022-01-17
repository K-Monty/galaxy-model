"""
An example showing how to convert ra (hrangle) and dec (deg) into
glon (deg) and glat (deg), and subsequently convert into cartesian
coordinates (x, y) which fits into the scheme of this Galactic model.

The coordinates are then plotted onto the model, and their locations
(on any spiral arm/spur) are also checked and printed.

Notes
-----
1. The functions defined here are only for demonstration purpose, and are
not used anywhere else.

2. The conversion to galactocentric cartesian system (see `c_galacto`
within the function `helio_to_galacto`) requires the inputs to be in
degrees. However, conversion from equatorial hour angle to equatorial
degrees are also possible. Doesnt have to be glon & glat degrees.
"""

from numbers import Number
from astropy import units as u
from astropy.coordinates import SkyCoord
import astropy.coordinates as coord
import matplotlib.pyplot as plt

import galaxy_model # noqa
from galaxy_model.galaxy import Galaxy


def eq_hrangle_to_gal_deg(ra: str, dec: str):
    """
    Convert equatorial coords to galactic l & b

    Parameters:
    ra, dec: strings
        RA (hrs) and dec (deg) of the coordinate
    """
    skycoordobj = coord.SkyCoord(ra, dec, unit=(u.hourangle, u.deg),
                                 frame='icrs')
    return skycoordobj.galactic.l.value, \
        skycoordobj.galactic.b.value


def helio_to_galacto(dist_kpc: Number, glon: Number, glat=0.0):
    """
    Convert coordinates from heliocentric (dist_kpc, glon, glat) to
    galactocentric cartesian system.

    Parameters
    ----------
    dist_kpc: float
        Heliocentric distance (kpc)
    glon, glat: float, float (optional)
        Galactic longitude and latitude (decimal degrees). Galactic latitude is
        set to 0 as default.

    Returns
    -------
    Galactocentric cartesian coordinate (x, y, z)
    """

    solar_dist = 8.15*u.kpc  # 8.15 kpc from GC
    z_sun = 5.5*u.pc  # 5.5 pc from Galactic mid-plane

    c = SkyCoord(l=glon*u.degree,
                 b=glat*u.degree,
                 frame='galactic',
                 distance=dist_kpc*u.kpc)
    c_galacto = c.transform_to(coord.Galactocentric(
                                            galcen_distance=solar_dist,
                                            z_sun=z_sun))
    return c_galacto.y.value, -c_galacto.x.value, c_galacto.z.value

###############################################################################


# a few sample coordinates for demonstration purpose
ra_hr = ['17:20:53.350', '17:50:14.520', '18:08:38.400', '18:46:03.720']
dec_deg = ['-35:47:01.500', '-28:54:30.700', '-19:51:52.000', '-01:54:28.000']
dist_kpc = [5.2, 13.3, 3.7, 0.6]

glon_deg_list = []
glat_deg_list = []
cartesian_x_coord = []
cartesian_y_coord = []
# z-coordinates are not used; can ignore this list
cartesian_z_coord = []

# conversion from hourangle to galactic degrees
for ra, dec in zip(ra_hr, dec_deg):
    gl, gb = eq_hrangle_to_gal_deg(ra, dec)
    glon_deg_list.append(gl)
    glat_deg_list.append(gb)

# conversion from galactic degrees to galactocentric cartesian coordinates
for gl, gb, dist in zip(glon_deg_list, glat_deg_list, dist_kpc):
    x, y, z = helio_to_galacto(dist, gl, gb)
    cartesian_x_coord.append(x)
    cartesian_y_coord.append(y)
    cartesian_z_coord.append(z)

# declare & plot the model
gal = Galaxy()
gal.add_coord(cartesian_x_coord, cartesian_y_coord)
gal.plot(plotSrc=True)
# this line is needed, as the model still heavily depends on matplotlib
plt.show()

# check the locations of given coordinates
# NOTE: this part is independent of the plotting and add_coord
# if only want to check the locations of some coordinates, only need:
# `gal = Galaxy()` and this line
coord_loc = gal.isOnSpiralArmOrSpur(cartesian_x_coord,
                                    cartesian_y_coord,
                                    verbose=True)
print(coord_loc)
