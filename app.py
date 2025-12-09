import os
from flask import Flask
import redis
import time
app = Flask(__name__)
cache = redis.Redis(host='my-redis', port=6379)
@app.route('/')
def hello():
    # 문구를 마음대로 바꿔봐!
    return f"Hello! 이것은 자동 배포된 웹사이트입니다! Test 수정! 222 333 {get_hit_count()}"

@app.route('/health')
def health_check():
    # 나 살아있어요! 라고 딕셔너리(JSON) 리턴
    return {"status": "ok"}, 200

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

if __name__ == '__main__':
    # 서버가 제공하는 PORT 환경변수를 사용하고, 없으면 5000번을 쓴다.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

