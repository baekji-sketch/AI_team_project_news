import os
import time
import streamlit as st
from prompts import (
    build_initial_story_prompt,
    build_continuity_story_prompt,
    build_image_prompt,
)
from utils import (
    get_openai_api_key,
    generate_openai_text,
    generate_openai_image,
    initialize_session_state,
    render_typewriter_text,
)

st.set_page_config(
    page_title="IF : 다른 선택의 미래",
    page_icon="🪞",
    layout="wide",
)

PAGE_CSS = """
body {
    color: #eeeeff;
    background: radial-gradient(circle at top left, #0f172a 0%, #020617 45%, #020617 100%);
}
[data-testid="stSidebar"] {
    background: rgba(10, 14, 30, 0.9);
    color: #e2e8f0;
}
.css-1d391kg {
    background-color: rgba(255, 255, 255, 0.04);
}
.reportview-container .main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.card {
    border-radius: 24px;
    background: rgba(12, 18, 42, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.28);
    backdrop-filter: blur(18px);
    padding: 1.6rem;
}
.title-text {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.06em;
}
.subtitle-text {
    color: #94a3b8;
    margin-bottom: 1.75rem;
}
.stButton>button {
    border-radius: 999px;
    background: linear-gradient(135deg, #3b82f6, #9333ea);
    color: white;
    border: none;
}
.stButton>button:hover {
    opacity: 0.95;
}
"""

st.markdown(f"<style>{PAGE_CSS}</style>", unsafe_allow_html=True)

initialize_session_state()

with st.container():
    st.markdown("""
    <div class='card' style='padding: 2rem;'>
        <h1 class='title-text'>IF : 다른 선택의 미래</h1>
        <p class='subtitle-text'>당신이 선택하지 않은 과거 위에서 펼쳐지는 감성적이고 미래적인 평행세계 시뮬레이터.</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class='card'>
        <h3>평행 타임라인</h3>
        <p>각 선택은 새로운 우주를 만들어냅니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.text_input(
        "OpenAI API 키 입력",
        type="password",
        help="이 세션에서 사용할 OpenAI API 키를 입력하세요.",
        placeholder="sk-...",
        key="openai_api_key_input",
    )

    if st.session_state.story_history:
        for entry in st.session_state.story_history:
            st.markdown(f"**T+{entry['step'] * 10}년 — 나이 {entry['age']}**")
            st.markdown(f"_{entry['headline']}_")
            st.divider()
    else:
        st.markdown("_아직 생성된 평행 세계가 없습니다. 첫 번째 대체 선택을 시작하세요._")

with st.form(key="parallel_form"):
    with st.container():
        left, right = st.columns([2, 1])
        with left:
            alternate_choice = st.text_area(
                "대체 인생 선택",
                placeholder="예시: 중학교 때 축구 연습을 그만두었습니다.",
                height=140,
            )
            current_age = st.number_input(
                "현재 나이",
                min_value=12,
                max_value=90,
                value=24,
                step=1,
                help="현재 나이는 AI가 미래 타임라인을 구성하는 데 도움이 됩니다.",
            )
            personality = st.text_input(
                "성격 특징",
                placeholder="창의적, 감성적, 호기심 많음",
            )
            interests = st.text_input(
                "관심사",
                placeholder="스포츠, 게임, 음악",
            )
            reason = st.text_area(
                "그 길을 포기한 이유",
                placeholder="부모님의 압박, 실패에 대한 두려움, 가족을 부양해야 하는 상황",
                height=100,
            )
        with right:
            st.markdown("""
            <div class='card'>
                <h4>작동 방식</h4>
                <ul style='padding-left: 1rem; color: #cbd5e1;'>
                    <li>실제로 선택하지 않은 과거의 결정을 입력하세요.</li>
                    <li>미래 뉴스 헤드라인, 시네마틱 이미지, 기사를 생성합니다.</li>
                    <li>같은 우주에서 10년 후 이야기를 이어갑니다.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    generate_button = st.form_submit_button("평행 세계 생성")

if generate_button:
    if not alternate_choice.strip():
        st.error("선택하지 않은 대체 인생 선택을 입력해 주세요.")
    else:
        api_key = get_openai_api_key()
        if not api_key:
            st.error("OpenAI API 키가 없습니다. 환경 변수 또는 Streamlit secrets에 설정해 주세요.")
        else:
            with st.spinner("평행 우주를 시뮬레이션하는 중..."):
                prompt = build_initial_story_prompt(
                    alternate_choice,
                    int(current_age),
                    personality,
                    interests,
                    reason,
                )
                future_text = generate_openai_text(prompt)
                image_prompt = build_image_prompt(
                    alternate_choice,
                    int(current_age),
                    personality,
                    interests,
                )
                image_url = generate_openai_image(image_prompt)

            st.session_state.current_age = int(current_age)
            st.session_state.timeline_step = 0
            story_entry = {
                "step": 0,
                "age": int(current_age),
                "choice": alternate_choice,
                "personality": personality,
                "interests": interests,
                "reason": reason,
                "headline": future_text["headline"],
                "article": future_text["article"],
                "image_url": image_url,
            }
            st.session_state.story_history = [story_entry]
            st.session_state.current_story = story_entry

if st.session_state.get("current_story"):
    story = st.session_state.current_story
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='margin-bottom:0.3rem;'>📣 {story['headline']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#94a3b8; margin-top:0.2rem;'>나이 {story['age']} — {story['choice']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    image_col, article_col = st.columns([2, 3])
    with image_col:
        if story["image_url"]:
            st.image(story["image_url"], use_column_width=True, caption="대체 미래의 시네마틱한 순간")
        else:
            st.info("이미지 생성에 문제가 있습니다. OpenAI 이미지 API 액세스를 확인하세요.")
    with article_col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h4>미래 기사</h4>", unsafe_allow_html=True)
        render_typewriter_text(story["article"])
        st.download_button(
            label="기사 텍스트 다운로드",
            data=story["article"],
            file_name="if_alternate_life.txt",
            mime="text/plain",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    continue_col1, continue_col2 = st.columns([3, 1])
    with continue_col2:
        if st.button("이야기 계속하기 (+10년)"):
            if not st.session_state.get("current_story"):
                st.warning("먼저 평행 세계를 생성하세요.")
            else:
                api_key = get_openai_api_key()
                if not api_key:
                    st.error("OpenAI API 키가 없습니다. 환경 변수 또는 Streamlit secrets에 설정해 주세요.")
                else:
                    with st.spinner("같은 우주에서 타임라인을 10년 더 진행하는 중..."):
                        previous = st.session_state.current_story
                        next_age = previous["age"] + 10
                        prompt = build_continuity_story_prompt(previous, next_age)
                        future_text = generate_openai_text(prompt)
                        image_prompt = build_image_prompt(
                            previous["choice"],
                            previous["age"],
                            previous["personality"],
                            previous["interests"],
                            future_age=next_age,
                            continuity=True,
                        )
                        image_url = generate_openai_image(image_prompt)

                    st.session_state.timeline_step += 1
                    story_entry = {
                        "step": st.session_state.timeline_step,
                        "age": next_age,
                        "choice": previous["choice"],
                        "personality": previous["personality"],
                        "interests": previous["interests"],
                        "reason": previous["reason"],
                        "headline": future_text["headline"],
                        "article": future_text["article"],
                        "image_url": image_url,
                    }
                    st.session_state.story_history.append(story_entry)
                    st.session_state.current_story = story_entry
                    st.experimental_rerun()
