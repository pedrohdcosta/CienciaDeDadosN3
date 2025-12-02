"""
API de Predição de Churn - Telecomunicações

Esta API permite fazer predições de churn de clientes usando o modelo treinado.
Endpoints disponíveis:
- GET /health: Verificar status da API
- POST /predict: Predição para um cliente
- POST /predict/batch: Predição para múltiplos clientes
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import joblib
import os

# Configurar caminhos dos arquivos do modelo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "test", "modelo_final.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "test", "feature_columns.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "test", "scaler.pkl")

# Variáveis globais para armazenar modelo e artefatos
modelo = None
feature_columns = None
scaler = None


def carregar_modelo():
    """Carrega o modelo e artefatos necessários."""
    global modelo, feature_columns, scaler
    
    if modelo is None:
        try:
            modelo = joblib.load(MODEL_PATH)
            feature_columns = joblib.load(FEATURES_PATH)
        except FileNotFoundError as e:
            raise RuntimeError(f"Erro ao carregar modelo: {e}. Certifique-se que os arquivos .pkl existem em {os.path.dirname(MODEL_PATH)}")
        
        try:
            scaler = joblib.load(SCALER_PATH)
        except FileNotFoundError:
            scaler = None
    
    return modelo, feature_columns, scaler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação."""
    # Carrega modelo ao iniciar
    carregar_modelo()
    yield
    # Cleanup (se necessário)


# Criar aplicação FastAPI
app = FastAPI(
    title="API de Predição de Churn",
    description="API para predição de churn de clientes de telecomunicações",
    version="1.0.0",
    lifespan=lifespan
)


# Modelos Pydantic para validação de dados
class ClienteInput(BaseModel):
    """Dados de entrada para predição de churn de um cliente."""
    
    tenure: int = Field(..., ge=0, le=120, description="Meses como cliente (0-120)")
    MonthlyCharges: float = Field(..., ge=0, description="Valor mensal (R$)")
    TotalCharges: float = Field(..., ge=0, description="Total gasto (R$)")
    Contract: Literal["Month-to-month", "One year", "Two year"] = Field(
        ..., description="Tipo de contrato"
    )
    InternetService: Literal["DSL", "Fiber optic", "No"] = Field(
        ..., description="Tipo de serviço de internet"
    )
    PaymentMethod: Literal[
        "Electronic check", 
        "Mailed check", 
        "Bank transfer (automatic)", 
        "Credit card (automatic)"
    ] = Field(..., description="Método de pagamento")
    OnlineSecurity: Literal["Yes", "No", "No internet service"] = Field(
        ..., description="Possui segurança online"
    )
    TechSupport: Literal["Yes", "No", "No internet service"] = Field(
        ..., description="Possui suporte técnico"
    )
    PaperlessBilling: Literal["Yes", "No"] = Field(
        ..., description="Fatura digital"
    )
    SeniorCitizen: int = Field(..., ge=0, le=1, description="É idoso (0 ou 1)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "tenure": 12,
                "MonthlyCharges": 75.00,
                "TotalCharges": 900.00,
                "Contract": "Month-to-month",
                "InternetService": "DSL",
                "PaymentMethod": "Electronic check",
                "OnlineSecurity": "No",
                "TechSupport": "No",
                "PaperlessBilling": "Yes",
                "SeniorCitizen": 0
            }
        }
    }


class PredictionResponse(BaseModel):
    """Resposta da predição de churn."""
    
    predicao: str = Field(..., description="Predição: 'Yes' (vai cancelar) ou 'No' (não vai cancelar)")
    probabilidade_churn: float = Field(..., description="Probabilidade de churn (0-1)")
    nivel_risco: str = Field(..., description="Nível de risco: ALTO, MÉDIO ou BAIXO")
    acao_recomendada: str = Field(..., description="Ação recomendada para retenção")


class BatchInput(BaseModel):
    """Dados de entrada para predição em lote."""
    clientes: list[ClienteInput] = Field(..., description="Lista de clientes para predição")


class BatchResponse(BaseModel):
    """Resposta da predição em lote."""
    resultados: list[PredictionResponse]
    total_clientes: int
    resumo: dict


