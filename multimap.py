#ctestwinのtextを読み込み白地図を描画
from unittest.case import DIFF_OMITTED
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pathlib
import matplotlib.colors as mcolors


logfile = "log.txt" #ctestwinでファイル出力 - その他ファイル出力 - ログファイル出力 - その他備考なしで作成したものを使ってください

#https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_0.html#prefecture00 から白地図をあらかじめダウンロードしてローカルに展開し、指定してください
#"D:\Downloads\N03-20210101_GML\N03-20210101_GML\N03-21_210101.shp" 
#https://github.com/w-ockham/JCC-JCG-List/blob/master/munitable.csv （w-ockham/JCC-JCG-List is licensed under the Apache License 2.0）のデータを改変しました。
#JCCと白地図の対応IDが入った以下ファイルをあらかじめダウンロードしてフォルダに入れておく
jccjcgdata = "multitable.csv"

#logファイル読み込み
df_log = pd.read_csv(
    logfile,
    delim_whitespace=True,
    header=None, 
    skiprows=2,
    names=('No', 'Date', 'Time', 'CS', 'Band', 'Mode', 'His', 'My'),
    index_col=0
)
df_log['My'] = df_log['My'].astype(str).str[2:]
#Working DFとなるdf_Myを作成
df_My =  pd.DataFrame()
#ログファイルのMyの数を数えてユニークマルチの交信数としてcountに代入
df_My['Count'] = df_log['My'].value_counts()
#indexを追加
df_My['JCCJCGd'] = df_My.index
df_My.reset_index(inplace=True, drop=True)

#白地図のデータをファイルからraw stringで読み込み
fp = r"D:\Downloads\N03-20210101_GML\N03-20210101_GML\N03-21_210101.shp"
geo_data = gpd.read_file(fp, encoding="sjis")

#マスターデータを読み込み
df_list = pd.read_csv(
    jccjcgdata,
    dtype={'muniCd': str, 'PrefNo': str,'Pref': str, 'City': str, 'JCCCd': str, 'JCC_text': str, 'WDCd': str, 'WDCd_text': str,'SHCd': str,'SHCd_text': str,'JCGCd': str, 'JCG_text': str},
#CSVのフィールド構成
#muniCd,PrefNo,Pref,City,JCCCd,JCC_text,WDCd,WDCd_text,SHCd,SHCd_Text,JCGCd,JCG_text
)

#~で重複する空白の値を含むレコードをdropして、一意のリストにする
df_JCC = df_list[~df_list.duplicated(subset='JCCCd')]
df_WD = df_list[~df_list.duplicated(subset='WDCd')]
df_JCG = df_list[~df_list.duplicated(subset='JCGCd')]

#df_My にJCC/WD(市区郡詳細コード)/JCGを追加し、全国の自治体コードmuniCdを転記する
df_My.insert(2, 'JCCmuniCd', df_My['JCCJCGd'].map(df_JCC.set_index('JCCCd')['muniCd']))   
df_My.insert(2, 'WDmuniCd',  df_My['JCCJCGd'].map(df_WD.set_index ('WDCd') ['muniCd']))   
df_My.insert(3, 'JCGmuniCd', df_My['JCCJCGd'].map(df_JCG.set_index('JCGCd')['muniCd']))   
#print(df_My)

#muniCdを追加後、JCCmuniCdの欠損に、WDとJCGの値を転記してマスターキーとする
df_My['JCCmuniCd'].fillna(df_My['JCGmuniCd'], inplace=True)
df_My['JCCmuniCd'].fillna(df_My['WDmuniCd'], inplace=True)

#print(df_My)

#マルチ毎の交信数をJCC/WD/JCFのPDに転記する。地図をそれぞれで作成するもとデータ
df_JCC.insert(5, 'Count', df_JCC['muniCd'].map(df_My.set_index('JCCmuniCd')['Count']))   
df_WD.insert(5, 'Count', df_WD['muniCd'].map(df_My.set_index('JCCmuniCd')['Count']))   
df_JCG.insert(5, 'Count', df_JCG['muniCd'].map(df_My.set_index('JCCmuniCd')['Count']))   

#print(df_WD)

#地図塗りつぶしデータ N03_007は国土地理院のデータの列名
JCCmap_data = geo_data.merge(df_JCC, left_on = 'N03_007', right_on = 'muniCd', how = "left")
WDmap_data = geo_data.merge(df_WD, left_on = 'N03_007', right_on = 'muniCd', how = "left")
JCGmap_data = geo_data.merge(df_JCG, left_on = 'N03_007', right_on = 'muniCd', how = "left")

#白地図描画
#色設定。必要に応じてカスタマイズ
#Cmap https://matplotlib.org/stable/tutorials/colors/colormaps.html
vmin, vmax, vcenter = 0, 10, 5
norm = mcolors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
# create a normalized colorbar
cmap = 'coolwarm'
#cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)

#map_data.plot(color="lightseagreen", linewidth=0.5, edgecolor="lightgray", figsize=(5, 5))
#plt.savefig('Japan.png')
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
#コンテスト名を外に出す、File名と同じに
ax.set_title('Multi Map', fontsize=18)
#緯度経度指定で描画エリア設定。全国地図で大きすぎる場合にはマルチの範囲でgooglemapでもみて範囲を見て設定してください。
#plt.xlim([139,141])
#plt.ylim([35,37])

#実際に描画
geo_data.plot(ax = ax, edgecolor='#444', facecolor='white', linewidth = 0.1) 
JCCmap_data.plot(column='Count', ax=ax, cmap='Oranges', norm=norm, legend=False )
WDmap_data.plot(column='Count', ax=ax, cmap='Oranges', norm=norm, legend=False )
JCGmap_data.plot(column='Count', ax=ax, cmap='Oranges', norm=norm, legend=False )

#add colorbar
#fig.colorbar(cbar, ax=ax)
fig.savefig('multimap.png')

#マスターデータを念のためCSVファイルで保存。確認用なので、削除しても結構です。
df_JCC.to_csv(
        pathlib.Path("", "multimap.csv"),
        #index=False,
        #quoting=csv.QUOTE_NONNUMERIC,
        encoding="utf_8_sig"
)
