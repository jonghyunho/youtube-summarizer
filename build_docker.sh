# 이미지 빌드
docker build -t youtube-summarizer .

# 컨테이너 실행
docker run -d -p 5050:5050 youtube-summarizer
