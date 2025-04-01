FROM ubuntu:24.04

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
COPY .env .
COPY main.py .
COPY query.py .

# 가상환경 생성 및 패키지 설치
RUN python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install -r requirements.txt

# 포트 설정
EXPOSE 5050

# 애플리케이션 실행
CMD ["/app/venv/bin/python3", "main.py"]
