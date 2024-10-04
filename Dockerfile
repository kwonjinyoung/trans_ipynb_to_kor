# 베이스 이미지로 Python 3.9 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 8501 열기 (Streamlit 기본 포트)
EXPOSE 8501

# 애플리케이션 실행
CMD ["streamlit", "run", "ipynb번역기.py", "--server.port=8501", "--server.address=0.0.0.0"]