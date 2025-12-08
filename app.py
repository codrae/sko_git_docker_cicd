from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! CI/CD와 Docker 체험 성공입니다! 수정수정 이렇게 !"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)