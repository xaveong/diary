from datetime import datetime
import json
import os
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


# 비밀번호 가져오기 (st.secrets 또는 환경 변수 fallback)
def get_delete_password():
    # 1. Streamlit secrets에서 확인 (.streamlit/secrets.toml)
    if "DELETE_PASSWORD" in st.secrets:
        return str(st.secrets["DELETE_PASSWORD"])
    # 2. OS 환경 변수에서 확인
    return os.environ.get("DELETE_PASSWORD", "")


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



# 5. 글 삭제 비밀번호 확인 팝업 창(Dialog) 정의
@st.dialog("게시글 삭제")
def delete_dialog(target_idx):
    st.write("게시글을 삭제하려면 비밀번호를 입력하세요.")
    password_input = st.text_input("비밀번호", type="password")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("삭제 확인", type="primary", use_container_width=True):
            correct_password = get_delete_password()

            if password_input == correct_password:
                # 리스트에서 해당 게시글 제거
                st.session_state.posts.pop(target_idx)
                # JSON 파일 업데이트
                save_posts(st.session_state.posts)
                st.success("삭제되었습니다.")
                st.rerun()
            else:
                st.error("비밀번호가 일치하지 않습니다.")

    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()


# 6. 메인 화면 구성

st.title("📋 Xave Diary")

# 상단 작성 버튼 영역
col_title, col_btn = st.columns([8, 2])
with col_btn:
    if st.button("➕ 새 글 작성", type="primary", use_container_width=True):
        write_dialog()

st.divider()

<<<<<<< HEAD
# 6. 게시글 목록 및 삭제 기능
if st.session_state.posts:
    for idx, post in enumerate(st.session_state.posts):
        # 목록 영역(9)과 삭제 버튼 영역(1)을 분리
        col_content, col_del = st.columns([9, 1])

        with col_content:
            # 제목 클릭 시 열리는 아코디언 형태
=======
# 7. 게시글 목록 및 삭제 기능
if st.session_state.posts:
    for idx, post in enumerate(st.session_state.posts):
        col_content, col_del = st.columns([9, 1])

        with col_content:
>>>>>>> d544ae4 (삭제 추가)
            with st.expander(f"📌 **[{post['작성일']}]** {post['제목']}"):
                st.markdown(f"**작성일시:** {post['작성일']}")
                st.write("---")
                st.write(post["내용"])

        with col_del:
<<<<<<< HEAD
            # 게시글 삭제 버튼 (각 항목별 고유 key 지정 필수)
            if st.button("🗑️ 삭제", key=f"del_{idx}", use_container_width=True):
                # 리스트에서 해당 게시글 제거
                st.session_state.posts.pop(idx)
                # JSON 파일 업데이트
                save_posts(st.session_state.posts)
                # 화면 갱신
                st.rerun()
=======
            # 삭제 버튼 클릭 시 비밀번호 확인 Dialog 호출
            if st.button("🗑️ 삭제", key=f"del_{idx}", use_container_width=True):
                delete_dialog(idx)
>>>>>>> d544ae4 (삭제 추가)
else:
    st.info("등록된 게시글이 없습니다. 상단의 작성 버튼을 눌러 글을 추가해보세요!")
