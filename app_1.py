import tkinter.messagebox
import folium
import tkinter as tk
from backend import bellman_ford, find_nearest_station
from data import vertices, edges, bike_stations

def display_map(current_location, nearest_station):
    map_ = folium.Map(location=[current_location['lat'], current_location['lon']], zoom_start=13)
    folium.Marker([current_location['lat'], current_location['lon']], tooltip="Current Location").add_to(map_)
    folium.Marker([nearest_station['lat'], nearest_station['lon']], tooltip="Nearest Bike Station").add_to(map_)
    map_.save("map.html")

def find_and_display():
    # 현재 위치
    current_location = 0  # 예시
    dist = bellman_ford(vertices, edges, current_location)
    nearest_station, min_dist = find_nearest_station(bike_stations, dist)
    if nearest_station != -1:
        # 지도에 표시할 대여소 좌표
        bike_station_location = {'lat': 37.5665, 'lon': 126.9780}  # 예시 좌표
        display_map(current_location={'lat': 37.5642135, 'lon': 127.0016985}, nearest_station=bike_station_location)

        # 기존 코드 수정
        tkinter.messagebox.showinfo("결과", f"가장 가까운 자전거 대여소는 노드 {nearest_station}에 있으며, 거리: {min_dist}")

    else:
        tkinter.messagebox.showinfo("결과", "근처에 자전거 대여소가 없습니다.")

# GUI 설정
root = tk.Tk()
root.title("자전거 대여소 찾기")
button = tk.Button(root, text="가장 가까운 대여소 찾기", command=find_and_display)
button.pack()

root.mainloop()