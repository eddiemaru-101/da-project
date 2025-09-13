import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
from matplotlib import rcParams
import warnings
import os
from datetime import datetime

warnings.filterwarnings('ignore')

# 페이지 설정
st.set_page_config(
    page_title="따릉이 & 외국인 관광객 데이터 분석",
    page_icon="🚴‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 한글 폰트 설정 함수
@st.cache_resource
def setup_korean_font():
    font_paths = [
        r'C:\Windows\Fonts\malgun.ttf',
        r'C:\Windows\Fonts\gulim.ttc',
        r'C:\Windows\Fonts\batang.ttc'
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                korean_font = fm.FontProperties(fname=font_path)
                fm.fontManager.addfont(font_path)
                plt.rcParams['font.family'] = korean_font.get_name()
                plt.rcParams['axes.unicode_minus'] = False
                return korean_font
            except:
                continue

    try:
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        return None
    except:
        return None

# 한글 폰트 설정
korean_font_prop = setup_korean_font()
sns.set_style("whitegrid")

# 메인 함수
def main():
    st.title("🚴‍♂️ 따릉이 & 외국인 관광객 데이터 분석 대시보드")
    st.markdown("---")

    # 사이드바
    st.sidebar.title("📋 분석 메뉴")
    page = st.sidebar.selectbox("분석 페이지 선택", [
        "📊 개요",
        "🚴‍♂️ 01. 외국인 따릉이 이용패턴",
        "📈 02. 전체 따릉이 중 외국인 비중",
        "🗺️ 03. 외국인 대여반납 장소패턴",
        "🏆 04. 전체 따릉이 이용객 반납장소",
        "🌏 05. 해외관광객 추이분석"
    ])

    # 페이지별 라우팅
    if page == "📊 개요":
        show_overview()
    elif page == "🚴‍♂️ 01. 외국인 따릉이 이용패턴":
        show_foreign_usage_pattern()
    elif page == "📈 02. 전체 따릉이 중 외국인 비중":
        show_foreign_ratio()
    elif page == "🗺️ 03. 외국인 대여반납 장소패턴":
        show_foreign_station_pattern()
    elif page == "🏆 04. 전체 따릉이 이용객 반납장소":
        show_all_users_pattern()
    elif page == "🌏 05. 해외관광객 추이분석":
        show_tourist_trend()

def show_overview():
    st.header("📊 분석 개요")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("분석 기간", "2021년 ~ 2024년", "4년간")

    with col2:
        st.metric("분석 대상", "따릉이 + 관광객", "통합 분석")

    with col3:
        st.metric("주요 지표", "이용패턴/장소/추이", "다각도 분석")

    st.markdown("### 🎯 분석 목표")
    st.markdown("""
    **🚴‍♂️ 따릉이 분석:**
    - 외국인 관광객의 따릉이 이용 패턴 분석
    - 연도별, 월별, 요일별 이용량 추이
    - 대여/반납 장소별 선호도 분석
    - 전체 이용자 중 외국인 비중 변화

    **🌏 관광객 분석:**
    - 2010-2024년 외국인 방문객 장기 추세
    - 연령대별, 성별, 대륙별 변화 분석
    - 코로나19 전후 회복 패턴 분석
    """)

    st.markdown("### 📈 주요 인사이트 미리보기")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        **🚴‍♂️ 따릉이 이용 급증**
        - 2021년 19,049건 → 2024년 71,077건
        - 여의나루역이 4년 연속 1위
        - 주말 이용량이 평일의 1.3배
        """)

    with col2:
        st.info("""
        **🌏 관광객 완전 회복**
        - 2024년 1,637만명 (역대 2위)
        - 아시아주 80.1% 압도적 비중
        - 여성 관광객 지속적 우세 (56.5%)
        """)

def show_foreign_usage_pattern():
    st.header("🚴‍♂️ 외국인 따릉이 이용패턴 분석")

    # 연도별 이용량 데이터
    annual_data = {2021: 19049, 2022: 50761, 2023: 64342, 2024: 71077}

    # 월별 이용량 데이터
    monthly_data = {
        2022: [518, 566, 1570, 4838, 6350, 5735, 5640, 4198, 7278, 7154, 5981, 933],
        2023: [502, 783, 2473, 3775, 5325, 9562, 6392, 6560, 9621, 11592, 5689, 2068],
        2024: [1403, 2043, 5959, 10403, 9390, 10103, 6602, 5091, 7271, 7108, 4296, 1408]
    }

    # 요일별 이용량 데이터
    weekday_data = {
        '월요일': [6156, 9297, 9654],
        '화요일': [6343, 8039, 8637],
        '수요일': [6207, 7600, 8930],
        '목요일': [5973, 7621, 9208],
        '금요일': [7252, 9208, 9995],
        '토요일': [9502, 10686, 11758],
        '일요일': [9328, 11891, 12895]
    }

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("2024년 총 이용", "71,077건", "+10.5%")

    with col2:
        st.metric("4년간 증가율", "+273%", "2021년 대비")

    with col3:
        st.metric("최고 이용 요일", "일요일", "12,895건")

    with col4:
        st.metric("최고 이용 월", "4월", "10,403건")

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📈 연도별 추이", "🗓️ 월별 패턴", "📅 요일별 패턴"])

    with tab1:
        st.subheader("연도별 외국인 따릉이 이용량 증가 추이")

        col1, col2 = st.columns(2)

        with col1:
            # 연도별 이용량
            fig, ax = plt.subplots(figsize=(10, 6))
            years = list(annual_data.keys())
            counts = list(annual_data.values())

            bars = ax.bar(years, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            ax.set_title('연도별 외국인 관광객 따릉이 대여건수',
                        fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            ax.set_xlabel('연도', fontproperties=korean_font_prop)
            ax.set_ylabel('총 대여건수', fontproperties=korean_font_prop)

            for bar, count in zip(bars, counts):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01,
                       f'{count:,}', ha='center', va='bottom', fontweight='bold')

            st.pyplot(fig)

        with col2:
            # 증가율
            growth_rates = []
            growth_years = []
            for i in range(1, len(years)):
                growth_rate = ((counts[i] - counts[i-1]) / counts[i-1]) * 100
                growth_rates.append(growth_rate)
                growth_years.append(f"{years[i-1]}-{years[i]}")

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ['green' if rate >= 0 else 'red' for rate in growth_rates]
            bars = ax.bar(growth_years, growth_rates, color=colors, alpha=0.7)
            ax.set_title('연도별 증가율 (%)', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            ax.set_xlabel('연도', fontproperties=korean_font_prop)
            ax.set_ylabel('증가율 (%)', fontproperties=korean_font_prop)
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)

            for bar, rate in zip(bars, growth_rates):
                ax.text(bar.get_x() + bar.get_width()/2,
                       bar.get_height() + (5 if rate >= 0 else -10),
                       f'{rate:.1f}%', ha='center', va='bottom' if rate >= 0 else 'top',
                       fontweight='bold')

            st.pyplot(fig)

    with tab2:
        st.subheader("월별 외국인 따릉이 이용량 패턴 (2022-2024)")

        fig, ax = plt.subplots(figsize=(14, 8))
        months = range(1, 13)
        colors = ['#FF6B6B', '#4ECDC4', '#9B59B6']
        markers = ['o', 's', '^']

        for i, year in enumerate([2022, 2023, 2024]):
            values = monthly_data[year]
            ax.plot(months, values, marker=markers[i], linewidth=2.5,
                   markersize=8, color=colors[i], label=f'{year}년')

        ax.set_title('월별 외국인 관광객 따릉이 이용량 추이 (2022-2024)',
                    fontproperties=korean_font_prop, fontsize=16, fontweight='bold')
        ax.set_xlabel('월', fontproperties=korean_font_prop, fontsize=12)
        ax.set_ylabel('총 대여건수', fontproperties=korean_font_prop, fontsize=12)
        ax.set_xticks(months)
        legend = ax.legend(fontsize=12)
        if korean_font_prop:
            for text in legend.get_texts():
                text.set_fontproperties(korean_font_prop)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        # 월별 패턴 인사이트
        st.markdown("### 📊 월별 패턴 분석")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("**🌸 봄철 급증**  \n3-5월 이용량 급증  \n관광 성수기 효과")

        with col2:
            st.warning("**☀️ 여름철 변동**  \n6-8월 불규칙  \n날씨 영향 큼")

        with col3:
            st.success("**🍂 가을철 안정**  \n9-10월 꾸준한 이용  \n관광 최적기")

    with tab3:
        st.subheader("요일별 외국인 따릉이 이용량 패턴")

        # 요일별 데이터 시각화
        weekdays = list(weekday_data.keys())
        years = [2022, 2023, 2024]

        col1, col2 = st.columns(2)

        with col1:
            # 요일별 라인 차트
            fig, ax = plt.subplots(figsize=(12, 8))

            for i, year in enumerate(years):
                values = [weekday_data[day][i] for day in weekdays]
                ax.plot(weekdays, values, marker='o', linewidth=2.5,
                       markersize=6, color=colors[i], label=f'{year}년')

            ax.set_title('요일별 이용량 추이', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            ax.set_xlabel('요일', fontproperties=korean_font_prop)
            ax.set_ylabel('총 대여건수', fontproperties=korean_font_prop)

            if korean_font_prop:
                ax.set_xticklabels(weekdays, fontproperties=korean_font_prop)

            plt.xticks(rotation=45)
            legend = ax.legend()
            if korean_font_prop:
                for text in legend.get_texts():
                    text.set_fontproperties(korean_font_prop)
            ax.grid(True, alpha=0.3)

            st.pyplot(fig)

        with col2:
            # 평일 vs 주말 비교
            weekday_avg = np.mean([np.mean([weekday_data[day][i] for day in weekdays[:5]]) for i in range(3)])
            weekend_avg = np.mean([np.mean([weekday_data[day][i] for day in weekdays[5:]]) for i in range(3)])

            fig, ax = plt.subplots(figsize=(8, 6))
            categories = ['평일', '주말']
            values = [weekday_avg, weekend_avg]

            bars = ax.bar(categories, values, color=['#4ECDC4', '#FF6B6B'], alpha=0.8)
            ax.set_title('평일 vs 주말 평균 이용량', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            ax.set_ylabel('평균 대여건수', fontproperties=korean_font_prop)

            if korean_font_prop:
                ax.set_xticklabels(categories, fontproperties=korean_font_prop)

            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.02,
                       f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')

            st.pyplot(fig)

        # 요일별 인사이트
        st.markdown("### 📊 요일별 패턴 분석")
        col1, col2 = st.columns(2)

        with col1:
            st.success(f"**🎯 최고 이용 요일: 일요일**  \n2024년 평균 12,895건  \n여가 목적 이용 집중")

        with col2:
            st.info(f"**📈 주말 vs 평일 비율**  \n주말이 평일보다 1.3배 높음  \n관광 목적 이용 특성")

def show_foreign_ratio():
    st.header("📈 전체 따릉이 이용자 중 외국인 비중 분석")

    # 데이터
    years = [2022, 2023, 2024]
    foreign_counts = [50761, 64342, 71077]
    general_counts = [40950756, 44904665, 43849559]
    total_counts = [41001517, 44969007, 43920636]
    foreign_ratios = [0.124, 0.143, 0.162]

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("2024년 외국인 비율", "0.162%", "+0.038%p")

    with col2:
        st.metric("2024년 외국인 이용", "71,077건", "+40.0%")

    with col3:
        st.metric("연평균 증가율", "14.3%", "2022-2024")

    with col4:
        st.metric("3년간 평균 비율", "0.143%", "소수지만 성장")

    # 시각화
    col1, col2 = st.columns(2)

    with col1:
        # 연도별 이용자 구성 (스택 바 차트)
        fig, ax = plt.subplots(figsize=(10, 8))
        width = 0.6

        p1 = ax.bar(years, [count/1000000 for count in general_counts], width,
                   label='일반 이용자', color='#4ECDC4', alpha=0.8)
        p2 = ax.bar(years, [count/1000000 for count in foreign_counts], width,
                   bottom=[count/1000000 for count in general_counts],
                   label='외국인 이용자', color='#FF6B6B', alpha=0.8)

        ax.set_title('연도별 따릉이 이용자 구성', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
        ax.set_xlabel('연도', fontproperties=korean_font_prop)
        ax.set_ylabel('총 이용건수 (백만건)', fontproperties=korean_font_prop)
        legend = ax.legend()
        if korean_font_prop:
            for text in legend.get_texts():
                text.set_fontproperties(korean_font_prop)

        # 총 이용건수 텍스트 추가
        for i, year in enumerate(years):
            total = (general_counts[i] + foreign_counts[i]) / 1000000
            ax.text(year, total + 2, f'{total:.1f}M', ha='center', va='bottom', fontweight='bold')

        st.pyplot(fig)

    with col2:
        # 외국인 비율 추이
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.plot(years, foreign_ratios, marker='o', linewidth=3, markersize=8, color='#FF6B6B')
        ax.set_title('연도별 외국인 이용자 비율 추이', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
        ax.set_xlabel('연도', fontproperties=korean_font_prop)
        ax.set_ylabel('외국인 비율 (%)', fontproperties=korean_font_prop)
        ax.grid(True, alpha=0.3)

        # 비율 수치 표시
        for i, (year, ratio) in enumerate(zip(years, foreign_ratios)):
            ax.text(year, ratio + max(foreign_ratios) * 0.05, f'{ratio:.3f}%',
                   ha='center', va='bottom', fontweight='bold')

        st.pyplot(fig)

    # 3년간 총합 파이 차트
    st.subheader("3년간(2022-2024) 전체 이용자 구성")

    total_foreign = sum(foreign_counts)
    total_general = sum(general_counts)
    total_all = total_foreign + total_general

    fig, ax = plt.subplots(figsize=(10, 8))
    sizes = [total_general, total_foreign]
    labels = ['일반 이용자', '외국인 이용자']
    colors = ['#4ECDC4', '#FF6B6B']
    explode = (0, 0.1)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                     autopct='%1.3f%%', shadow=True, startangle=90)

    if korean_font_prop:
        for text in texts:
            text.set_fontproperties(korean_font_prop)
        for autotext in autotexts:
            autotext.set_fontproperties(korean_font_prop)

    ax.set_title('3년간 전체 이용자 구성 (2022-2024)',
                fontproperties=korean_font_prop, fontsize=14, fontweight='bold')

    st.pyplot(fig)

    # 통계 요약
    st.markdown("### 📊 주요 통계")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**전체 이용건수**  \n{total_all:,}건")

    with col2:
        st.success(f"**일반 이용자**  \n{total_general:,}건  \n({(total_general/total_all)*100:.3f}%)")

    with col3:
        st.warning(f"**외국인 이용자**  \n{total_foreign:,}건  \n({(total_foreign/total_all)*100:.3f}%)")

def show_foreign_station_pattern():
    st.header("🗺️ 외국인 대여반납 장소패턴 분석")

    # 연도별 TOP 5 대여 장소 데이터
    yearly_rental_top5 = {
        2021: [
            ("207. 여의나루역 1번출구 앞", 587),
            ("502. 뚝섬유원지역 1번출구 앞", 290),
            ("2262. 한신16차아파트 119동 앞", 215),
            ("3010.홍대입구역 3번출구", 183),
            ("272. 당산육갑문", 179)
        ],
        2022: [
            ("207. 여의나루역 1번출구 앞", 1823),
            ("502. 뚝섬유원지역 1번출구 앞", 666),
            ("4217. 한강공원 망원나들목", 661),
            ("3515. 서울숲 관리사무소", 562),
            ("2262. 한신16차아파트 119동 앞", 559)
        ],
        2023: [
            ("207. 여의나루역 1번출구 앞", 2236),
            ("3515. 서울숲 관리사무소", 922),
            ("2262. 한신16차아파트 119동 앞", 850),
            ("249. 여의도중학교 옆", 724),
            ("502. 뚝섬유원지역 1번출구 앞", 724)
        ],
        2024: [
            ("207. 여의나루역 1번출구 앞", 1990),
            ("4217. 한강공원 망원나들목", 1114),
            ("3515. 서울숲 관리사무소", 1109),
            ("502. 자양(뚝섬한강공원)역 1번출구 앞", 857),
            ("474.동대문역사문화공원역 1번출구 뒤편", 651)
        ]
    }

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("4년 연속 1위", "여의나루역", "한강공원 최고 인기")

    with col2:
        st.metric("2024년 1위 이용량", "1,990건", "역대 2위")

    with col3:
        st.metric("신규 급성장", "자양역", "+857건 (신규)")

    with col4:
        st.metric("지속 인기", "서울숲", "3년 TOP5")

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["📈 연도별 순위", "🚀 급성장 분석", "🎯 관광 코스 예측"])

    with tab1:
        st.subheader("연도별 외국인 대여 TOP 5 장소")

        # 연도별 비교
        for year in [2021, 2022, 2023, 2024]:
            st.markdown(f"**{year}년 TOP 5:**")
            data = yearly_rental_top5[year]

            col1, col2 = st.columns([3, 1])
            with col1:
                for i, (station, count) in enumerate(data):
                    emoji = "🏆" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}️⃣"
                    short_name = station[:30] + "..." if len(station) > 30 else station
                    st.write(f"{emoji} {short_name}")

            with col2:
                for i, (station, count) in enumerate(data):
                    st.write(f"{count:,}건")

            st.markdown("---")

    with tab2:
        st.subheader("2023→2024년 급성장 대여소 분석")

        # 급성장 TOP 10 데이터
        growth_data = [
            ("502. 자양(뚝섬한강공원)역 1번출구 앞", 0, 857, "신규 등장"),
            ("4217. 한강공원 망원나들목", 724, 1114, "+53.9%"),
            ("5870. LG트윈타워 앞", 265, 499, "+88.3%"),
            ("2217.아크로리버뷰 부지 앞", 134, 365, "+172.4%"),
            ("3552.서울숲 공영주차장앞", 373, 582, "+56.0%"),
            ("302. 경복궁역 6번출구 뒤", 0, 190, "신규 등장"),
            ("3515. 서울숲 관리사무소", 922, 1109, "+20.3%"),
            ("4244. 당인리발전소 공원 앞", 160, 313, "+95.6%"),
            ("2525.반포쇼핑타운 2동 앞", 448, 596, "+33.0%"),
            ("3559.성동구민종합체육센터 앞", 216, 356, "+64.8%")
        ]

        # 급성장 대여소 시각화
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # 증가량 TOP 5
        top5_growth = growth_data[:5]
        names = [item[0][:20] + "..." for item in top5_growth]
        growth_amounts = [item[2] - item[1] for item in top5_growth]

        bars1 = ax1.barh(range(len(names)), growth_amounts, color='#E74C3C', alpha=0.8)
        ax1.set_yticks(range(len(names)))
        if korean_font_prop:
            ax1.set_yticklabels(names, fontproperties=korean_font_prop, fontsize=10)
        ax1.set_xlabel('증가량 (건)', fontproperties=korean_font_prop)
        ax1.set_title('2023→2024 급성장 대여소 TOP 5', fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
        ax1.invert_yaxis()

        for i, (bar, value) in enumerate(zip(bars1, growth_amounts)):
            ax1.text(bar.get_width() + max(growth_amounts) * 0.02,
                    bar.get_y() + bar.get_height()/2,
                    f'+{int(value)}', ha='left', va='center', fontweight='bold')

        # 2023 vs 2024 비교
        x = np.arange(len(top5_growth))
        width = 0.35

        values_2023 = [item[1] for item in top5_growth]
        values_2024 = [item[2] for item in top5_growth]

        bars2 = ax2.bar(x - width/2, values_2023, width, label='2023년', color='#3498DB', alpha=0.8)
        bars3 = ax2.bar(x + width/2, values_2024, width, label='2024년', color='#E74C3C', alpha=0.8)

        ax2.set_xlabel('대여소', fontproperties=korean_font_prop)
        ax2.set_ylabel('대여건수', fontproperties=korean_font_prop)
        ax2.set_title('급성장 상위 5개 대여소 비교', fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        if korean_font_prop:
            ax2.set_xticklabels([name[:10] + "..." for name in names],
                               rotation=45, ha='right', fontproperties=korean_font_prop, fontsize=8)
        legend = ax2.legend()
        if korean_font_prop:
            for text in legend.get_texts():
                text.set_fontproperties(korean_font_prop)

        st.pyplot(fig)

        # 급성장 특징 분석
        st.markdown("### 🚀 급성장 대여소 특징")
        col1, col2 = st.columns(2)

        with col1:
            st.success("""
            **신규 등장 대여소**
            - 자양(뚝섬한강공원)역: 857건
            - 경복궁역 6번출구: 190건
            - 한강공원/관광지 인근 집중
            """)

        with col2:
            st.info("""
            **기존 대여소 급성장**
            - 아크로리버뷰: +172.4%
            - 당인리발전소 공원: +95.6%
            - 한강/공원 지역 성장세
            """)

    with tab3:
        st.subheader("외국인 관광 코스 예측 분석")

        # 2024년 대여/반납 TOP 5 비교
        rental_top5_2024 = [
            "207. 여의나루역 1번출구 앞",
            "4217. 한강공원 망원나들목",
            "3515. 서울숲 관리사무소",
            "502. 자양(뚝섬한강공원)역 1번출구 앞",
            "474.동대문역사문화공원역 1번출구 뒤편"
        ]

        return_top5_2024 = [
            "207. 여의나루역 1번출구 앞",
            "4217. 한강공원 망원나들목",
            "502. 자양(뚝섬한강공원)역 1번출구 앞",
            "2525.반포쇼핑타운 2동 앞",
            "3515. 서울숲 관리사무소"
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🚀 주요 대여 출발지 TOP 5**")
            for i, station in enumerate(rental_top5_2024):
                emoji = "🏆" if i == 0 else f"{i+1}️⃣"
                short_name = station[:25] + "..." if len(station) > 25 else station
                st.write(f"{emoji} {short_name}")

        with col2:
            st.markdown("**🏁 주요 반납 도착지 TOP 5**")
            for i, station in enumerate(return_top5_2024):
                emoji = "🏆" if i == 0 else f"{i+1}️⃣"
                short_name = station[:25] + "..." if len(station) > 25 else station
                st.write(f"{emoji} {short_name}")

        # 공통 장소 분석
        common_stations = set(rental_top5_2024) & set(return_top5_2024)

        st.markdown("### 🔄 대여/반납 공통 상위 장소")
        st.success(f"**{len(common_stations)}곳이 대여/반납 모두 TOP 5**")

        for station in common_stations:
            short_name = station[:40] + "..." if len(station) > 40 else station
            st.write(f"• {short_name}")

        # 관광 코스 예측
        st.markdown("### 🎯 추정 관광 코스 패턴")

        col1, col2 = st.columns(2)

        with col1:
            st.info("""
            **🚴‍♂️ 순환형 코스**
            - 여의나루역 ↔ 한강공원
            - 서울숲 ↔ 뚝섬한강공원
            - 같은 지역 내 순환 이용
            """)

        with col2:
            st.warning("""
            **🚶‍♂️ 이동형 코스**
            - 동대문 → 반포쇼핑타운
            - 지역 간 이동형 관광
            - 지하철 연계 이용
            """)

def show_all_users_pattern():
    st.header("🏆 전체 따릉이 이용객 반납장소 패턴")

    # TOP5 대여소 정보
    top5_stations = {
        '207': '여의나루역 1번출구 앞',
        '4217': '한강공원 망원나들목',
        '3515': '서울숲 관리사무소',
        '502': '자양(뚝섬한강공원)역 1번출구 앞',
        '474': '동대문역사문화공원역 1번출구 뒤편'
    }

    # 6개월 데이터 결과
    results = {
        '207': {'total': 50175, 'same_ratio': 21.4, 'pattern': '이동형'},
        '4217': {'total': 73751, 'same_ratio': 25.4, 'pattern': '이동형'},
        '3515': {'total': 15745, 'same_ratio': 35.1, 'pattern': '이동형'},
        '502': {'total': 73157, 'same_ratio': 22.7, 'pattern': '이동형'},
        '474': {'total': 13947, 'same_ratio': 7.9, 'pattern': '이동형'}
    }

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("분석 대상", "TOP 5 대여소", "6개월 데이터")

    with col2:
        st.metric("총 분석 건수", "226,775건", "전체 이용 패턴")

    with col3:
        st.metric("최고 이용", "한강공원 망원나들목", "73,751건")

    with col4:
        st.metric("패턴 결과", "모두 이동형", "교통수단 활용")

    # 대여소별 분석 결과
    st.subheader("TOP 5 대여소별 반납 패턴 분석")

    # 동일지점 반납 비율 시각화
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # 동일지점 반납 비율
    stations = [f"{station_id}번\n{name[:10]}..." for station_id, name in top5_stations.items()]
    ratios = [results[station_id]['same_ratio'] for station_id in top5_stations.keys()]
    colors = ['#FF6B6B' if ratio < 30 else '#FFA500' if ratio < 50 else '#4ECDC4' for ratio in ratios]

    bars1 = ax1.bar(range(len(stations)), ratios, color=colors, alpha=0.8)
    ax1.set_title('대여소별 동일지점 반납 비율', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
    ax1.set_ylabel('동일지점 반납 비율 (%)', fontproperties=korean_font_prop)
    ax1.set_xticks(range(len(stations)))
    if korean_font_prop:
        ax1.set_xticklabels(stations, fontproperties=korean_font_prop, rotation=45, ha='right')

    # 패턴 기준선
    ax1.axhline(y=30, color='orange', linestyle='--', alpha=0.7, label='이동형 기준 (30%)')
    ax1.axhline(y=50, color='green', linestyle='--', alpha=0.7, label='혼합형 기준 (50%)')

    for bar, ratio in zip(bars1, ratios):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{ratio:.1f}%', ha='center', va='bottom', fontweight='bold')

    legend = ax1.legend()
    if korean_font_prop:
        for text in legend.get_texts():
            text.set_fontproperties(korean_font_prop)

    # 총 이용건수 비교
    totals = [results[station_id]['total'] for station_id in top5_stations.keys()]
    bars2 = ax2.bar(range(len(stations)), [total/1000 for total in totals],
                    color='#45B7D1', alpha=0.8)
    ax2.set_title('대여소별 총 이용건수 (6개월)', fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
    ax2.set_ylabel('총 이용건수 (천건)', fontproperties=korean_font_prop)
    ax2.set_xticks(range(len(stations)))
    if korean_font_prop:
        ax2.set_xticklabels(stations, fontproperties=korean_font_prop, rotation=45, ha='right')

    for bar, total in zip(bars2, totals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{total:,.0f}', ha='center', va='bottom', fontweight='bold')

    st.pyplot(fig)

    # 분석 결과 요약 테이블
    st.subheader("📋 분석 결과 요약")

    summary_data = []
    for station_id, station_name in top5_stations.items():
        data = results[station_id]
        summary_data.append({
            '대여소': f'{station_id}번 {station_name}',
            '총대여': f"{data['total']:,}건",
            '동일지점반납': f"{data['same_ratio']:.1f}%",
            '패턴': data['pattern']
        })

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)

    # 주요 인사이트
    st.subheader("🎯 주요 인사이트")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        **🚴 이동형 패턴 우세**
        - 모든 TOP5 대여소가 이동형
        - 동일지점 반납 7.9~35.1%
        - 따릉이 = 교통수단 활용
        """)

    with col2:
        st.info("""
        **📍 지역별 차이**
        - 서울숲: 35.1% (상대적 순환형)
        - 동대문: 7.9% (강한 이동형)
        - 관광지 특성에 따른 차이
        """)

    # 패턴 분류 기준
    st.markdown("### 📊 패턴 분류 기준")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.error("""
        **🚴 이동형**
        - 동일지점 반납 < 40%
        - 교통수단으로 활용
        - A지점 → B지점 이동
        """)

    with col2:
        st.warning("""
        **🔀 혼합형**
        - 동일지점 반납 40~70%
        - 이동 + 여가 혼합
        - 상황에 따라 다양한 이용
        """)

    with col3:
        st.success("""
        **🔄 순환형**
        - 동일지점 반납 > 70%
        - 여가/운동 목적
        - 출발지로 되돌아오는 이용
        """)

def show_tourist_trend():
    st.header("🌏 해외관광객 추이분석 (2010-2024)")

    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("2024년 총 방문객", "1,637만명", "역대 2위")

    with col2:
        st.metric("15년간 성장률", "+86.1%", "2010년 대비")

    with col3:
        st.metric("여성 방문객 비율", "56.5%", "2024년 기준")

    with col4:
        st.metric("아시아주 비중", "80.1%", "압도적 1위")

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["📈 연령대 분석", "🌏 대륙별 분석", "👫 성별 분석", "📊 장기 추세"])

    with tab1:
        st.subheader("2023-2024년 연령대별 분석")

        # 연령대별 데이터
        age_2023 = {'0-20세': 1141274, '21-30세': 2789771, '31-40세': 2267755,
                    '41-50세': 1617046, '51-60세': 1349707, '61세 이상': 1110580}
        age_2024 = {'0-20세': 1467487, '21-30세': 3966890, '31-40세': 3446258,
                    '41-50세': 2365782, '51-60세': 1957080, '61세 이상': 2024923}

        col1, col2 = st.columns(2)

        with col1:
            # 2023년 파이차트
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(age_2023.values(), labels=age_2023.keys(),
                                             autopct='%1.1f%%', startangle=90)
            for text in texts + autotexts:
                if korean_font_prop:
                    text.set_fontproperties(korean_font_prop)
            ax.set_title('2023년 외국인 방문객 연령대별 분포',
                        fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            st.pyplot(fig)

        with col2:
            # 2024년 파이차트
            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(age_2024.values(), labels=age_2024.keys(),
                                             autopct='%1.1f%%', startangle=90)
            for text in texts + autotexts:
                if korean_font_prop:
                    text.set_fontproperties(korean_font_prop)
            ax.set_title('2024년 외국인 방문객 연령대별 분포',
                        fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
            st.pyplot(fig)

        # 변화 분석
        st.markdown("### 📊 연령대별 변화 분석")

        age_change = {}
        for age_group in age_2023.keys():
            change = age_2024[age_group] - age_2023[age_group]
            change_rate = (change / age_2023[age_group]) * 100
            age_change[age_group] = {'변화량': change, '변화율(%)': change_rate}

        change_df = pd.DataFrame(age_change).T

        col1, col2 = st.columns(2)

        with col1:
            st.success("""
            **🎯 주요 증가 연령대**
            - 21-30세: +42.2% 증가
            - 31-40세: +52.0% 증가
            - 젊은 층 중심 증가
            """)

        with col2:
            st.info("""
            **📈 전체 증가율**
            - 전 연령대 증가
            - 총 48.4% 증가
            - 0-20세도 28.6% 증가
            """)

    with tab2:
        st.subheader("2023-2024년 대륙별 분석")

        # 대륙별 데이터
        continent_data = {
            '아시아주': {'2023': 8401391, '2024': 13113511},
            '미주': {'2023': 1373227, '2024': 1719511},
            '구주': {'2023': 918059, '2024': 1140953},
            '대양주': {'2023': 240864, '2024': 289685},
            '아프리카': {'2023': 57253, '2024': 70758},
            '교포': {'2023': 40663, '2024': 34989}
        }

        col1, col2 = st.columns(2)

        with col1:
            # 2023년 분포
            fig, ax = plt.subplots(figsize=(8, 8))
            values_2023 = [continent_data[cont]['2023'] for cont in continent_data.keys()]
            wedges, texts, autotexts = ax.pie(values_2023, labels=continent_data.keys(),
                                             autopct='%1.1f%%', startangle=90)
            for text in texts + autotexts:
                if korean_font_prop:
                    text.set_fontproperties(korean_font_prop)
            ax.set_title('2023년 대륙별 외국인 방문객 분포',
                        fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
            st.pyplot(fig)

        with col2:
            # 2024년 분포
            fig, ax = plt.subplots(figsize=(8, 8))
            values_2024 = [continent_data[cont]['2024'] for cont in continent_data.keys()]
            wedges, texts, autotexts = ax.pie(values_2024, labels=continent_data.keys(),
                                             autopct='%1.1f%%', startangle=90)
            for text in texts + autotexts:
                if korean_font_prop:
                    text.set_fontproperties(korean_font_prop)
            ax.set_title('2024년 대륙별 외국인 방문객 분포',
                        fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
            st.pyplot(fig)

        # 대륙별 변화 분석
        st.markdown("### 🌏 대륙별 변화 분석")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("""
            **🚀 아시아주 급증**
            - 80.1% 압도적 비중
            - 56.1% 증가 (~470만명)
            - 중국 관광객 회복 주도
            """)

        with col2:
            st.info("""
            **📈 서구권 회복**
            - 구주(유럽): +24.3%
            - 미주: +25.2%
            - 대양주: +20.3%
            """)

        with col3:
            st.warning("""
            **📉 유일한 감소**
            - 해외동포: -13.9%
            - 코로나 영향 지속
            - 방문 목적 변화
            """)

    with tab3:
        st.subheader("2017-2024년 성별 분석")

        # 성별 데이터
        gender_data = {
            '2017': {'전체': 13335758, '남자': 5533199, '여자': 6806301, '여성비율': 51.0},
            '2018': {'전체': 15346879, '남자': 6229185, '여자': 8195792, '여성비율': 53.4},
            '2019': {'전체': 17502756, '남자': 6768303, '여자': 9695380, '여성비율': 55.4},
            '2020': {'전체': 2519118, '남자': 978594, '여자': 1156517, '여성비율': 45.9},
            '2021': {'전체': 967003, '남자': 335894, '여자': 196694, '여성비율': 20.3},
            '2022': {'전체': 3198017, '남자': 1403186, '여자': 1290033, '여성비율': 40.3},
            '2023': {'전체': 11031665, '남자': 4233401, '여자': 6042732, '여성비율': 54.8},
            '2024': {'전체': 16369629, '남자': 5979930, '여자': 9248490, '여성비율': 56.5}
        }

        years = list(gender_data.keys())
        total_visitors = [gender_data[year]['전체'] for year in years]
        female_ratios = [gender_data[year]['여성비율'] for year in years]

        col1, col2 = st.columns(2)

        with col1:
            # 전체 방문객 수 변화
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(years, [x/1000000 for x in total_visitors], marker='o', linewidth=2, markersize=8, color='blue')
            ax.set_title('2017-2024년 외국인 방문객 총 수 변화',
                        fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
            ax.set_ylabel('방문객 수 (백만명)', fontproperties=korean_font_prop)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            # 여성 비율 변화
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(years, female_ratios, marker='s', linewidth=2, markersize=6, color='red')
            ax.set_title('2017-2024년 여성 방문객 비율 변화',
                        fontproperties=korean_font_prop, fontsize=12, fontweight='bold')
            ax.set_ylabel('여성 비율 (%)', fontproperties=korean_font_prop)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 70)
            st.pyplot(fig)

        # 성별 분석 인사이트
        st.markdown("### 👫 성별 분석 인사이트")

        col1, col2 = st.columns(2)

        with col1:
            st.success("""
            **👩 여성 방문객 우세**
            - 8년 평균 57.5%
            - 2024년 56.5% 안정적
            - 지속적인 여성 우위
            """)

        with col2:
            st.info("""
            **📊 코로나19 영향**
            - 2020-2021년 급감
            - 2022년부터 회복
            - 2024년 완전 정상화
            """)

    with tab4:
        st.subheader("2010-2024년 장기 추세 분석")

        # 장기 데이터
        years_long = ['2010', '2011', '2012', '2013', '2014', '2015', '2016',
                     '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
        total_visitors_long = [8797658, 9794796, 11140028, 12175550, 14201516, 13231651,
                              17241823, 13335758, 15346879, 17502756, 2519118, 967003,
                              3198017, 11031665, 16369629]

        # 국가별 데이터
        countries_data = {
            '일본': [3023009, 3289051, 3518792, 2747750, 2280434, 1837782, 2297893,
                    2311447, 2948527, 3271706, 430742, 15265, 296867, 2316429, 3224079],
            '중국': [1875157, 2220196, 2836892, 4326869, 6126865, 5984170, 8067722,
                    4169353, 4789512, 6023021, 686430, 170215, 227358, 2019424, 4603273],
            '미국': [652889, 661503, 697866, 722315, 770305, 767613, 866186,
                    868881, 967992, 1044038, 220417, 204025, 543648, 1086415, 1320108]
        }

        # 전체 트렌드
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(years_long, [x/1000000 for x in total_visitors_long],
               marker='o', linewidth=3, markersize=8, color='darkblue')
        ax.set_title('2010-2024년 외국인 방문객 총 수 변화',
                    fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
        ax.set_ylabel('방문객 수 (백만명)', fontproperties=korean_font_prop)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

        # 주요 시점 표시
        ax.axvline(x='2019', color='green', linestyle='--', alpha=0.7)
        ax.text('2019', 18, '역대 최고', ha='center', fontproperties=korean_font_prop)
        ax.axvline(x='2020', color='red', linestyle='--', alpha=0.7)
        ax.text('2020', 15, 'COVID-19', ha='center', fontproperties=korean_font_prop)

        st.pyplot(fig)

        # 국가별 트렌드
        st.markdown("### 🌍 주요 국가별 변화")

        fig, ax = plt.subplots(figsize=(14, 8))
        colors = ['red', 'orange', 'blue']
        markers = ['o', 's', '^']

        for i, (country, data) in enumerate(countries_data.items()):
            ax.plot(years_long, [x/1000000 for x in data],
                   marker=markers[i], label=country, linewidth=2,
                   markersize=6, color=colors[i], alpha=0.8)

        ax.set_title('2010-2024년 주요 국가별 외국인 방문객 수 변화',
                    fontproperties=korean_font_prop, fontsize=14, fontweight='bold')
        ax.set_ylabel('방문객 수 (백만명)', fontproperties=korean_font_prop)
        ax.tick_params(axis='x', rotation=45)
        legend = ax.legend()
        if korean_font_prop:
            for text in legend.get_texts():
                text.set_fontproperties(korean_font_prop)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        # 15년간 변화 통계
        st.markdown("### 📈 15년간 주요 변화")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("2010년", "880만명", "시작점")
            st.metric("2019년", "1,750만명", "역대 최고")
            st.metric("2024년", "1,637만명", "회복 완료")

        with col2:
            st.success("""
            **🚀 중국 급증**
            - 2010년: 188만명
            - 2024년: 460만명
            - 145.5% 증가
            """)

        with col3:
            st.info("""
            **🇯🇵 일본 안정**
            - 2010년: 302만명
            - 2024년: 322만명
            - 안정적 유지
            """)

    # 종합 인사이트
    st.markdown("---")
    st.subheader("🎯 종합 분석 결과")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        **🚀 완전한 회복 달성**
        - 2024년 1,637만명 (역대 2위)
        - 코로나19 이전 수준 완전 회복
        - 아시아권 중심의 급속한 회복
        - 젊은 층(21-40세) 증가 두드러짐
        """)

    with col2:
        st.info("""
        **📊 지속적 특징**
        - 여성 관광객 비중 높음 (56.5%)
        - 아시아주 압도적 비중 (80.1%)
        - 중국 관광객 급속한 회복
        - 관광 시장 다변화 지속
        """)

if __name__ == "__main__":
    main()