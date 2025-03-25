### Activate virtual environment
```bash
.venv/Activate/Scripts
```

### Decode .lyt track file 
```bash
python3 track_decoder.py -i encoded_tracks/AU1_FG_2023_practise.lyt -o decoded_tracks/AU1_FG_2023_practise.json
```

### Encode json into .lyt track file
```bash
python3 track_encoder.py -i decoded_tracks/AU1_FG_2023_practise.json -o encoded_tracks/AU1_FG_2023_practise_2.lyt
```

### Important all .lyt track names must start with "AU1_"
"AU1_" tells the game which track to use as base. Then all objects added on top of that track.
```text
AU1_FG_2023_practise.lyt
AU1_FG2023_R1.lyt
AU1_LX_week3.lyt
```

### Track json example
```json
[
    {
        "position": {
            "x": 13.06,
            "y": -637.31,
            "z": 0.0
        },
        "rotation": -90.0,
        "type": "AXO_CHALK_LINE2"
    },
    {
        "position": {
            "x": -2.62,
            "y": -691.5,
            "z": 0.0
        },
        "rotation": -12.7,
        "type": "AXO_CONE_RED2"
    },
    {
        "position": {
            "x": -2.5,
            "y": -695.75,
            "z": 0.0
        },
        "rotation": -12.7,
        "type": "AXO_CONE_RED2"
    },
    {
        "position": {
            "x": 8.06,
            "y": -699.75,
            "z": 0.0
        },
        "rotation": -12.7,
        "type": "AXO_CONE_RED2"
    }
]
```