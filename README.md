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
See examply.py.