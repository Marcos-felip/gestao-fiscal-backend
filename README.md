# Gestão Fiscal Backend

## Stack
## Stack

- ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)  Python 3.12
- ![Django](https://img.shields.io/badge/Django-5-green?logo=django&logoColor=white)  Django 5 + DRF
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%20-blue?logo=postgresql&logoColor=white)  PostgreSQL
- ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)  Docker / Docker Compose

## 1. Clonar o repositório

```bash
git clone https://github.com/Marcos-felip/gestao-fiscal-backend.git
cd gestao-fiscal-backend
```

## 2. Variáveis de ambiente

Copie o arquivo de exemplo e ajuste valores sensíveis (senhas, SECRET_KEY):

```bash
cp .env.example .env
```

Principais variáveis (arquivo `.env`):
- SECRET_KEY (trocar em produção)
- POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD
- DEBUG=1 para desenvolvimento

## 3. Subir com Docker

```bash
docker compose up --build
```

Após subir:
- Aplicar migrações (primeira vez):
	```bash
	docker compose exec web python manage.py migrate
	```
- Criar superusuário (opcional):
	```bash
	docker compose exec web python manage.py createsuperuser --email admin@example.com
	```

## 4. Executar sem Docker (opcional)
Pré‑requisitos: Python 3.12 + Postgres local.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajustar variáveis
python manage.py migrate
python manage.py runserver
```