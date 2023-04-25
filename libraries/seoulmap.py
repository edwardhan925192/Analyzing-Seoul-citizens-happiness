import pandas as pd 
import numpy as np 
import folium 

#사용할 데이터와 행
def thresh_hold(seoulhouse_price,house_col):
  houseprice_scalelist = []
  for col in house_col:
    temp_list = []
    temp = (seoulhouse_price[col].astype(float).max() - seoulhouse_price[col].astype(float).min()) / 5   
    temp_list.append([seoulhouse_price[col].astype(float).min() + (temp * i)for i in range(0,7)])
    houseprice_scalelist.append(temp_list)

  return houseprice_scalelist

#josn geo_data, data, 사용할행이름,threshlist,저장할맵 object,color
def choropleth(geo_data,seoulhouse_price,col_name,thresh_list,map_name,color = 'OrRd'):  
  folium.Choropleth(geo_data = geo_data,  # 지도 경계
                    data = seoulhouse_price,    # 표시하려는 데이터
                    columns=['구', col_name],  # 열 지정
                    threshold_scale = thresh_list,
                    key_on = 'feature.properties.name',
                    fill_color = 'OrRd'
                    ).add_to(map_name)

#저장할 맵object
def gu_lat_long(map_name):
  for i, row in gu_lat_long.iterrows():
    temp = row["구"]
    s = "Info"
    folium.Marker([row["위도"], row["경도"]],icon = folium.DivIcon(html = f""" 
                  {"{}".format(temp) }  """)).add_to(map_name)
