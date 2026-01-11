

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






