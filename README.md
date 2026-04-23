# smtp-relay-service

Microserviço minimalista de relay SMTP construído com FastAPI.

Nasceu pra resolver um problema pontual: containers no Railway bloqueiam conexões diretas nas portas SMTP (465/587), impedindo o envio de emails transacionais a partir do worker Celery. A solução foi isolar o envio em um serviço separado hospedado no Render, que recebe requisições HTTP do Django e repassa para o SMTP da Hostinger.

## Como funciona

```
Django (Railway) → POST /send → smtp-relay (Render) → SMTP Hostinger → Email
```

A autenticação entre os serviços é feita via API key no header `x-api-key`.

## Endpoints

| Método | Rota      | Descrição                        |
|--------|-----------|----------------------------------|
| GET    | /health   | Health check para o Render       |
| POST   | /send     | Envia um email via SMTP          |

## Variáveis de ambiente

| Variável        | Descrição                              |
|-----------------|----------------------------------------|
| `SMTP_HOST`     | Host SMTP (ex: smtp.hostinger.com)     |
| `SMTP_PORT`     | Porta SMTP (587)                       |
| `SMTP_USER`     | Email remetente                        |
| `SMTP_PASS`     | Senha do email                         |
| `SMTP_FROM`     | Endereço do remetente                  |
| `SMTP_FROM_NAME`| Nome exibido no remetente              |
| `API_KEY`       | Chave de autenticação entre serviços   |
| `DEBUG`         | Liga logs detalhados e /docs (false)   |

## Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic Settings