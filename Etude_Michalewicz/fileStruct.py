structIn={
    "space":{"sampling":{"init_size","method"}},
    "pod":{"dim_max","tolerance"},
    "surrogate":{"predictions","method"}
}

structOut={
    "space": {
        "corners": [
            [1.0, 1.0],
            [3.1415, 3.1415]
        ],
        "sampling": {
            "init_size": 4,
            "method": "halton"
        },
        "resampling":{
            "delta_space": 0.08,
            "resamp_size": 0,
            "method": "sigma",
            "hybrid": [["sigma", 4], ["loo_sobol", 2]],
            "q2_criteria": 0.9
        }
    },
    "pod": {
        "dim_max": 100,
        "tolerance": 0.99,
        "type": "static"
    },
    "snapshot": {
        "max_workers": 8,
        "plabels": ["x1", "x2"],
        "flabels": ["F"],
        "provider": {
            "type": "file",
            "command": "bash script.sh",
            "context_directory": "data",
            "coupling_directory": "batman-coupling",
            "timeout": 10,
            "clean": False,
            "restart": "False"
        },
        "io": {
            "point_filename": "sample-space.npy",
            "data_filename": "sample-data.npz",
            "point_format": "npy",
            "data_format": "npz"
        }
    },
    "surrogate": {
        "predictions": [[2, 2]],
        "method": "kriging"
    },
    "visualization": {
        "doe": True,
        "ticks_nbr": 5,
        "flabel": "F(x1, x2)",
        "feat_order": [2, 1]
    },
    "uq": {
        "sample": 1000,
        "test": "Michalewicz",
        "pdf": ["Uniform(1., 3.415)", "Uniform(0., 3.1415)"],
        "type": "aggregated",
        "method": "sobol"
    }
}
