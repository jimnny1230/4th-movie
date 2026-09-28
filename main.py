import numpy as np
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

# ---------------------------------------------------------------
# 구역 2. 장르 안의 영화별 총 관객 (트리맵)
# ---------------------------------------------------------------
with st.container():
    st.header("2. 장르별 영화 총 관객 트리맵")

    tree_df = df.dropna(subset=["total_audi"])
    fig2 = px.treemap(
        tree_df,
        path=[px.Constant("전체"), "genre", "movieNm"],
        values="total_audi",
    )
    fig2.update_traces(
        hovertemplate="%{label}<br>총 관객: %{value:,}명<extra></extra>",
        textinfo="label",
    )
    fig2.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig2, use_container_width=True)

    INSIGHT_2 = ""  # 예: "○○ 장르에서 총 관객이 가장 큰 영화는 ○○이다."
    insight_box(INSIGHT_2)

st.divider()

# ---------------------------------------------------------------
# 구역 3. 총 관객 히스토그램
# ---------------------------------------------------------------
with st.container():
    st.header("3. 총 관객 분포 (히스토그램)")

    audi = df["total_audi"].dropna()

    # 그래프와 문구가 같은 구간을 쓰도록 구간을 직접 계산
    counts, edges = np.histogram(audi, bins=20)
    fig3 = px.histogram(df.dropna(subset=["total_audi"]), x="total_audi")
    fig3.update_traces(
        xbins=dict(start=edges[0], end=edges[-1], size=edges[1] - edges[0]),
        hovertemplate="총 관객: %{x:,}명<br>영화 수: %{y}편<extra></extra>",
    )
    fig3.update_layout(xaxis_title="총 관객(명)", yaxis_title="영화 수(편)", bargap=0.05)
    st.plotly_chart(fig3, use_container_width=True)

    # 가장 많이 몰린 구간과 관객이 가장 많은 영화
    peak = int(np.argmax(counts))
    lo, hi = edges[peak], edges[peak + 1]
    share = counts[peak] / counts.sum() * 100
    top = df.loc[df["total_audi"].idxmax()]
    INSIGHT_3 = (
        f"대부분의 영화는 총 관객 {lo:,.0f}~{hi:,.0f}명 구간에 몰려 있고"
        f"({counts[peak]}편, 전체의 {share:.0f}%), "
        f"관객이 가장 많은 영화는 '{top['movieNm']}'({top['total_audi']:,.0f}명)이다."
    )
    insight_box(INSIGHT_3)

st.divider()

# ---------------------------------------------------------------
# 구역 4. 개봉일 스크린수와 총 관객 (산점도)
# ---------------------------------------------------------------
with st.container():
    st.header("4. 개봉일 스크린수와 총 관객의 관계 (산점도)")

    scatter_df = df.dropna(subset=["first_scrn", "total_audi"])
    fig4 = px.scatter(
        scatter_df,
        x="first_scrn",
        y="total_audi",
        color="genre",
        hover_name="movieNm",
        hover_data={"genre": True, "first_scrn": ":,", "total_audi": ":,"},
        labels={
            "first_scrn": "개봉일 스크린수(개)",
            "total_audi": "총 관객(명)",
            "genre": "장르",
        },
    )
    fig4.update_traces(marker=dict(size=9, opacity=0.8))
    st.plotly_chart(fig4, use_container_width=True)

    INSIGHT_4 = ""  # 예: "개봉일 스크린수가 많을수록 총 관객도 많은 경향이 있다."
    insight_box(INSIGHT_4)

st.divider()

# ---------------------------------------------------------------
# 구역 5. 장르별 총 관객 상자 그림 (영화 10편 이상인 장르만)
# ---------------------------------------------------------------
with st.container():
    st.header("5. 장르별 총 관객 상자 그림")

    genre_size = df["genre"].value_counts()
    big_genres = genre_size[genre_size >= 10].index.tolist()

    if big_genres:
        box_df = df[df["genre"].isin(big_genres)].dropna(subset=["total_audi"])
        fig5 = px.box(
            box_df,
            x="genre",
            y="total_audi",
            color="genre",
            points="outliers",  # 상자 밖으로 튀는 점만 표시
            hover_name="movieNm",
            hover_data={"genre": False, "total_audi": ":,"},
            category_orders={"genre": big_genres},
            labels={"genre": "장르", "total_audi": "총 관객(명)"},
        )
        fig5.update_layout(showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("영화가 10편 이상인 장르만 보여요: " + ", ".join(big_genres))
    else:
        st.warning("영화가 10편 이상인 장르가 없어요.")

    INSIGHT_5 = ""  # 예: "○○ 장르는 상자가 넓어 영화마다 관객 수 차이가 크다."
    insight_box(INSIGHT_5)

st.divider()

# ---------------------------------------------------------------
# 구역 6. 개봉일 스크린수와 총 관객 (버블 그래프: 점 크기 = 첫 주 관객)
# ---------------------------------------------------------------
with st.container():
    st.header("6. 스크린수와 총 관객, 첫 주 관객까지 (버블 그래프)")

    bubble_df = df.dropna(subset=["first_scrn", "total_audi", "first_week_audi"])
    fig6 = px.scatter(
        bubble_df,
        x="first_scrn",
        y="total_audi",
        size="first_week_audi",
        color="genre",
        size_max=40,
        hover_name="movieNm",
        hover_data={
            "genre": True,
            "first_scrn": ":,",
            "total_audi": ":,",
            "first_week_audi": ":,",
        },
        labels={
            "first_scrn": "개봉일 스크린수(개)",
            "total_audi": "총 관객(명)",
            "first_week_audi": "개봉 첫 주 관객(명)",
            "genre": "장르",
        },
    )
    fig6.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="white")))
    st.plotly_chart(fig6, use_container_width=True)
    st.caption("점(버블)이 클수록 개봉 첫 주 관객이 많아요.")

    INSIGHT_6 = ""  # 예: "첫 주 관객이 많은 영화(큰 버블)일수록 총 관객도 많은 편이다."
    insight_box(INSIGHT_6)

st.divider()

# 다음 그래프는 위와 같은 형식으로 아래에 구역을 추가하면 돼요.
