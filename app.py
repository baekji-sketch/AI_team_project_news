import datetime
import os
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
)

st.set_page_config(
    page_title="IF : 다른 선택의 미래",
    page_icon="🪞",
    layout="wide",
)

PAGE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Noto+Serif+KR:wght@400;500;700&display=swap');

body {
    background: #F9F8F6;
    color: #222222;
}

main .block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 2200px;
}

.news-title-panel {
    text-align: center;
    margin-bottom: 3rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #d8d0c6;
}

.news-title-panel h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(3.4rem, 4.8vw, 6rem);
    color: #1f1a18;
    margin: 0;
    letter-spacing: -0.04em;
}

.news-title-panel .meta {
    margin-top: 1rem;
    font-family: 'Noto Serif KR', serif;
    color: #4f4a44;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    font-size: 0.9rem;
}

.news-title-panel .meta span {
    padding: 0.15rem 0.8rem;
    border: 1px solid #d8d0c6;
    margin: 0 0.35rem;
}

.panel {
    background: #fff;
    border: 1px solid #d8d0c6;
    box-shadow: 0 18px 48px rgba(83, 74, 66, 0.08);
    padding: 1.8rem;
    margin-bottom: 1.8rem;
}

.panel h2,
.panel h3,
.panel h4 {
    font-family: 'Noto Serif KR', serif;
    color: #1f1a18;
    margin-bottom: 1rem;
}

.panel h2 {
    font-size: 1.6rem;
    letter-spacing: 0.04em;
}

.panel h3 {
    font-size: 1.35rem;
}

.input-label {
    font-family: 'Noto Serif KR', serif;
    font-weight: 600;
    color: #222222;
    margin-bottom: 0.35rem;
    margin-top: 1rem;
}

.stTextArea textarea,
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stTextInput>div>div>textarea,
.stTextArea>div>div>textarea {
    border-radius: 0;
    border: 1px solid #7a746c;
    background: #fbfaf6;
    color: #222222;
    font-family: 'Noto Serif KR', serif;
}

.stTextArea textarea:focus,
.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stTextInput>div>div>textarea:focus,
.stTextArea>div>div>textarea:focus {
    outline: 2px solid rgba(32, 56, 88, 0.16);
}

.stButton>button {
    border-radius: 0;
    background: #1f3f73;
    color: #faf8f2;
    padding: 0.85rem 1.8rem;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    opacity: 0.92;
}

.news-headline {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 4vw, 4.5rem);
    line-height: 1.02;
    font-weight: 800;
    color: #1b1a18;
    margin-bottom: 0.35rem;
}

.news-subtitle {
    font-family: 'Noto Serif KR', serif;
    color: #5b5550;
    margin-bottom: 1.25rem;
}

.news-article {
    font-family: 'Noto Serif KR', serif;
    color: #2a2724;
    line-height: 1.85;
    font-size: 1rem;
}

.news-article p:first-of-type::first-letter {
    float: left;
    font-size: 4rem;
    line-height: 0.8;
    margin-right: 0.15em;
    font-weight: 700;
    color: #1d1b18;
}

.news-article blockquote {
    margin: 1.8rem 0;
    padding-left: 1rem;
    border-left: 4px solid #415274;
    color: #4c4844;
    font-style: italic;
}

.news-detail {
    display: grid;
    gap: 1rem;
}

.news-image {
    width: 100%;
    border: 1px solid #d8d0c6;
}

.timeline-list li {
    margin-bottom: 0.9rem;
    color: #4f4a44;
}

.timeline-list strong {
    color: #222222;
}
"""

st.markdown(f"<style>{PAGE_CSS}</style>", unsafe_allow_html=True)

initialize_session_state()

header_html = f"""
<div class='news-title-panel'>
    <h1>IF : 다른 선택의 미래</h1>
    <div class='meta'>
        <span>{datetime.date.today():%B %d, %Y}</span>
        <span>Parallel Universe Edition</span>
    </div>
    <p class='news-subtitle'>뉴욕타임스 스타일의 디지털 신문 지면, 당신이 선택하지 않은 또 다른 삶의 헤드라인을 펼쳐보세요.</p>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

left_col, mid_col, right_col = st.columns([2, 3, 3], gap='large')

