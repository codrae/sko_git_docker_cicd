# 1. Python 3.9 슬림 버전을 기반으로 시작
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일 복사
COPY requirements.txt .

# 4. 라이브러리 설치
RUN pip install -r requirements.txt

# 5. 나머지 소스 코드 복사
COPY . .

# 6. 컨테이너 실행 시 작동할 명령어
CMD ["python", "app.py"]