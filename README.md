네, 요청하신 **README.md** 파일을 아주 깔끔하고 친절한 가이드 형식으로 작성해 드릴게요.

이 내용을 복사해서 GitHub 저장소의 `README.md` 파일에 붙여넣으시면 됩니다. 다른 사람들이 이 프로젝트를 보고 따라 하며 CI/CD와 Docker를 배울 수 있도록 구성했습니다.

-----

# 🚀 CI/CD, Git, Docker 체험하기 (Hands-on Guide)

이 프로젝트는 간단한 Python Flask 웹 애플리케이션을 사용하여 **Git 버전 관리**, **Docker 컨테이너화**, 그리고 **GitHub Actions를 이용한 CI/CD(지속적 통합/배포)** 파이프라인을 직접 구축하고 체험해 보기 위한 튜토리얼 저장소입니다.

## 🛠 사용 기술 (Tech Stack)

  * **Language:** Python 3.9 (Flask)
  * **Container:** Docker
  * **VCS:** Git & GitHub
  * **CI/CD:** GitHub Actions
  * **Deployment:** Railway or Render (권장)

-----

## 1️⃣ 프로젝트 파일 작성 (Step 1: Code Setup)

프로젝트 폴더 안에 다음 파일들을 생성합니다.

### 1\. 웹 서버 코드 (`app.py`)

간단한 웹 서버를 실행하는 코드입니다. 포트 설정이 포함되어 있어 클라우드 배포 시 자동으로 포트를 할당받습니다.

```python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! CI/CD와 Docker 체험 성공입니다!"

if __name__ == '__main__':
    # 환경변수 PORT가 있으면 사용하고, 없으면 5000번 사용
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
```

### 2\. 테스트 코드 (`test_app.py`)

서버가 정상적으로 응답하는지 검사하는 자동 테스트 코드입니다.

```python
import pytest
from app import app

def test_hello():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello!" in response.data
```

### 3\. 라이브러리 목록 (`requirements.txt`)

필요한 패키지를 정의합니다.

```text
flask
pytest
```

### 4\. Docker 이미지 설계도 (`Dockerfile`)

확장자 없이 파일명을 `Dockerfile`로 생성합니다.

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### 5\. Git 무시 목록 (`.gitignore`)

Git에 업로드하지 않을 파일들을 지정합니다.

```text
__pycache__/
venv/
.pytest_cache/
```

-----

## 2️⃣ Git 설정 및 원격 저장소 연결 (Step 2: Git Push)

터미널(Terminal)을 열고 프로젝트 폴더에서 아래 명령어들을 순서대로 입력하여 GitHub에 코드를 업로드합니다.

```bash
# 1. Git 초기화
git init

# 2. 모든 파일 스테이징
git add .

# 3. 커밋 생성
git commit -m "Initial commit: Set up Flask app with Docker and Tests"

# 4. 브랜치명을 main으로 변경
git branch -M main

# 5. 원격 저장소 연결 (본인의 저장소 주소 확인!)
git remote add origin https://github.com/codrae/sko_git_docker_cicd.git

# 6. GitHub로 업로드 (Push)
git push -u origin main
```

-----

## 3️⃣ CI/CD 파이프라인 설정 (Step 3: GitHub Actions)

GitHub에 코드가 올라갈 때마다 **자동으로 테스트하고 빌드**하도록 설정합니다.

1.  프로젝트 폴더 내에 `.github/workflows/ci.yml` 경로로 폴더와 파일을 생성합니다.
2.  `ci.yml` 파일에 아래 내용을 작성합니다.

<!-- end list -->

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Tests (CI)
      run: pytest

    - name: Build Docker Image
      run: docker build -t my-app .
```

3.  작성 후 다시 Git Push를 수행합니다.
    ```bash
    git add .
    git commit -m "Add GitHub Actions workflow"
    git push
    ```
4.  GitHub 저장소 상단의 **Actions** 탭에서 초록색 체크(✅)가 뜨는지 확인합니다.

-----

## 4️⃣ 자동 배포 체험하기 (Step 4: Continuous Deployment)

**Render** 또는 **Railway**와 같은 Docker 지원 클라우드 서비스를 사용하여 **"코드를 수정하면 자동으로 사이트가 업데이트되는"** 경험을 해봅니다.

### 설정 방법 (Railway 예시)

1.  [Railway](https://railway.app/) 로그인 후 `New Project` -\> `Deploy from GitHub repo` 선택.
2.  이 저장소(`sko_git_docker_cicd`)를 선택.
3.  자동으로 Dockerfile을 인식하여 배포가 시작됨.
4.  배포 완료 후 제공된 URL로 접속하여 웹사이트 확인.

### 🔄 자동 수정 배포 테스트 (The Magic Loop)

이 과정이 핵심입니다\!

1.  로컬 코드(`app.py`)에서 문구를 수정합니다.
      * 예: `"Hello!..."` -\> `"안녕하세요! 자동 배포가 완료되었습니다!"`
2.  Git으로 코드를 올립니다.
    ```bash
    git add .
    git commit -m "문구 수정 테스트"
    git push
    ```
3.  **GitHub Actions**가 자동으로 테스트를 수행합니다.
4.  **Railway/Render**가 변경 사항을 감지하고 자동으로 재배포합니다.
5.  잠시 후 사이트 주소를 새로고침하면 문구가 바뀐 것을 확인할 수 있습니다\!

-----

## 📝 라이선스

This project is for educational purposes.