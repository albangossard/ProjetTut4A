structIn={
    "space":{"sampling":{"init_size","method"}},
    "pod":{"dim_max","tolerance"},
    "surrogate":{"predictions","method"}
}

structOut={
    "space": {
        "corners": [
            [-3.1415, -3.1415, -3.1415],
            [3.1415, 3.1415, 3.1415]
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
        "plabels": ["x1", "x2", "x3"],
        "flabels": ["F"],
        "provider": {
            "type": "plugin",
            "module": "function",
            "function": "f",
            "clean": False
        },
        "io": {
            "point_filename": "sample-space.json",
            "data_filename": "sample-data.json",
            "point_format": "json",
            "data_format": "json"
        }
    },
    "surrogate": {
        "predictions": [[1, 1, 1]],
        "method": "kriging"
    },
    "uq": {
        "sample": 1000,
        "test": "Ishigami",
        "pdf": ["Uniform(-3.1415, 3.1415)", "Uniform(-3.1415, 3.1415)", "Uniform(-3.1415, 3.1415)"],
        "type": "aggregated",
        "method": "sobol"
    }
}