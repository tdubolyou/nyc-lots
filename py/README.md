# Development Density Calculator

This script calculates units per hectare for development polygons by joining development point data.

## Setup

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script from the `py` directory:

```bash
cd py
python calculate_dev_density.py
```

## What it does

1. **Loads development data**: Reads `dev_par.json` (polygons) and `dev_pts.json` (points)
2. **Spatial join**: Finds which development points fall within each polygon
3. **Calculates density**: Computes total units and units per hectare for each polygon
4. **Outputs results**: Saves updated polygons with density data to `dev_par_with_density.json`

## Output

The script creates a new GeoJSON file with additional fields:
- `Units`: Total number of units in the polygon
- `UnitsHA`: Units per hectare (density)
- `area_ha`: Area of the polygon in hectares

## Files

- `calculate_dev_density.py`: Main calculation script
- `requirements.txt`: Python dependencies
- `README.md`: This documentation

## Input files (expected in `../data/final/`)

- `dev_par.json`: Development polygons
- `dev_pts.json`: Development points with unit counts

## Output files

- `dev_par_with_density.json`: Updated polygons with density calculations 