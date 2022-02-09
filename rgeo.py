from unittest import result
import geopandas as gpd
from geopandas.geoseries import *
from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon


#白地図のデータをファイルからraw stringで読み込み
#https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html#prefecture00 をローカルに保存
fp = r"D:\Downloads\N03-20210101_GML\N03-20210101_GML\N03-21_210101.shp"
geo_data = gpd.read_file(fp, encoding="sjis")

def reverse_geo(geo_data, lon, lat):
    """
    reverse geocoding
    geo_dataは、geopandasでshapefileを読み込んだDF
    lon, latは経度、緯度
    """
    polygon = geo_data['geometry']
    point = Point(lon, lat)
    
    fTrue = polygon.contains(point)
    result = fTrue[fTrue == True].index

    geos = geo_data.loc[result]
    
    if geos.empty == True:
        return(None)

    reslist = [geos['N03_001'].to_string(index=False), #都道府県名
               geos['N03_003'].to_string(index=False), #郡・政令都市名
               geos['N03_004'].to_string(index=False), #市区町村名
               geos['N03_007'].to_string(index=False)] #行政区域コード

    res = ','.join(reslist)
    
    return(res)


print (reverse_geo(geo_data ,140.1225216, 36.2062132)) #テストしたい地点の緯度経度を指定
