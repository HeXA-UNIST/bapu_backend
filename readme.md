# Taxi HeXA 백엔드

## 프로젝트 소개
UNIST에서 택시를 이용하는 학생들을 위한 택시 호출 서비스입니다.

## 프로젝트 구조
```
TaxiHeXA
├── README.md
├── src
│   ├── error : 서비스 관련 오류 처리
│   │   ├── ...
│   ├── model : 서비스에서 사용하는 데이터 모델
│   │   ├── ...
│   ├── middleware : 서비스에서 사용하는 미들웨어
│   │   ├── ...
│   ├── resource : endpoint정의
│   │   ├── ...
│   ├── schema : 서비스에서 사용하는 데이터 스키마
│   │   ├── ...
│   ├── utils : 서비스에서 사용하는 유틸리티
│   │   ├── ...
├── test : 테스트 코드
│   ├── ...
├── app.py : 서비스 진입점
├── config.py : 서비스 설정
├── requirements.txt : 서비스 의존성
├── Makefile : 서비스 빌드 및 실행 스크립트
```

## 실행 방법
### 1. 의존성 설치
```bash
$ make install
```

### 2. 서비스 실행
```bash
$ make run
```

### 3. 테스트 실행
```bash
$ make test
```

### 4. DB Migration
```bash
$ make migrate
```

## API 문서
HeXA Notion내 멜룬부 페이지 참고