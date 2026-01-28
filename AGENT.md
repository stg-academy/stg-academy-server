# 프로젝트 구조

```
fastapi-postgres-backend/
├── app/
│   ├── api/              # API 라우터
│   │   ├── auth.py       # 인증 (회원가입, 로그인)
│   │   └── users.py      # 사용자 CRUD
│   ├── models/           # SQLAlchemy 모델
│   │   └── user.py
│   ├── schemas/          # Pydantic 스키마
│   │   └── user.py
│   ├── crud/             # 데이터베이스 작업
│   │   └── user.py
│   ├── utils/            # 유틸리티
│   │   └── security.py   # JWT, 비밀번호 해싱
│   ├── config.py         # 설정 관리
│   ├── database.py       # DB 연결
│   └── main.py           # 앱 진입점
├── alembic/              # 마이그레이션
├── requirements.txt
├── .env.example
└── README.md
```

```

  생성된 파일 구조:
  app/
  ├── api/
  │   ├── auth.py       # 카카오 로그인, JWT 인증
  │   └── users.py      # 모든 CRUD API 엔드포인트
  ├── models/
  │   └── user.py       # 6개 테이블 SQLAlchemy 모델
  ├── schemas/
  │   └── user.py       # Pydantic 스키마 (Request/Response)
  ├── crud/
  │   └── user.py       # 데이터베이스 CRUD 작업
  ├── utils/
  │   └── security.py   # JWT, 패스워드 해싱
  ├── config.py         # 환경 설정
  ├── database.py       # DB 연결
  └── main.py           # FastAPI 앱 진입점

  주요 API 엔드포인트:

  인증:
  - GET /auth/kakao - 카카오 로그인 URL 생성
  - GET /auth/kakao/callback - 카카오 콜백 처리
  - GET /auth/me - 현재 사용자 정보
  - POST /auth/logout - 로그아웃

  CRUD 작업:
  - Users: /api/users/*
  - Courses: /api/courses/*
  - Classes: /api/courses/{id}/classes/*, /api/classes/*
  - Lectures: /api/classes/{id}/lectures/*, /api/lectures/*
  - Attendances: /api/lectures/{id}/attendances/*, /api/attendances/*
  - Certifications: /api/certifications/*, /api/users/{id}/certifications

  모든 보호된 엔드포인트는 JWT 인증이 필요하며, 카카오 OAuth2 로그인이 구현되어 있습니다.
```

# DB 테이블 구조

### Users
| 컬럼명       | 데이터 타입 | 제약 조건             | 설명                                  |
|--------------|--------|-------------------|-------------------------------------|
| id           | Text   | PRIMARY KEY, UUID | 사용자 고유 식별자                          |
| username     | Text   | NOT NULL, UNIQUE  | 사용자 이름                              |
| auth_type   | Text   | NOT NULL          | 인증 유형 (예: 'manual', 'temp', 'kakao') |
| password     | Text   |                   | 비밀번호 (auth_type이 'manual'일 때 사용)    |
| kakao_id    | Text   |                   | 카카오톡 고유 식별자 (auth_type이 'kakao'일 때 사용) |
| authorizations | JSONB  |                   | 사용자 권한 정보 (예: 역할, 권한 등)            |
| created_at   | TIMESTAMP | NOT NULL          | 계정 생성 일시                           |
| updated_at   | TIMESTAMP | NOT NULL          | 계정 정보 수정 일시                        |
| last_login   | TIMESTAMP |                   | 마지막 로그인 일시                        |
| is_active    | BOOLEAN | NOT NULL          | 계정 활성 상태                           |

### Courses
| 컬럼명         | 데이터 타입 | 제약 조건             | 설명        |
|-------------|--------|-------------------|-----------|
| id          | Text   | PRIMARY KEY, UUID | 강의 고유 식별자 |
| title       | Text   | NOT NULL          | 강의 제목     |
| description | Text   |                   | 강의 설명     |
| keyword     | Text   |                   | 키워드       |
| created_at  | TIMESTAMP | NOT NULL          | 강의 생성 일시  |
| created_by  | Text   | NOT NULL          | 강의 생성자    |
| updated_at  | TIMESTAMP | NOT NULL          | 강의 수정 일시  |
| updated_by  | Text   | NOT NULL          | 강의 수정자    |
| is_active   | BOOLEAN | NOT NULL          | 강의 활성 상태  |

