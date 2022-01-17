# Galaxy Model
2D Galaxy model following the theoretical description in [Reid et al. (2019)](https://arxiv.org/abs/1910.03357). Note that this is not an exact copy of Reid 2019, but rather "best-effort imitation", with minor additions and modifications due to differences in programming languages and research purposes.

## Requirements
The following packages are required for this module to work:

- `descartes`
- `matplotlib`
- `numpy`
- `scipy`
- `Shapely`

For exact versions, please refer to requirements.txt. However, most of the other versions will also work for this model.

Packages not required for this module, but often used within the workflow (see example.py):

- `astropy`

This module can be installed by either 

```
pip install git+https://github.com/K-Monty/galaxy-model.git
```

or downloadable directly from the [release](https://github.com/K-Monty/galaxy-model/releases).

## How to use
See [examply.py](https://github.com/K-Monty/galaxy-model/blob/main/example.py) for a working workflow, from the conversion of astronomical coordinate system (not included in this package) to the plotting & location checks of (cartesian) coordinates. 

Individual functions within `Galaxy` class (galaxy_model/galaxy.py):

1. `add_coords(x_coord: list, y_coord: list)` and `remove_coords(x_coord: list, y_coord: list)` add and remove coordinates from the `Galaxy()` instance.

2. `plot(x_radius=16, y_radius=16, plotSrc=False)`, combined with `matplotlib.pyplot.show()`, plot the Galaxy model. `plotSrc` is defaulted as `false`. For showing the added coordinates (by `add_coords`) onto the model, it needs to be set as `True`.

3. `isOnSpiralArmOrSpur(x_coord: list, y_coord: list, verbose=False)` check whether the given coordinates is/are on spiral arm(s) or spur. Set verbose as True for more details, e.g. what spiral arm(s) a coordinate is on.

The basic syntax for the functions 1 and 2 is

```
from galaxy_model.galaxy import Galaxy
gal = Galaxy()
# arbitrary coordinates
gal.add_coord([6.5, 0.5, -2.27, 1.54], [1, 10, 4.62, 4.35])
gal.plot(plotSrc=True)
plt.show()
```

As for function 3

```
# import and instantiate Galaxy as above
# other arbitraty coordinates
coord_loc = gal.isOnSpiralArmOrSpur([0.72, 8.35], [12, 8.4], verbose=True)
print(coord_loc) 
```

The `coord_loc` is a list of encoded locations  of the given coordinates. The encoding is as below:

- 0 of the coordinate is on neither a spiral arm nor a spur

- 1 if the coordinate is on a spiral arm

- 2 if the coordinate is on a spur

- 3 if the coordinate is on multiple "objects"; e.g. multiple spiral arms, both a spur and a spiral arm

`verbose=True` will also tell what spiral arm(s) a coordinate falls on, if any.