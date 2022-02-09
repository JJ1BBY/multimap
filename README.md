# multimap.py
コンテストのログデータ(CSV)から取得マルチの区域を塗りつぶす地図を作成するpythonのスクリプトです
全市全郡などに対応しますが、ロカコンで独自のマルチ番号や、JCGより細かい独自のマルチ番号を持つコンテストには対応していません。
また、都道府県レベルの番号の対応はまだ行っていません。
関東UHFや全市全郡ではお使いいただけます。

munitable.csvは
https://github.com/w-ockham/JCC-JCG-List/blob/master/munitable.csv （w-ockham/JCC-JCG-List is licensed under the Apache License 2.0）のデータを利用し、追加を行っています。
ありがとうございました。

#regeo.py
逆ジオコーディング（緯度経度から地名を引く）サンプルコードです。
40 print (reverse_geo(geo_data ,140.1225216, 36.2062132)) #テストしたい地点の緯度経度を指定
https://y-mattu.hatenablog.com/entry/2017/09/18/185014 を参考にさせていただきました。