### Classes
| 컬럼명           | 데이터 타입 | 제약 조건             | 설명                         |
|---------------|--------|-------------------|----------------------------|
| id            | Text   | PRIMARY KEY, UUID | 수업 고유 식별자                  |
| course_id     | Text   | NOT NULL          | 강의 고유 식별자 (Courses 테이블 참조) |
| title         | Text   | NOT NULL          | 수업 제목                      |
| lecturer_info | Text   |                   | 강사 정보                      |
| date_info    | Text   |                   | 수업 날짜 정보                   |
| begin_date    | TIMESTAMP |                   | 수업 시작 일시                   |
| end_date      | TIMESTAMP |                   | 수업 종료 일시                   |
| created_at    | TIMESTAMP | NOT NULL          | 수업 생성 일시                   |
| created_by    | Text   | NOT NULL          | 수업 생성자                     |
| updated_at    | TIMESTAMP | NOT NULL          | 수업 수정 일시                   |
| updated_by    | Text   | NOT NULL          | 수업 수정자                     |
| is_active     | BOOLEAN | NOT NULL          | 수업 활성 상태                   |

### Lectures
| 컬럼명        | 데이터 타입 | 제약 조건             | 설명                         |
|-------------|--------|-------------------|----------------------------|
| id          | Text   | PRIMARY KEY, UUID | 강의 고유 식별자                  |
| class_id    | Text   | NOT NULL          | 수업 고유 식별자 (Classes 테이블 참조) |
| title       | Text   | NOT NULL          | 강의 제목                      |
| sequence    | INTEGER | NOT NULL          | 강의 순서                      |
| attendance_type | Text   |                   | 출석 유형                      |
| lecture_date  | TIMESTAMP |                   | 강의 일시                      |
| created_at  | TIMESTAMP | NOT NULL          | 강의 생성 일시                   |
| created_by  | Text   | NOT NULL          | 강의 생성자                     |
| updated_at  | TIMESTAMP | NOT NULL          | 강의 수정 일시                   |
| updated_by  | Text   | NOT NULL          | 강의 수정자                     |

### Attendances
| 컬럼명        | 데이터 타입 | 제약 조건             | 설명                                        |
|-------------|--------|-------------------|-------------------------------------------|
| id          | Text   | PRIMARY KEY, UUID | 출석 고유 식별자                                 |
| lecture_id  | Text   | NOT NULL          | 강의 고유 식별자 (Lectures 테이블 참조)               |
| user_id     | Text   | NOT NULL          | 사용자 고유 식별자 (Users 테이블 참조)                 |
| status      | Text   | NOT NULL          | 출석 상태 (예: 'present', 'absent', 'late')    |
| detail_type | Text   |                   | 출석 상세 유형                                  |
| description| Text   |                   | 출석 설명                                     |
| assignment_id | Text   |                   | 과제 고유 식별자 (Assignments 테이블 참조) (현재는 NULL) |
| created_at  | TIMESTAMP | NOT NULL          | 출석 기록 생성 일시                              |
| created_by  | Text   | NOT NULL          | 출석 기록 생성자                                |
| updated_at  | TIMESTAMP | NOT NULL          | 출석 기록 수정 일시                              |
| updated_by  | Text   | NOT NULL          | 출석 기록 수정자                                |


### Certifications
| 컬럼명       | 데이터 타입 | 제약 조건             | 설명                        |
|-----------|--------|-------------------|---------------------------|
| id        | Text   | PRIMARY KEY, UUID | 수료 고유 식별자                 |
| course_id | Text   | NOT NULL          | 수업 고유 식별자 (Course 테이블 참조) |
| user_id   | Text   | NOT NULL          | 사용자 고유 식별자 (Users 테이블 참조) |
| class_ids | JSONB  |                   | 수료한 수업 고유 식별자 목록           |
| issued_at | TIMESTAMP | NOT NULL          | 수료증 발급 일시                 |
| created_at| TIMESTAMP | NOT NULL          | 수료 기록 생성 일시               |
| created_by| Text   | NOT NULL          | 수료 기록 생성자                 |
| updated_at| TIMESTAMP | NOT NULL          | 수료 기록 수정 일시               |
| updated_by| Text   | NOT NULL          | 수료 기록 수정자                 |

# 개발 계획

## 1단계: 카카오 로그인 구현

### 1.1 환경 설정 및 의존성
- [ ] 카카오 API 관련 패키지 설치 (httpx, python-jose, passlib)
- [ ] 환경변수 설정 (.env 파일에 KAKAO_CLIENT_ID, SECRET_KEY 등)
- [ ] JWT 토큰 관리를 위한 설정

### 1.2 카카오 인증 API 구현
- [ ] 카카오 OAuth2 인증 URL 생성 엔드포인트 (`/auth/kakao`)
- [ ] 카카오 콜백 처리 엔드포인트 (`/auth/kakao/callback`)
- [ ] 카카오 사용자 정보 조회 함수
- [ ] JWT 토큰 생성/검증 유틸리티