with left_col:
    st.markdown("""
    <div class='panel'>
        <h2>대체 인생 간단 입력</h2>
        <p style='color:#5b5550; margin-top:-0.5rem;'>세련된 신문 양식처럼 차분하게 작성하세요.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form(key='parallel_form'):
        st.text_area(
            '대체 인생 선택',
            placeholder='예시: 중학교 때 축구 연습을 그만두었습니다.',
            height=140,
            key='alternate_choice',
        )
        st.number_input(
            '현재 나이',
            min_value=12,
            max_value=90,
            value=24,
            step=1,
            help='현재 나이는 AI가 미래 타임라인을 구성하는 데 도움이 됩니다.',
            key='current_age',
        )
        st.text_input(
            '성격 특징',
            placeholder='창의적, 감성적, 호기심 많음',
            key='personality',
        )
        st.text_input(
            '관심사',
            placeholder='스포츠, 게임, 음악',
            key='interests',
        )
        st.text_area(
            '그 길을 포기한 이유',
            placeholder='부모님의 압박, 실패에 대한 두려움, 가족을 부양해야 하는 상황',
            height=100,
            key='reason',
        )
        st.text_input(
            'OpenAI API 키',
            type='password',
            placeholder='sk-...',
            help='이 세션에서 사용할 OpenAI API 키를 입력하세요.',
            key='openai_api_key_input',
        )
        generate_button = st.form_submit_button('평행 세계 생성')

    st.markdown("""
    <div class='panel'>
        <h3>타임라인 히스토리</h3>
        <ul class='timeline-list'>
    """, unsafe_allow_html=True)

    if st.session_state.story_history:
        for entry in st.session_state.story_history:
            st.markdown(f"<li><strong>T+{entry['step']*10}년</strong> — 나이 {entry['age']} / {entry['headline']}</li>", unsafe_allow_html=True)
    else:
        st.markdown("<li>아직 생성된 평행 세계가 없습니다.</li>", unsafe_allow_html=True)

    st.markdown("</ul></div>", unsafe_allow_html=True)

with mid_col:
    if st.session_state.get('current_story'):
        story = st.session_state.current_story
        st.markdown("""
        <div class='panel'>
            <div class='news-headline'>{headline}</div>
            <div class='news-subtitle'>현재 연대와 감성, 그리고 그 선택이 만든 미래의 서사.</div>
        </div>
        """.replace('{headline}', story['headline']), unsafe_allow_html=True)
        if story['image_url']:
            st.image(story['image_url'], use_column_width=True, caption='대체 미래의 표지 이미지', clamp=True)
        else:
            st.markdown("""
            <div class='panel'>
                <p style='color:#5b5550;'>이미지 생성이 실패했습니다. API 키와 연결 상태를 확인하세요.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='panel'>
            <h3>평행 세계를 펼쳐보세요</h3>
            <p style='color:#5b5550;'>왼쪽 입력란에서 당신의 다른 선택을 입력하면 미래 뉴스 헤드라인과 이미지, 기사가 우측 지면에 펼쳐집니다.</p>
        </div>
        """, unsafe_allow_html=True)

with right_col:
    if st.session_state.get('current_story'):
        story = st.session_state.current_story
        article_html = story['article'].strip().replace('\n\n', '</p><p>').replace('\n', '<br>')
        st.markdown("""
        <div class='panel'>
            <h3>미래 기사</h3>
            <div class='news-article'>
                <p>{article}</p>
            </div>
        </div>
        """.replace('{article}', article_html), unsafe_allow_html=True)
        st.download_button(
            label='기사 텍스트 다운로드',
            data=story['article'],
            file_name='if_alternate_life.txt',
            mime='text/plain',
        )
        if st.button('이야기 계속하기 (+10년)'):
            api_key = get_openai_api_key()
            if not api_key:
                st.error('OpenAI API 키가 없습니다. 환경 변수 또는 Streamlit secrets에 설정해 주세요.')
            else:
                with st.spinner('같은 우주에서 타임라인을 10년 더 진행하는 중...'):
                    previous = st.session_state.current_story
                    next_age = previous['age'] + 10
                    prompt = build_continuity_story_prompt(previous, next_age)
                    future_text = generate_openai_text(prompt)
                    image_prompt = build_image_prompt(
                        previous['choice'],
                        previous['age'],
                        previous['personality'],
                        previous['interests'],
                        future_age=next_age,
                        continuity=True,
                    )
                    image_url = generate_openai_image(image_prompt)

                st.session_state.timeline_step += 1
                story_entry = {
                    'step': st.session_state.timeline_step,
                    'age': next_age,
                    'choice': previous['choice'],
                    'personality': previous['personality'],
                    'interests': previous['interests'],
                    'reason': previous['reason'],
                    'headline': future_text['headline'],
                    'article': future_text['article'],
                    'image_url': image_url,
                }
                st.session_state.story_history.append(story_entry)
                st.session_state.current_story = story_entry
                st.experimental_rerun()
    else:
        st.markdown("""
        <div class='panel'>
            <h3>기사 지면</h3>
            <p style='color:#5b5550;'>여기에 생성된 뉴스 기사와 감성적인 평행 세계의 이야기가 신문 지면처럼 표시됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

if generate_button:
    if not st.session_state.alternate_choice.strip():
        st.error('선택하지 않은 대체 인생 선택을 입력해 주세요.')
    else:
        api_key = get_openai_api_key()
        if not api_key:
            st.error('OpenAI API 키가 없습니다. 환경 변수 또는 Streamlit secrets에 설정해 주세요.')
        else:
            with st.spinner('평행 우주를 시뮬레이션하는 중...'):
                prompt = build_initial_story_prompt(
                    st.session_state.alternate_choice,
                    int(st.session_state.current_age),
                    st.session_state.personality,
                    st.session_state.interests,
                    st.session_state.reason,
                )
                future_text = generate_openai_text(prompt)
                image_prompt = build_image_prompt(
                    st.session_state.alternate_choice,
                    int(st.session_state.current_age),
                    st.session_state.personality,
                    st.session_state.interests,
                )
                image_url = generate_openai_image(image_prompt)

            story_entry = {
                'step': 0,
                'age': int(st.session_state.current_age),
                'choice': st.session_state.alternate_choice,
                'personality': st.session_state.personality,
                'interests': st.session_state.interests,
                'reason': st.session_state.reason,
                'headline': future_text['headline'],
                'article': future_text['article'],
                'image_url': image_url,
            }
            st.session_state.story_history = [story_entry]
            st.session_state.current_story = story_entry
            st.session_state.timeline_step = 0
            st.experimental_rerun()
