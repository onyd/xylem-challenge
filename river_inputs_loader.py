import geopandas as gpd

# Model regression parameters
k = 1.85e-3
a = 1.52

MOUNTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

def _compute_plastic_mass(mpw, R):
    return (k * mpw * R) ** a

def compute_model(df):
    model = gpd.GeoDataFrame()
    for mounth in MOUNTHS:
        model[f"m_out_{mounth}"] = _compute_plastic_mass(df["mpw"], df[f"runoff_{mounth}"])
    return model

def load_river_inputs(path):
    """
    Load and compute the plastic river inputs from this model https://www.nature.com/articles/ncomms15611#Ack1.
    Args:
        path: the file path to the shp file of the dataset.
    Returns:
        The associated GeoDataFrame.
    """
    df = gpd.read_file(path)
    model = compute_model(df)
    model[["area", "mpw", "geometry"]] = df[["area", "mpw", "geometry"]]
    model["m_out_max"] = model.loc[:,[f"m_out_{mounth}" for mounth in MOUNTHS]].max(axis=1)
    model = model[model["m_out_max"].astype('float32') != 0.0]
    return model