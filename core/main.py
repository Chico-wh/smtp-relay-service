import logging
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse

from .config import settings
from .schemas import EmailPayload, EmailResponse
from .smtp import send_email

# ─── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Allugi Email Relay",
    description="Microserviço de envio de email via SMTP",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,  # esconde docs em produção
    redoc_url=None,
)

# ─── Dependência de autenticação ─────────────────────────────────────────────

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        logger.warning("Tentativa de acesso com API key inválida")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key inválida.",
        )


# ─── Rotas ───────────────────────────────────────────────────────────────────

@app.get("/health", tags=["infra"])
def health_check():
    """Usado pelo Render para verificar se o serviço está vivo."""
    return {"status": "ok"}


@app.post(
    "/send",
    response_model=EmailResponse,
    tags=["email"],
    status_code=status.HTTP_200_OK,
)
def send(payload: EmailPayload, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    try:
        send_email(payload)
        return EmailResponse(success=True, message="Email enviado com sucesso.")
    except Exception as e:
        logger.error("Falha ao enviar email para %s: %s", payload.to, str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Falha no envio: {str(e)}",
        )


# ─── Handler global de erros ─────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("Erro não tratado: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Erro interno no relay."},
    )