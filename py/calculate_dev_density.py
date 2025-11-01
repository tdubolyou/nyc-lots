#!/usr/bin/env python3
"""
Calculate development density (units/ha) for development polygons.

This script joins development point data to development polygons and calculates
the units per hectare for each polygon.
"""

import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import numpy as np

def load_geojson(file_path):
    """Load GeoJSON file and return as GeoDataFrame."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return gpd.GeoDataFrame.from_features(data['features'])
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def calculate_units_per_ha(dev_par_path, dev_pts_path, output_path):
    """
    Calculate units per hectare for development polygons.
    
    Args:
        dev_par_path: Path to development polygons GeoJSON
        dev_pts_path: Path to development points GeoJSON  
        output_path: Path to save the updated development polygons
    """
    
    print("Loading development polygons...")
    dev_par = load_geojson(dev_par_path)
    if dev_par is None:
        return
    
    print("Loading development points...")
    dev_pts = load_geojson(dev_pts_path)
    if dev_pts is None:
        return
    
    print(f"Development polygons: {len(dev_par)} features")
    print(f"Development points: {len(dev_pts)} features")
    
    # Ensure both GeoDataFrames have the same CRS
    if dev_par.crs != dev_pts.crs:
        dev_pts = dev_pts.to_crs(dev_par.crs)
    
    # Calculate area of each polygon in hectares
    dev_par['area_ha'] = dev_par.geometry.area / 10000  # Convert m² to hectares
    
    # Spatial join: find which points fall within each polygon
    print("Performing spatial join...")
    joined = gpd.sjoin(dev_pts, dev_par, how='inner', predicate='within')
    
    # Group by polygon and calculate total units and units/ha
    print("Calculating units per hectare...")
    polygon_stats = joined.groupby('index_right').agg({
        'Units': 'sum',  # Total units in this polygon
        'area_ha': 'first'  # Area of the polygon
    }).reset_index()
    
    # Calculate units per hectare
    polygon_stats['UnitsHA'] = polygon_stats['Units'] / polygon_stats['area_ha']
    
    # Merge the calculated stats back to the original polygons
    dev_par_updated = dev_par.copy()
    dev_par_updated = dev_par_updated.merge(
        polygon_stats[['index_right', 'Units', 'UnitsHA']], 
        left_index=True, 
        right_on='index_right', 
        how='left'
    )
    
    # Fill NaN values with 0 for polygons that have no development points
    dev_par_updated['Units'] = dev_par_updated['Units'].fillna(0)
    dev_par_updated['UnitsHA'] = dev_par_updated['UnitsHA'].fillna(0)
    
    # Drop the index column used for merging
    dev_par_updated = dev_par_updated.drop('index_right', axis=1)
    
    print(f"Updated development polygons: {len(dev_par_updated)} features")
    print(f"Polygons with development: {len(dev_par_updated[dev_par_updated['Units'] > 0])}")
    print(f"Average units/ha: {dev_par_updated['UnitsHA'].mean():.2f}")
    print(f"Max units/ha: {dev_par_updated['UnitsHA'].max():.2f}")
    
    # Save the updated GeoJSON
    print(f"Saving to {output_path}...")
    dev_par_updated.to_file(output_path, driver='GeoJSON')
    print("Done!")

def main():
    """Main function to run the calculation."""
    
    # File paths
    dev_par_path = "../data/final/dev_par.json"
    dev_pts_path = "../data/final/dev_pts.json"
    output_path = "../data/final/dev_par_with_density.json"
    
    print("Development Density Calculator")
    print("=" * 40)
    
    calculate_units_per_ha(dev_par_path, dev_pts_path, output_path)

if __name__ == "__main__":
    main() 