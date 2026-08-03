from datetime import datetime  
import streamlit as st  
from supabase import create_client, Client

# =================================================================  
# [수정 부분] Supabase 연결 설정  
# 실제 배포 시에는 st.secrets["SUPABASE_URL"] 형태로 사용하시길 권장합니다.  
SUPABASE_URL = st.secrets["supabase_url"]  
SUPABASE_KEY = st.secrets["supabase_key"] 
# =================================================================

# Supabase 클라이언트 초기화  
@st.cache_resource # 매번 연결하지 않고 세션 동안 유지  
def init_supabase():  
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()  
TABLE_NAME = "xave_diary"

# 1. 데이터 불러오기 함수 (JSON 파일 -> Supabase Table)  
def load_posts():  
    try:  
        # xave_diary 테이블에서 모든 데이터를 가져오되, created_at 기준으로 내림차순 정렬  
        response = supabase.table(TABLE_NAME).select("*").order("created_at", desc=True).execute()  
        return response.data  
    except Exception as e:  
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")  
        return []

# 2. 데이터 저장하기 함수 (JSON 파일 쓰기 -> Supabase Insert)  
def save_post(title, content):  
    try:  
        # Supabase는 id와 created_at을 자동 생성하도록 설정했다면 title과 content만 넣으면 됩니다.  
        data = {"title": title, "content": content}  
        supabase.table(TABLE_NAME).insert(data).execute()  
        return True  
    except Exception as e:  
        st.error(f"저장 중 오류 발생: {e}")  
        return False

# 3. 데이터 삭제하기 함수 (리스트 pop -> Supabase Delete)  
def delete_post(post_id):  
    try:  
        # id 컬럼을 기준으로 해당 행을 삭제  
        supabase.table(TABLE_NAME).delete().eq("id", post_id).execute()  
        return True  
    except Exception as e:  
        st.error(f"삭제 중 오류 발생: {e}")  
        return False

# 비밀번호 가져오기 (기존과 동일)  
def get_delete_password():  
    if "DELETE_PASSWORD" in st.secrets:  
        return str(st.secrets["DELETE_PASSWORD"])  
    return os.environ.get("DELETE_PASSWORD", "")

# 페이지 기본 설정  
st.set_page_config(page_title="Supabase 기반 메모장", layout="wide")

# 데이터 초기화 (이제 session_state 대신 실시간으로 DB에서 불러오거나 캐싱합니다)  
# 실시간성을 위해 매번 load_posts()를 호출하거나, 버튼 클릭 시 갱신합니다.

# 4. 글작성 팝업 창(Dialog)  
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
                if save_post(title, content):  
                    st.success("저장되었습니다!")  
                    st.rerun()  
    with col2:  
        if st.button("취소", use_container_width=True):  
            st.rerun()

# 5. 글 삭제 비밀번호 확인 팝업 창(Dialog)  
@st.dialog("게시글 삭제")  
def delete_dialog(post_id):  
    st.write("게시글을 삭제하려면 비밀번호를 입력하세요.")  
    password_input = st.text_input("비밀번호", type="password")

    col1, col2 = st.columns([1, 1])  
    with col1:  
        if st.button("삭제 확인", type="primary", use_container_width=True):  
            if password_input == get_delete_password():  
                if delete_post(post_id):  
                    st.success("삭제되었습니다.")  
                    st.rerun()  
            else:  
                st.error("비밀번호가 일치하지 않습니다.")  
    with col2:  
        if st.button("취소", use_container_width=True):  
            st.rerun()

# 6. 메인 화면 구성  
st.title("📋 Xave Diary (Cloud)")

col_title, col_btn = st.columns([8, 2])  
with col_btn:  
    if st.button("➕ 새 글 작성", type="primary", use_container_width=True):  
        write_dialog()

st.divider()

# 7. 게시글 목록 표시  
posts = load_posts() # DB에서 최신 데이터 로드

if posts:  
    for post in posts:  
        # Supabase의 컬럼명에 맞춰 수정 (id, created_at, title, content)  
        col_content, col_del = st.columns([9, 1])

        with col_content:  
            # created_at을 읽기 좋은 포맷으로 변환  
            date_str = post['created_at'][:16].replace('T', ' ')   
            with st.expander(f"📌 **[{date_str}]** {post['title']}"):  
                st.markdown(f"**작성일시:** {post['created_at']}")  
                st.write("---")  
                st.write(post["content"])

        with col_del:  
            # post['id']를 전달하여 정확한 행을 삭제하도록 함  
            if st.button("🗑️ 삭제", key=f"del_{post['id']}", use_container_width=True):  
                delete_dialog(post['id'])  
else:  
    st.info("등록된 게시글이 없습니다. 상단의 작성 버튼을 눌러 글을 추가해보세요!")  
