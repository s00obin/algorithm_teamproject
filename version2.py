import tkinter as tk # GUI 구현
from tkinter import messagebox
import folium # 지도 생성 및 시각화
import osmnx as ox # 도로 네트워크
import networkx as nx # 그래프 데이터 구조 및 알고리즘 처리
import os # 파일 및 디렉토리 작업
import webbrowser # 웹브라우저 사용

# 사용자와 자전거 대여소 좌표
user_location = (37.5451, 127.1017) # 서울 광장동
bike_stations = [
    # !!!!!---이건 csv파일에서 긁어오는 식으로 바꾸면 좋을거같아요---!!!!!!
    (37.6110, 127.0584), (37.5910, 127.0144), (37.5902, 127.0175), (37.5870, 127.0209), (37.6103, 127.0333), (37.6191, 127.0551), (37.5924, 126.9975), (37.5893, 127.0074), (37.6064, 127.0539), (37.6064, 127.0539), (37.5929, 127.0339), (37.5929, 127.0339), (37.6056, 127.0474), (37.6027, 127.0209), (37.6179, 127.0523), (37.6062, 127.0347), (37.6013, 127.0332), (37.6026, 127.0123), (37.6163, 127.0026), (37.6163, 127.0026), (37.6035, 127.0246), (37.5946, 126.9950), (37.5825, 127.0289), (37.6066, 127.0127), (37.5410, 127.0190), (37.5508, 127.0346), (37.5888, 127.0063), (37.5937, 127.0131), (37.5557, 127.1569), (37.6610, 127.0736), (37.6250, 127.0703), (37.6250, 127.0703), (37.4822, 126.8777), (37.6456, 127.0628), (37.6456, 127.0628), (37.6610, 127.0736), (37.5988, 127.0402), (37.6038, 127.0225), (37.5915, 127.0201), (37.6090, 127.0297), (37.5946, 126.9952), (37.5866, 127.0320), (37.6027, 127.0395), (37.6034, 127.0365), (37.6011, 127.0453), (37.6011, 127.0453), (37.6100, 127.0162), (37.6099, 127.0369), (37.6065, 127.0623), (37.5373, 127.0939), (37.5373, 127.0939), (37.6051, 127.0110), (37.6192, 127.0448), (37.6031, 127.0136), (37.5937, 127.0028), (37.5852, 127.0197), (37.5838, 127.0220), (37.5902, 127.0041), (37.5930, 126.9975), (37.5180, 127.0470), (37.6001, 127.0139), (37.6094, 127.0193), (37.6050, 127.0220), (37.6048, 127.0230), (37.6228, 127.0493), (37.5828, 127.0156), (37.5999, 127.0224)

]

# 현재 디렉토리에 map.html 저장
map_file = os.path.join(os.getcwd(), "map.html")

def calculate_nearest_station(user_location, stations):
    # 도로 네트워크 그래프 가져오기
    graph = ox.graph_from_point(user_location, dist= 5000, network_type = 'walk') # dist는 미터 단위임

    # 사용자와 가장 가까이 있는 자전거 대여소 찾기
    user_node = ox.distance.nearest_nodes(graph, user_location[1], user_location[0]) # user_location[1],[0]은 각각 위도와 경도임
    station_nodes = [ox.distance.nearest_nodes(graph, station[1], station[0]) for station in stations]

    # 벨만포드 알고리즘으로 최단경로 계산하기
    distance, path = nx.single_source_bellman_ford(graph, user_node, weight='length')

    # 가장 가까운 대여소 찾기
    min_distance = float('inf')
    nearest_station_node = None
    shortest_path = None

    for station_node in station_nodes:
        if station_node in distance and distance[station_node] < min_distance:
            min_distance = distance[station_node]
            nearest_station_node = station_node
            shortest_path = path[station_node]

    return nearest_station_node, min_distance, shortest_path, graph

def show_map():
    # 가장 가까운 대여소와 경로 계산
    nearest_station_node, min_distance, shortest_path, graph = calculate_nearest_station(user_location, bike_stations)
    
    # 경로 좌표 계산
    shortest_path_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

    # 대여소의 좌표 계산
    nearest_station_coords = (graph.nodes[nearest_station_node]['y'], graph.nodes[nearest_station_node]['x'])

    # 콘솔에 정보 출력
    print(f"가장 가까운 대여소 좌표: {nearest_station_coords}")
    print(f"가장 가까운 대여소까지의 거리: {min_distance:.2f}m")

    # 자전거대여소까지의 거리와 위치 표시
    messagebox.showinfo(
        "가장 가까운 대여소 정보",
        f"대여소 위치 (위도, 경도): {nearest_station_coords}\n거리: {min_distance:.2f}m"
    )

    # 지도 생성 및 경로 표시
    m = folium.Map(location=user_location, zoom_start=10)
    folium.Marker(user_location, popup="사용자 위치", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(nearest_station_coords, popup="가장 가까운 대여소", icon=folium.Icon(color="green")).add_to(m)
    folium.PolyLine(shortest_path_coords, color="red", weight=5, opacity=0.8, popup="최단 경로").add_to(m)
    
    # 지도 HTML 저장
    m.save(map_file)
    
    # 기본 웹 브라우저에서 지도 파일 열기
    webbrowser.open(f"file:///{map_file.replace('\\', '/')}")

# tkinter gui 
root = tk.Tk()
root.title("자전거 대여소 찾기")

# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(os.path.dirname(map_file)):
    os.makedirs(os.path.dirname(map_file))

button = tk.Button(root, text="가장 가까운 대여소 찾기", command=show_map)
button.pack()

root.mainloop()