# Code-Analysis-Server
FastAPI를 사용한 파이썬 코드 분석 서버

### 개발 환경
개발언어 : python 3.11

## ✅ run
1. 프로젝트 다운로드 <br>
`git clone https://github.com/Co-due/Code-Analysis-Server.git`

2. 라이브러리 다운로드 <br>
`pip install -r requirements.txt`

3. 실행 <br>
`cd app` <br>
`uvicorn main:app --reload`

<br>

## ❌ 실행 안될 시

**오류 1. [Errno 48] Address already in use   <br>**
1. 8000포트 사용하는 프로세스 찾기 <br>
`lsof -i:8000` <br>
2. 해당 프로세스 강제 종료 <br>
`kill -9 [pid번호]` <br>