def preparar_dados(cliente: ClienteInput) -> pd.DataFrame:
    """
    Prepara os dados do cliente para predição.
    
    Aplica One-Hot Encoding e garante que as colunas estão
    na mesma ordem esperada pelo modelo.
    """
    # Criar DataFrame com os dados
    df = pd.DataFrame([cliente.model_dump()])
    
    # Aplicar One-Hot Encoding
    df_encoded = pd.get_dummies(df, drop_first=True)
    
    # Garantir que todas as colunas esperadas existem
    for col in feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    
    # Ordenar colunas na ordem esperada pelo modelo
    df_encoded = df_encoded[feature_columns]
    
    return df_encoded


def calcular_risco(probabilidade: float) -> tuple[str, str]:
    """
    Calcula o nível de risco e ação recomendada baseado na probabilidade.
    
    Args:
        probabilidade: Probabilidade de churn (0-1)
    
    Returns:
        Tuple com (nivel_risco, acao_recomendada)
    """
    if probabilidade >= 0.7:
        return (
            "ALTO",
            "AÇÃO URGENTE: Contato imediato, oferecer desconto de 25%, migrar para contrato anual"
        )
    elif probabilidade >= 0.4:
        return (
            "MÉDIO",
            "MONITORAR: Incluir em campanha de engajamento, oferecer upgrade de serviços"
        )
    else:
        return (
            "BAIXO",
            "MANTER: Cliente estável, continuar comunicação regular e programa de fidelidade"
        )


# Endpoints da API
@app.get("/health")
async def health_check():
    """
    Verifica o status da API e se o modelo está carregado.
    
    Returns:
        Status da API e informações do modelo
    """
    if modelo is None:
        return {
            "status": "unhealthy",
            "modelo_carregado": False,
            "mensagem": "Modelo não foi carregado"
        }
    
    return {
        "status": "healthy",
        "modelo_carregado": True,
        "tipo_modelo": type(modelo).__name__,
        "numero_features": len(feature_columns),
        "usa_scaler": scaler is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(cliente: ClienteInput):
    """
    Faz predição de churn para um único cliente.
    
    Args:
        cliente: Dados do cliente para predição
    
    Returns:
        Predição com probabilidade, nível de risco e ação recomendada
    """
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    # Preparar dados
    df_prepared = preparar_dados(cliente)
    
    # Aplicar scaler se necessário
    if scaler is not None:
        df_scaled = scaler.transform(df_prepared)
    else:
        df_scaled = df_prepared
    
    # Fazer predição
    predicao = modelo.predict(df_scaled)[0]
    probabilidade = modelo.predict_proba(df_scaled)[0][1]
    
    # Calcular risco
    nivel_risco, acao = calcular_risco(probabilidade)
    
    return PredictionResponse(
        predicao=predicao,
        probabilidade_churn=round(probabilidade, 4),
        nivel_risco=nivel_risco,
        acao_recomendada=acao
    )


@app.post("/predict/batch", response_model=BatchResponse)
async def predict_batch(batch: BatchInput):
    """
    Faz predição de churn para múltiplos clientes.
    
    Args:
        batch: Lista de clientes para predição
    
    Returns:
        Lista de predições e resumo estatístico
    """
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    if not batch.clientes:
        raise HTTPException(status_code=400, detail="Lista de clientes vazia")
    
    resultados = []
    riscos = {"ALTO": 0, "MÉDIO": 0, "BAIXO": 0}
    
    for cliente in batch.clientes:
        # Preparar dados
        df_prepared = preparar_dados(cliente)
        
        # Aplicar scaler se necessário
        if scaler is not None:
            df_scaled = scaler.transform(df_prepared)
        else:
            df_scaled = df_prepared
        
        # Fazer predição
        predicao = modelo.predict(df_scaled)[0]
        probabilidade = modelo.predict_proba(df_scaled)[0][1]
        nivel_risco, acao = calcular_risco(probabilidade)
        
        # Contar riscos
        riscos[nivel_risco] += 1
        
        resultados.append(PredictionResponse(
            predicao=predicao,
            probabilidade_churn=round(probabilidade, 4),
            nivel_risco=nivel_risco,
            acao_recomendada=acao
        ))
    
    return BatchResponse(
        resultados=resultados,
        total_clientes=len(batch.clientes),
        resumo={
            "alto_risco": riscos["ALTO"],
            "medio_risco": riscos["MÉDIO"],
            "baixo_risco": riscos["BAIXO"],
            "percentual_alto_risco": round(riscos["ALTO"] / len(batch.clientes) * 100, 1)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
