import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # genre 열에 세로막대(|) 기호로 여러 장르가 적힌 경우 첫 번째 장르만 사용
    df["genre_main"] = df["genre"].astype(str).str.split("|").str[0].str.strip()

    # openDt(여덟 자리 숫자)를 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")

    return df


df = load_data()

# =========================================================
# 구역 1. 장르별 영화 편수 (도넛 그래프)
# =========================================================
st.header("1. 장르별 영화 편수")

genre_counts = df["genre_main"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

fig_genre = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
)
fig_genre.update_traces(
    textinfo="percent",
    hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig_genre.update_layout(legend_title_text="장르")

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** ")

st.divider()

# =========================================================
# 앞으로 그래프가 추가될 자리
# =========================================================
# st.header("2. ...")
