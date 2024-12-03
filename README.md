**# algorithm_teamproject
Algorithm Team Project - Bike Rental Finder

이 프로젝트는 Python을 사용하여 사용자의 위치를 기준으로 가장 가까운 자전거 대여소를 찾아주는 애플리케이션입니다.
지도와 경로 안내를 제공하며, Folium과 OSMnx 라이브러리를 사용하여 최단 경로를 시각화합니다.

주요 기능
사용자의 현재 위치를 입력하여 가장 가까운 자전거 대여소 탐색
Folium 지도에 사용자 위치, 대여소 위치, 최단 경로 표시
CSV 파일을 이용한 자전거 대여소 데이터 로드
경로 계산에 OSMnx 및 NetworkX 사용
설치 방법
이 리포지터리를 클론합니다:

bash
코드 복사
git clone https://github.com/YourUsername/algorithm_teamproject.git
cd algorithm_teamproject
Python 라이브러리를 설치합니다:

bash
코드 복사
pip install -r requirements.txt
전국자전거대여소표준데이터.csv 파일이 프로젝트 디렉토리에 있어야 합니다.
데이터는 공공데이터포털에서 다운로드할 수 있습니다.

사용법
final.py 파일을 실행합니다:

bash
코드 복사
python final.py
애플리케이션에서 사용자 위치를 입력합니다 (위도, 경도 또는 주소).

지도에서 최단 경로와 대여소 위치를 확인합니다.

기술 스택
언어: Python
라이브러리:
pandas: 데이터 처리
osmnx: OpenStreetMap 데이터를 활용한 네트워크 분석
networkx: 최단 경로 계산
folium: 지도 시각화
tkinter: GUI 구축
프로젝트 구조
php
코드 복사
algorithm_teamproject/
│
├── app_1.py                 # 초기 버전 코드
├── app_2.py                 # 개선된 버전
├── final.py                 # 최종 버전 실행 파일
├── backend.py               # 경로 계산 관련 모듈
├── data.py                  # 데이터 처리 관련 코드
├── 전국자전거대여소표준데이터.csv # 자전거 대여소 데이터
├── map.html                 # 생성된 지도 파일
├── README.md                # 프로젝트 설명
├── requirements.txt         # 필요한 Python 라이브러리 목록

참고 자료
공공데이터포털 - 전국자전거대여소표준데이터
OSMnx GitHub

기여 방법
이 리포지터리를 포크합니다.
새로운 브랜치를 생성합니다:
bash
코드 복사
git checkout -b feature/새로운기능
변경 사항을 커밋하고 푸시합니다:
bash
코드 복사
git commit -m "새로운 기능 추가"
git push origin feature/새로운기능
Pull Request를 생성합니다.

라이선스
이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 LICENSE 파일을 참조하세요.
**
