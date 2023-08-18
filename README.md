1.Para subir container docker:

docker compose up

2.Para executar as migrations da api:

docker compose exec backend alembic upgrade heads

3.Para realizar os testes dos endpoints:

http://0.0.0.0:8000/docs
