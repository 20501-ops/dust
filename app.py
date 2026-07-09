import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="서울시 미세먼지 대시보드", page_icon="☁️", layout="wide")

st.title("☁️ 2025년 서울시 구별 (초)미세먼지 현황")
st.markdown("제공된 시간별 데이터를 바탕으로 서울시 각 자치구의 미세먼지 추이를 확인합니다.")

# 2. 데이터 로드 및 전처리 함수 (캐싱 적용으로 속도 최적화)
@st.cache_data
def load_data():
    # 제공된 파일명으로 데이터 불러오기
    # 인코딩 오류 시 encoding='cp949' 또는 'euc-kr'로 변경
    df = pd.read_csv("dust.csv", encoding="utf-8")
    
    # 컬럼명을 다루기 쉽게 변경
    df.columns = ['일시', '구분', '미세먼지', '초미세먼지']
    
    # '일시'를 시간(Datetime) 형식으로 변환
    df['일시'] = pd.to_datetime(df['일시'], errors='coerce')
    
    # 미세먼지 수치를 숫자형으로 변환 (빈칸 등은 결측치(NaN) 처리)
    df['미세먼지'] = pd.to_numeric(df['미세먼지'], errors='coerce')
    df['초미세먼지'] = pd.to_numeric(df['초미세먼지'], errors='coerce')
    
    # 시간순으로 데이터 정렬
    df = df.sort_values('일시')
    
    return df

df = load_data()

# 3. 사이드바 - 구별 검색/선택 기능
st.sidebar.header("🔍 검색 옵션")

# '구분' 컬럼에서 중복을 제거하여 구 리스트 추출
gu_list = df['구분'].dropna().unique().tolist()

# '평균' 데이터가 있다면 기본값으로 선택, 없다면 첫 번째 구 선택
default_idx = gu_list.index('평균') if '평균' in gu_list else 0
selected_gu = st.sidebar.selectbox("조회할 자치구를 선택하세요:", gu_list, index=default_idx)

# 선택한 구에 맞춰 데이터 필터링
filtered_df = df[df['구분'] == selected_gu]

# 시계열 그래프를 그리기 위해 인덱스를 '일시'로 설정
filtered_df = filtered_df.set_index('일시')

# 4. 메인 화면 - 데이터 시각화
st.subheader(f"📍 {selected_gu} 미세먼지 및 초미세먼지 추이")

# 탭을 나누어 미세먼지와 초미세먼지를 각각 확인
tab1, tab2 = st.tabs(["미세먼지(PM10)", "초미세먼지(PM2.5)"])

with tab1:
    st.line_chart(filtered_df['미세먼지'], color="#FF4B4B")  # 빨간색 그래프

with tab2:
    st.line_chart(filtered_df['초미세먼지'], color="#0068C9")  # 파란색 그래프

# 원본 데이터 확인 체크박스
st.divider()
if st.checkbox(f"{selected_gu} 원본 데이터 표 보기"):
    st.dataframe(filtered_df[['미세먼지', '초미세먼지']])
