import requests
import json

def main():
    # Flask 서버의 URL (포트 번호는 서버 설정에 맞게 조정)
    url = "http://localhost:5050/summarize"

    # 요청에 사용할 video_url 데이터
    payload = {
        "video_url": "https://www.youtube.com/watch?v=Aw7iQjKAX2k"
    }

    # HTTP 헤더 설정
    headers = {
        "Content-Type": "application/json"
    }

    # POST 요청 보내기
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # 오류 발생 시 예외 발생
    except requests.RequestException as e:
        print("요청 중 오류 발생:", e)
        return

    # 서버 응답을 JSON 형식으로 파싱하여 출력
    #result = response.json()
    print("서버 응답:")
    print(response.text)
    #print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
