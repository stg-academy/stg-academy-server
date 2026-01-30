# 테스트

### 테스트용 DB 생성

- postgreSQL

```bash
docker run \
    --name test-postgres \ 
    -e POSTGRES_USER=postgres \ 
    -e POSTGRES_PASSWORD=testpassword \ 
    -e POSTGRES_DB=testdb \ 
    -p 5433:5432 \ 
    -d postgres:16
```

-
- connnect

```
postgresql://postgres:testpassword@localhost:5433/testdb
```