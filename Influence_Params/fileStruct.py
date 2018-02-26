structIn={
    "space":{"sampling":{"init_size","method","distributions"}},
    "pod":{"dim_max","tolerance"},
    "surrogate":{"predictions","method","strategy"}
}

structOut={
    "space": {
        "corners": [
            [15.0, 2500.0],
            [60.0, 6000.0]
        ],
        "sampling": {
            "init_size": 200,
            "method": "halton",
            "distributions": ["Uniform(15., 60.)", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]
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
            "point_filename": "sample-space.json",
            "data_filename": "sample-data.json",
            "point_format": "json",
            "data_format": "json"
        }
    },
    "surrogate": {
        "predictions": [[30,4000]],
        "method": "pc",
        "strategy": "Quad",
        "degree": 10
    },
    "visualization": {
        "bounds": [
            [30.0, 3000.0],
            [55.0, 5500.0]
        ],
        "doe": False,
        "xdata": [1000, 2000, 2500, 3000, 4000],
        "xlabel": "s (km)",
        "ticks_nbr": 5,
        "flabel": "F(Ks, Q)"
    },
    "uq": {
        "sample": 1000,
        "test": "Channel_Flow",
        "pdf": ["Uniform(15., 60.)", "Normal(4035., 400.)"],
        "type": "aggregated",
        "method": "FAST"
    }
}