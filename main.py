import boto3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import query

from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

def get_video_id(video_url):
    try:
        # URL에서 'v=' 뒤의 11자리 영상 ID를 추출합니다.
        video_id = video_url.split('v=')[1][:11]
    except IndexError:
        raise ValueError("유효하지 않은 video_url 입니다.")
    return video_id

def extract_video_id(video_url):
    parsed_url = urlparse(video_url)

    # 단축 URL 형식: https://youtu.be/<video_id>?...
    if "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path.lstrip('/')
        if video_id:
            return video_id

    # 일반 URL 형식: https://www.youtube.com/watch?v=<video_id>
    elif "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return query_params['v'][0]

    # 다른 형식 또는 video_id를 찾을 수 없는 경우
    raise ValueError("유효하지 않은 video_url 입니다.")

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    print(data)
    if not data or 'video_url' not in data:
        return jsonify({"error": "video_url 파라미터가 필요합니다."}), 400

    video_url = data['video_url']

    try:
        video_id = extract_video_id(video_url)
        print(video_id)
    except Exception as e:
        print("error")
        return jsonify({"error": str(e)}), 400

    try:
        # 영어(en)와 한국어(ko) 자막을 가져옵니다.
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ko'])
    except Exception as e:
        print('Error: 자막 변환 실패')
        return jsonify({"error": f"자막을 가져오는 데 실패했습니다: {str(e)}"}), 500

    # 자막을 텍스트 포맷으로 변환
    text_formatted = ""
    for item in transcript:
        text_formatted += item['text']

    try:
        system_prompt = f"You are a summarizer assistant. And you always responds in Markdown format.\n"
        prompt = f"Below is the content that needs to be summarized:\n{text_formatted}\n\n"
        prompt += f"Please summarize the content in detail in Korean. "
        prompt += f"Your response must be entirely in Markdown format. "
        prompt += f"Do not use JSON formatting or output any JSON structure. "
        prompt += f"Do not include the word 'summary' or '요약' in the title of your response."

        service = query.GeminiService()
        response = service.ask(system_prompt, prompt)

        # Markdown 형식의 응답에서 제목 추출 (첫 번째 # 또는 ##으로 시작하는 줄)
        title = "notitle"
        for line in response.split('\n'):
            if line.startswith('# '):
                title = line[2:].strip()  # #과 공백 제거
                break
            elif line.startswith('## '):
                title = line[3:].strip()  # ##과 공백 제거
                break

        # 현재 날짜와 시간을 파일명에 포함
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

        # S3에 저장할 파일명 생성
        s3_filename = f"{current_time}_{title}.md"

        # S3에 파일 업로드
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket='jonghyunho.com',
            Key=f"youtube/{s3_filename}",
            Body=response.encode('utf-8'),
            ContentType='text/markdown'
        )
    except Exception as e:
        return jsonify({"error": f"요약 요청에 실패했습니다: {str(e)}"}), 500

    return response, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051)
