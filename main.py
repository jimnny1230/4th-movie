import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    # 장르: 세로막대(|)로 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"].fillna("미분류").astype(str).str.split("|").str[0].str.strip()
    )
    # 개봉일: 여덟 자리 숫자(예: 20250115) -> 날짜
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str).str[:8], format="%Y%m%d", errors="coerce"
    )
    return df


def insight_box(text: str) -> None:
    """그래프 아래 '이 그래프로 알 수 있는 것' 한 문장 자리."""
    if text.strip():
        st.info(f"**이 그래프로 알 수 있는 것**  \n{text}")
    else:
        st.info("**이 그래프로 알 수 있는 것**  \n(여기에 한 문장을 적어 주세요)")


df = load_data()

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption(f"1년간 박스오피스 10위권에 든 영화 중 이 기간에 개봉한 {len(df)}편의 요약표")

with st.expander("데이터 미리 보기"):
    st.dataframe(df, use_container_width=True)

st.divider()

# ---------------------------------------------------------------
# 구역 1. 장르별 영화 편수 (도넛 그래프)
# ---------------------------------------------------------------
with st.container():
    st.header("1. 장르별 영화 편수")

    genre_counts = df["genre"].value_counts().reset_index()
    genre_counts.columns = ["장르", "편수"]

    fig1 = px.pie(genre_counts, names="장르", values="편수", hole=0.5)
    fig1.update_traces(
        textinfo="label+percent",
        hovertemplate="장르: %{label}<br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
    )
    fig1.update_layout(legend_title_text="장르")
    st.plotly_chart(fig1, use_container_width=True)

    INSIGHT_1 = ""  # 예: "○○ 장르가 전체의 ○%로 가장 많다."
    insight_box(INSIGHT_1)

st.divider()

# 다음 그래프는 위와 같은 형식으로 아래에 구역을 추가하면 돼요.
