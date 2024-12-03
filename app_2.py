import pandas as pd
import folium

# CSV 파일 읽기 (인코딩을 euc-kr 또는 cp949로 설정)
df = pd.read_csv("전국자전거대여소표준데이터.csv", encoding='euc-kr')  # 파일명에 맞게 수정

# 현재 위치 설정 (예: 서울 시청 좌표)
current_location = {'lat': 37.5665, 'lon': 126.9780}

# 지도 생성
map_ = folium.Map(location=[current_location['lat'], current_location['lon']], zoom_start=13)

# 자전거 대여소 위치 표시
for idx, row in df.iterrows():
    folium.Marker(
        [row['위도'], row['경도']],  # '위도'와 '경도'를 CSV 파일에 맞게 사용
        tooltip=row['자전거대여소명']  # '자전거대여소명'을 tooltip에 사용
    ).add_to(map_)

# 결과를 HTML 파일로 저장
map_.save("bike_station_map.html")
print("지도 생성 완료: bike_station_map.html")