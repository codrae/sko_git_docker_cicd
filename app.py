import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # 문구를 마음대로 바꿔봐!
    return "Hello! 이것은 자동 배포된 웹사이트입니다! Test 수정! 222"

if __name__ == '__main__':
    # 서버가 제공하는 PORT 환경변수를 사용하고, 없으면 5000번을 쓴다.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)