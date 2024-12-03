import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
import folium
import osmnx as ox
import networkx as nx
import os
from pathlib import Path
import webbrowser

# CSV 파일에서 자전거 대여소 좌표 가져오기
def load_bike_stations(csv_path):
    try:
        bike_data = pd.read_csv(csv_path, encoding='cp949')  # cp949는 한글 인코딩용
        return list(zip(bike_data['위도'], bike_data['경도']))
    except FileNotFoundError:
        messagebox.showerror("오류", f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        exit()
    except Exception as e:
        messagebox.showerror("오류", f"CSV 파일을 로드하는 중 오류가 발생했습니다: {str(e)}")
        exit()

# 사용자와 자전거 대여소 좌표 설정
csv_file_path = '전국자전거대여소표준데이터.csv'
bike_stations = load_bike_stations(csv_file_path)
map_file = Path(os.getcwd(), "map.html")

def calculate_nearest_station(user_location, stations):
    try:
        print("1. 그래프 생성 시작...")
        graph = ox.graph_from_point(user_location, dist=2000, network_type='walk')
        print("1. 그래프 생성 완료.")

        print("2. 사용자 노드 탐색 시작...")
        user_node = ox.distance.nearest_nodes(graph, user_location[1], user_location[0])
        print(f"2. 사용자 노드 탐색 완료. 사용자 노드: {user_node}")

        print("3. 대여소 노드 탐색 시작...")
        station_nodes = [ox.distance.nearest_nodes(graph, station[1], station[0]) for station in stations]
        print(f"3. 대여소 노드 탐색 완료. 대여소 노드: {station_nodes}")

        print("4. 경로 계산 시작...")
        distance, path = nx.single_source_bellman_ford(graph, user_node, weight='length')
        print("4. 경로 계산 완료.")

        print("5. 최단 거리 대여소 탐색 시작...")
        min_distance = float('inf')
        nearest_station_node = None
        shortest_path = None

        for station_node in station_nodes:
            if station_node in distance and distance[station_node] < min_distance:
                min_distance = distance[station_node]
                nearest_station_node = station_node
                shortest_path = path[station_node]
        print(f"5. 최단 거리 대여소 탐색 완료. 최단 거리: {min_distance}m, 노드: {nearest_station_node}")

        return nearest_station_node, min_distance, shortest_path, graph
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        messagebox.showerror("오류", f"경로 계산 중 오류가 발생했습니다: {str(e)}")
        exit()

def show_map():
    user_lat = simpledialog.askfloat("사용자 위치 입력", "현재 위치의 위도를 입력하세요:")
    user_lon = simpledialog.askfloat("사용자 위치 입력", "현재 위치의 경도를 입력하세요:")
    
    if user_lat is None or user_lon is None:
        messagebox.showerror("입력 오류", "올바른 위도와 경도를 입력해주세요.")
        return

    user_location = (user_lat, user_lon)

    nearest_station_node, min_distance, shortest_path, graph = calculate_nearest_station(user_location, bike_stations)
    shortest_path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]
    nearest_station_coords = (graph.nodes[nearest_station_node]['y'], graph.nodes[nearest_station_node]['x'])

    print(f"가장 가까운 대여소 좌표: {nearest_station_coords}")
    print(f"가장 가까운 대여소까지의 거리: {min_distance:.2f}m")

    messagebox.showinfo(
        "가장 가까운 대여소 정보",
        f"대여소 위치 (위도, 경도): {nearest_station_coords}\n거리: {min_distance:.2f}m"
    )

    m = folium.Map(location=user_location, zoom_start=10)
    folium.Marker(user_location, popup="사용자 위치", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(nearest_station_coords, popup="가장 가까운 대여소", icon=folium.Icon(color="green")).add_to(m)
    folium.PolyLine(shortest_path_coords, color="red", weight=5, opacity=0.8, popup="최단 경로").add_to(m)
    
    map_file_path = map_file.as_posix()  # POSIX 형식 경로로 변환
    m.save(map_file_path)
    webbrowser.open(f"file:///{map_file_path}")

root = tk.Tk()
root.title("자전거 대여소 찾기")

button = tk.Button(root, text="가장 가까운 대여소 찾기", command=show_map)
button.pack()

root.mainloop()
