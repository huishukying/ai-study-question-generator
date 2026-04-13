# Simple Coffee - Full-Stack E-commerce Platform

## Features
- Upload PDF/image → AI generate Q&A pairs
- JSON-structured output for easy integration
- Interactive Streamlit UI with hidden answers

## Tech Stack
- Python
- Streamlit
- Azure OpenAI API
- Tesseract OCR

## How to use
```bash
git clone https://github.com/huishukying/ai-study-question-generator.git && \
cd ai-study-question-generator && \
pip install -r requirements.txt && \
brew install tesseract && \
echo "API_KEY=your_hku_azure_key_here" > .env && \
streamlit run app.py 
```

## Screenshots
<img src="screenshots/study_helper_1.jpg" width="600">
<img src="screenshots/study_helper_2.jpg" width="600">
<img src="screenshots/study_helper_3.jpg" width="600">
<img src="screenshots/study_helper_4.jpg" width="600">
<img src="screenshots/study_helper_5.jpg" width="600">
