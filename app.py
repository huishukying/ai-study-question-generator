import streamlit as st
from extractor import extract_text
from question import generate_questions
import time
import json

st.set_page_config(
    page_title="AI Study Question Generator",
    page_icon="📚",
    layout="centered"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .summary-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("📚 AI Study Question Generator")
st.markdown("Upload your lecture notes in PDF or image, AI generates revision questions with answers")
st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📖 How to use")
    st.markdown("""
    1. **Upload** a PDF (selectable text, max 10 pages) or image file (clear)
    2. Wait for text extraction
    3. Click **Generate Questions**
    4. Get Questions and Answers!
    """)

    st.header("⚙️ Settings")
    max_text_length = st.slider(
        "Max text length (characters)",
        min_value=1000,
        max_value=10000,
        value=6000,
        help="Longer text = more context but slower processing"
    )

    num_questions = st.slider(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=5,
        help="How many questions to generate"
    )

    st.header("📊 Stats")
    stats_placeholder = st.empty()

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['pdf', 'png', 'jpg', 'jpeg']
)

if uploaded_file is not None: 
    if st.button("Extract Text", type="primary"):
        with st.spinner("Extracting text from file..."):
            extracted_text = extract_text(uploaded_file)

        if extracted_text.startswith("ERROR"):
            st.error(extracted_text)
        else:
            st.session_state['extracted_text'] = extracted_text #save extracted text
            st.session_state['text_length'] = len(extracted_text) #save text length

            st.success(f"✅ Extracted {len(extracted_text)} characters")

            with st.expander("Preview extracted text"):
                st.write(extracted_text[:1000])
                if len(extracted_text) > 1000:
                    st.caption(f"... and {len(extracted_text) - 1000} more characters")
    
    if 'extracted_text' in st.session_state:
        if st.button("Generate Questions", type="primary"):
            with st.spinner("Generating questions..."): 
                start_time = time.time()
                response = generate_questions( #Calls question.py
                    st.session_state['extracted_text'],
                    max_text_length=max_text_length,
                    num_questions=num_questions
                )
                end_time = time.time()

            stats_placeholder.metric("Processing Time", f"{end_time - start_time:.1f} seconds")
            stats_placeholder.metric("Characters", f"{st.session_state['text_length']}")

            st.markdown("## 📚 Study Questions")
            st.caption("💡 Think before you check the answers!")

            try:
                response = response.strip() # " hello\n" → "hello"
                if response.startswith('```json'): # remove ```json
                    response = response[7:]
                if response.startswith('```'): # remove ```
                    response = response[3:]
                if response.endswith('```'): # remove ``` (end)
                    response = response[:-3]
                
                data = json.loads(response.strip()) #converts to Py dictionary

                st.info(f"📖 **Topic:** {data.get('topic', 'Study Notes')}")
                st.divider()

                for idx, pair in enumerate(data['qa_pairs'], 1):
                    st.markdown(f"### Q{idx}. {pair['question']}")

                    with st.expander(f"🔍 Answer"):
                        st.write(pair['answer'])
                    
                    st.divider()
                
            except json.JSONDecodeError as e:
                st.warning(f"Failed to parse response. Showing raw output:\n\nError: {str(e)}")
                st.code(response)
    
            st.markdown("Good luck for your exams!")
    elif uploaded_file is not None and 'extracted_text' not in st.session_state:
        st.caption("👆 Click 'Extract Text' first to process your file")

st.divider()
st.caption(f"Built with HKU Azure OpenAI API (GPT-4.1-mini) | {st.__version__}")

            