### 1.3 사용자 관리 로직
- [ ] 신규 카카오 사용자 자동 등록
- [ ] 기존 카카오 사용자 로그인 처리
- [ ] 사용자 세션 관리
- [ ] 로그아웃 처리

### 1.4 인증 미들웨어
- [ ] JWT 토큰 검증 미들웨어
- [ ] 보호된 라우트를 위한 데코레이터
- [ ] 권한 체크 시스템 (authorizations 필드 활용)

## 2단계: CRUD 작업 구현

### 2.1 기본 CRUD 구조 설정
- [ ] Pydantic 스키마 정의 (각 테이블별 Request/Response 모델)
- [ ] 기본 CRUD 베이스 클래스 생성
- [ ] 데이터베이스 서비스 레이어 구현
- [ ] 에러 핸들링 및 예외 처리

### 2.2 Users CRUD
- [ ] 사용자 목록 조회 (`GET /users`)
- [ ] 사용자 상세 조회 (`GET /users/{user_id}`)
- [ ] 사용자 정보 수정 (`PUT /users/{user_id}`)
- [ ] 사용자 삭제/비활성화 (`DELETE /users/{user_id}`)
- [ ] 사용자 권한 관리 (`PUT /users/{user_id}/authorizations`)

### 2.3 Courses CRUD
- [ ] 강의 생성 (`POST /courses`)
- [ ] 강의 목록 조회 (`GET /courses`)
- [ ] 강의 상세 조회 (`GET /courses/{course_id}`)
- [ ] 강의 정보 수정 (`PUT /courses/{course_id}`)
- [ ] 강의 삭제/비활성화 (`DELETE /courses/{course_id}`)

### 2.4 Classes CRUD
- [ ] 수업 생성 (`POST /courses/{course_id}/classes`)
- [ ] 수업 목록 조회 (`GET /courses/{course_id}/classes`)
- [ ] 수업 상세 조회 (`GET /classes/{class_id}`)
- [ ] 수업 정보 수정 (`PUT /classes/{class_id}`)
- [ ] 수업 삭제/비활성화 (`DELETE /classes/{class_id}`)

### 2.5 Lectures CRUD
- [ ] 강의 생성 (`POST /classes/{class_id}/lectures`)
- [ ] 강의 목록 조회 (`GET /classes/{class_id}/lectures`)
- [ ] 강의 상세 조회 (`GET /lectures/{lecture_id}`)
- [ ] 강의 정보 수정 (`PUT /lectures/{lecture_id}`)
- [ ] 강의 삭제 (`DELETE /lectures/{lecture_id}`)

### 2.6 Attendances CRUD
- [ ] 출석 기록 생성 (`POST /lectures/{lecture_id}/attendances`)
- [ ] 출석 목록 조회 (`GET /lectures/{lecture_id}/attendances`)
- [ ] 개별 출석 조회 (`GET /attendances/{attendance_id}`)
- [ ] 출석 상태 수정 (`PUT /attendances/{attendance_id}`)
- [ ] 출석 기록 삭제 (`DELETE /attendances/{attendance_id}`)

### 2.7 Certifications CRUD
- [ ] 수료증 발급 (`POST /certifications`)
- [ ] 수료증 목록 조회 (`GET /certifications`)
- [ ] 수료증 상세 조회 (`GET /certifications/{certification_id}`)
- [ ] 사용자별 수료증 조회 (`GET /users/{user_id}/certifications`)

## 3단계: 고급 기능 구현

### 3.1 검색 및 필터링
- [ ] 강의 검색 (제목, 키워드 기반)
- [ ] 사용자 검색 (이름, 인증 타입 기반)
- [ ] 출석 통계 및 필터링
- [ ] 페이지네이션 구현

### 3.2 통계 및 리포트
- [ ] 강의별 출석률 통계
- [ ] 사용자별 수강 내역
- [ ] 수료 현황 대시보드
- [ ] 월별/주별 통계 리포트

### 3.3 알림 및 이벤트
- [ ] 강의 시작 알림
- [ ] 출석 체크 리마인더
- [ ] 수료증 발급 알림

## 4단계: 테스트 및 최적화

### 4.1 테스트 코드 작성
- [ ] 단위 테스트 (pytest)
- [ ] 통합 테스트
- [ ] API 테스트
- [ ] 인증 테스트

### 4.2 성능 최적화
- [ ] 데이터베이스 인덱스 최적화
- [ ] 쿼리 최적화
- [ ] 캐싱 전략 구현
- [ ] API 응답 최적화

### 4.3 보안 및 배포
- [ ] 입력 데이터 검증 강화
- [ ] Rate limiting 구현
- [ ] CORS 설정
- [ ] 프로덕션 환경 설정






