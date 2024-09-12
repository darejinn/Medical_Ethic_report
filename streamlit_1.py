import streamlit as st
from function import generate_plans, manual, init_plan, final_plan, make_report, create_word_file
import datetime
import pandas as pd
import time

##################################################################################################################################################################################

st.title("🦜🔗 윤리 보고서 생성")



# 세션 상태에서 topics를 초기화 (최초 실행 시에만 초기화)
if 'topics' not in st.session_state:
    st.session_state.topics = {}
with st.form("my_form_1"):
    text = st.text_area(
        "윤리 소재 입력:",
        "무엇과 관련된 주제를 생성할까요?",
    )
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # 로딩 애니메이션과 메시지 표시
        with st.spinner('약 30초 정도 소요됩니다...'):

            # 예시 response (실제 함수 호출 대신 사용)
            # response = {'1': '주제1: 설명1', '2': '주제2: 설명2', '3': '주제3: 설명3', ...}
            response = generate_plans(text)  # 실제로는 이 함수를 호출하여 response 생성

            # topics 딕셔너리에 주제와 설명을 추가하고 세션 상태에 저장
            for i in range(1, 9):
                topic, description = response[str(i)].split(": ", 1)
                st.session_state.topics[topic] = description  # 세션 상태에 저장

            # 각 주제를 출력
            for key, value in response.items():
                topic, description = value.split(": ", 1)
                st.markdown(f"#### 주제 {key}: {topic}")
                st.write(f"**상세 설명**: {description}")
                st.markdown("---")  # 주제 간 구분선 추가
# 두 번째 폼 (주제 선택)
if st.session_state.get('topics'):  # topics가 세션에 저장된 경우만 실행
    with st.form("my_form_2"):
        # 라디오 선택 버튼: 세션 상태의 topics 딕셔너리의 키 사용
        주제 = st.radio(
            '어떤 주제로 개요를 생성할까요?',
            list(st.session_state.topics.keys()),  # 딕셔너리의 키 리스트
            index=0  # 기본 선택 값을 첫 번째 주제로 설정
        )
        submitted = st.form_submit_button("Submit")
        
        # 폼 제출 시 보고서 생성
        if submitted:
            # 로딩 애니메이션과 메시지 표시
            with st.spinner('약 2분 정도 소요됩니다...'):
                # 텍스트 할당
                text = f"{주제} : {st.session_state.topics[주제]}"
                response2 = make_report(text)  # 가상의 함수로 보고서 생성
                st.code(response2, language='python')
                st.markdown("---")
                st.info(f"보고서 생성 시각 : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

                # 워드 파일 생성
                st.session_state.word_file = create_word_file(response2)

# 폼 외부에서 다운로드 버튼 표시
if 'word_file' in st.session_state:
    st.download_button(
        label="워드 파일 다운로드",
        data=st.session_state.word_file,
        file_name="report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.write("보고서를 생성한 후에 다운로드할 수 있습니다.")