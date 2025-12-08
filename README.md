# 🚀 CI/CD, Git, Docker 실전 가이드 (With Render)

이 프로젝트는 Python Flask 웹 애플리케이션을 사용하여 **Git 버전 관리**, **Docker 컨테이너화**, 그리고 **GitHub Actions + Render**를 연동한 **완벽한 자동화 파이프라인**을 구축하는 튜토리얼입니다.

## 🎯 목표

1.  **Docker:** 애플리케이션을 컨테이너로 포장하기.
2.  **CI (지속적 통합):** 코드가 GitHub에 올라오면 자동으로 테스트하고 빌드 확인하기.
3.  **CD (지속적 배포):** 테스트가 통과된 경우에만 Render 서버에 자동으로 배포하기.

-----

## 1️⃣ 프로젝트 파일 준비 (Step 1: File Setup)

프로젝트 폴더에 다음 파일들을 작성합니다.

### 1\. 웹 서버 코드 (`app.py`)

클라우드 환경(Render)의 포트 설정을 지원하는 웹 서버 코드입니다.

```python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! CI/CD와 Docker 체험 성공입니다!"

if __name__ == '__main__':
    # Render가 제공하는 PORT 환경변수를 사용 (없으면 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
```

### 2\. 테스트 코드 (`test_app.py`)

CI 과정에서 실행될 테스트 시나리오입니다.

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

```text
flask
pytest
```

### 4\. Docker 설정 (`Dockerfile`)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### 5\. Git 무시 목록 (`.gitignore`)

```text
__pycache__/
venv/
.pytest_cache/
```

-----

## 2️⃣ GitHub 저장소 연결 (Step 2: Git Push)

터미널에서 아래 명령어를 입력하여 GitHub에 코드를 업로드합니다.

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
# 본인의 저장소 주소로 변경해주세요!
git remote add origin <본인 원격 저장소>
git push -u origin main
```

-----

## 3️⃣ Render 서버 구축 및 Deploy Hook 설정 (Step 3: Render Setup)

자동 배포를 위해 **Render** 서비스를 설정합니다.

1.  **[Render.com](https://render.com/)** 회원가입 및 로그인.
2.  `New +` -\> `Web Service` -\> `Build and deploy from a Git repository` 선택.
3.  본인의 GitHub 저장소(`sko_git_docker_cicd`) 연결.
4.  **설정:**
      * **Runtime:** Docker
      * **Region:** Singapore (권장)
      * **Free Plan** 선택 후 생성.

### ✨ 중요: "진짜 CI/CD"를 위한 Deploy Hook 설정

Render가 멋대로 배포하지 못하게 막고, **테스트 통과 시에만 배포**되도록 설정합니다.

1.  Render 대시보드 -\> **Settings** 메뉴 클릭.
2.  **Auto-Deploy** 항목을 찾아 \*\*`No`\*\*로 변경하고 저장.
3.  바로 아래 **Deploy Hook** 항목에 있는 URL(`https://api.render.com/...`)을 **복사**합니다.

-----

## 4️⃣ GitHub Secrets 설정 (Step 4: Secrets)

Render의 배포 주소(Deploy Hook)를 GitHub에 안전하게 저장합니다.

1.  GitHub 저장소 상단 **Settings** 탭 클릭.
2.  왼쪽 메뉴 **Secrets and variables** -\> **Actions** 클릭.
3.  **[New repository secret]** 클릭.
      * **Name:** `RENDER_DEPLOY_HOOK`
      * **Secret:** 아까 복사한 Render URL 붙여넣기.
4.  **[Add secret]** 저장.

-----

## 5️⃣ CI/CD 파이프라인 완성 (Step 5: GitHub Actions)

이제 GitHub가 코드를 받으면 **테스트 -\> 빌드 -\> (성공 시) 배포**하도록 지시서를 작성합니다.

`.github/workflows/ci.yml` 파일을 생성하고 아래 내용을 붙여넣습니다.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    # 1. 코드 가져오기
    - name: Checkout code
      uses: actions/checkout@v3

    # 2. 파이썬 환경 설정
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    # 3. 라이브러리 설치
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    # 4. 테스트 실행 (여기서 실패하면 배포되지 않음!)
    - name: Run Tests
      run: pytest

    # 5. Docker 빌드 테스트
    - name: Build Docker Image
      run: docker build -t my-app .

    # 6. Render로 배포 (Deploy Hook 실행)
    - name: Deploy to Render
      if: success() # 위 단계가 모두 성공했을 때만 실행
      run: curl "${{ secrets.RENDER_DEPLOY_HOOK }}"
```

작성 후 변경 사항을 Push 합니다.

```bash
git add .
git commit -m "Add CI/CD pipeline with Deploy Hook"
git push
```

-----

## 6️⃣ 최종 체험: 자동 수정 배포 (Step 6: The Magic Loop)

이제 모든 시스템이 구축되었습니다. 자동 배포를 체험해 봅니다.

1.  **코드 수정:** 로컬의 `app.py` 메시지를 변경합니다.
      * `"Hello!..."` -\> `"안녕하세요! 테스트 통과 후 자동 배포되었습니다!"`
2.  **Git Push:**
    ```bash
    git add .
    git commit -m "Update message"
    git push
    ```
3.  **관찰:**
      * GitHub **Actions** 탭에서 테스트가 통과되는지 확인합니다.
      * 테스트가 끝나면 Render 대시보드에서 **Deploy**가 시작되는지 확인합니다.
4.  **결과:**
      * 배포 완료 후 사이트 URL에 접속하면 문구가 바뀐 것을 볼 수 있습니다\!

-----

## 📝 라이선스

This project is for educational purposes.