from datetime import datetime
import json
import os
import pandas as pd
import streamlit as st

# JSON 파일 경로 설정
DATA_FILE = "posts.json"


# 1. 파일에서 데이터 불러오기 함수
def load_posts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


# 2. 파일에 데이터 저장하기 함수
def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)


# 페이지 기본 설정
st.set_page_config(page_title="JSON 기반 메모장", layout="wide")

# 3. 데이터 초기화 (앱 시작 시 JSON 파일에서 읽어옴)
if "posts" not in st.session_state:
    st.session_state.posts = load_posts()


# 4. 글작성 팝업 창(Dialog) 정의
@st.dialog("새 글 작성하기")
def write_dialog():
    title = st.text_input("제목", placeholder="제목을 입력하세요")
    content = st.text_area("내용", placeholder="내용을 입력하세요", height=150)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("저장", type="primary", use_container_width=True):
            if not title.strip():
                st.warning("제목을 입력해주세요.")
            else:
                # 현재 날짜 및 시간 기록
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

                # 데이터 추가 (최신글이 위로 오도록 맨 앞에 추가)
                new_post = {"작성일": now_str, "제목": title, "내용": content}
                st.session_state.posts.insert(0, new_post)

                # 파일에 영구 저장
                save_posts(st.session_state.posts)

                # 다이얼로그 닫고 화면 갱신
                st.rerun()

    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()


# 5. 메인 화면 구성
st.title("📋 Dairy")

# 상단 작성 버튼 영역
col_title, col_btn = st.columns([8, 2])
with col_btn:
    if st.button("➕ 새 글 작성", type="primary", use_container_width=True):
        write_dialog()

st.divider()

# 6. 입력된 이력을 Table 형식으로 표시
if st.session_state.posts:
    df = pd.DataFrame(st.session_state.posts)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "작성일": st.column_config.TextColumn("작성일시", width="medium"),
            "제목": st.column_config.TextColumn("제목", width="large"),
            "내용": st.column_config.TextColumn("내용", width="max"),
        },
    )
else:
    st.info("등록된 게시글이 없습니다. 상단의 작성 버튼을 눌러 글을 추가해보세요!")