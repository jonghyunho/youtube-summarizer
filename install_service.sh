#!/bin/bash

# 서비스 파일 경로 설정
SERVICE_FILE="/etc/systemd/system/youtube-summarizer.service"
APP_DIR="$(pwd)"
PYTHON_PATH=$(which python3)

# 서비스 파일 생성
cat > "$SERVICE_FILE" << EOL
[Unit]
Description=YouTube Summarizer Service
After=network.target

[Service]
User=jonghyun
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_PATH $APP_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# systemd 리로드
sudo systemctl daemon-reload

# 서비스 활성화 및 시작
sudo systemctl enable youtube-summarizer
sudo systemctl start youtube-summarizer

# 서비스 상태 확인
sudo systemctl status youtube-summarizer
