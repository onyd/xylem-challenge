import geopandas as gpd
import numpy as np
import pandas as pd

from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString

import itertools
from operator import itemgetter

def ckd_nearest_point_to_point(gdA, gdB):

    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)

    return gdf

def ckd_nearest_point_to_line(gdfA, gdfB, gdfB_cols=['Place']):
    A = np.concatenate(
        [np.array(geom.coords) for geom in gdfA.geometry.to_list()])
    B = [np.array(geom.coords) for geom in gdfB.geometry.to_list()]
    B_ix = tuple(itertools.chain.from_iterable(
        [itertools.repeat(i, x) for i, x in enumerate(list(map(len, B)))]))
    B = np.concatenate(B)
    ckd_tree = cKDTree(B)
    dist, idx = ckd_tree.query(A, k=1)
    idx = itemgetter(*idx)(B_ix)
    gdf = pd.concat(
        [gdfA, gdfB.loc[idx, gdfB_cols].reset_index(drop=True),
         pd.Series(dist, name='dist')], axis=1)
    return gdf


if __name__ == "__main__":
    gpd1 = gpd.GeoDataFrame([['John', 1, Point(1, 1)], ['Smith', 1, Point(2, 2)],
                         ['Soap', 1, Point(0, 2)]],
                        columns=['Name', 'ID', 'geometry'])
    gpd2 = gpd.GeoDataFrame([['Work', Point(0, 1.1)], ['Shops', Point(2.5, 2)],
                            ['Home', Point(1, 1.1)]],
                            columns=['Place', 'geometry'])
    print("Point-Point nearest search: \n", ckd_nearest_point_to_point(gpd1, gpd2))


    gpd1 = gpd.GeoDataFrame([['John', 1, Point(1, 1)],
                            ['Smith', 1, Point(2, 2)],
                            ['Soap', 1, Point(0, 2)]],
                            columns=['Name', 'ID', 'geometry'])
    gpd2 = gpd.GeoDataFrame([['Work', LineString([Point(100, 0), Point(100, 1)])],
                            ['Shops', LineString([Point(101, 0), Point(101, 1), Point(102, 3)])],
                            ['Home',  LineString([Point(101, 0), Point(102, 1)])]],
                            columns=['Place', 'geometry'])
    print("Point-Line nearest search\n", ckd_nearest_point_to_line(gpd1, gpd2))
