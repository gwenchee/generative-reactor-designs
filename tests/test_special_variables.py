import pytest, random
import numpy as np
from realm.special_variables import SpecialVariables
from deap import base, creator, tools, algorithms

poly_dict = {
    "name": "triso",
    "order": 3,
    "min": 1,
    "max": 1,
    "radius": 4235e-5,
    "volume": 10,
    "slices": 10,
    "height": 10,
}


def test_polynomial_naming():
    sv = SpecialVariables()
    var_names = sv.polynomial_naming(poly_dict)
    assert var_names == ["poly_triso_0", "poly_triso_1", "poly_triso_2", "poly_triso_3"]


def test_polynomial_triso_toolbox():
    expected_toolbox = base.Toolbox()
    expected_toolbox.register("polynomial_triso", random.uniform, 1, 1)

    toolbox = base.Toolbox()
    sv = SpecialVariables()
    toolbox = sv.polynomial_triso_toolbox(poly_dict, toolbox)

    method = getattr(toolbox, "polynomial_triso")
    expected_method = getattr(expected_toolbox, "polynomial_triso")
    assert method() == expected_method()


def test_polynomial_values():
    poly_dict = {
        "name": "triso",
        "order": 3,
        "min": -1,
        "max": 1,
        "radius": 4235e-5,
        "volume": 10,
        "slices": 10,
        "height": 10,
    }

    var_dict = {"packing_fraction": 0.1}
    toolbox = base.Toolbox()
    toolbox.register("poly_triso", random.uniform, -1, 1)
    sv = SpecialVariables()
    dz_vals = np.linspace(0, poly_dict["height"], poly_dict["slices"])
    vol_triso = 4 / 3 * np.pi * poly_dict["radius"] ** 3
    no_trisos = var_dict["packing_fraction"] * poly_dict["volume"] / vol_triso
    for i in range(1):
        poly = sv.polynomial_values(poly_dict, toolbox, var_dict)
        poly_val = (
            poly[0] * dz_vals ** 3
            + poly[1] * dz_vals ** 2
            + poly[2] * dz_vals
            + poly[3]
        )
        pf_z = poly_val / sum(poly_val) * no_trisos * vol_triso / poly_dict["volume"]
        assert len([i for i in pf_z if i > 0.25]) == 0
        assert len([i for i in poly_val if i < 0]) == 0
