"""
Testes para a API de Predição de Churn.
"""

import pytest
from fastapi.testclient import TestClient
from api.app import app, carregar_modelo

# Carregar modelo antes dos testes
carregar_modelo()

client = TestClient(app)


class TestHealthEndpoint:
    """Testes para o endpoint /health."""
    
    def test_health_check_returns_200(self):
        """Verifica se o endpoint de health retorna status 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_model_loaded(self):
        """Verifica se o modelo foi carregado corretamente."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert data["modelo_carregado"] is True
        assert data["tipo_modelo"] == "LogisticRegression"


class TestPredictEndpoint:
    """Testes para o endpoint /predict."""
    
    def test_predict_high_risk_client(self):
        """Testa predição para cliente de alto risco."""
        cliente = {
            "tenure": 2,
            "MonthlyCharges": 89.99,
            "TotalCharges": 179.98,
            "Contract": "Month-to-month",
            "InternetService": "Fiber optic",
            "PaymentMethod": "Electronic check",
            "OnlineSecurity": "No",
            "TechSupport": "No",
            "PaperlessBilling": "Yes",
            "SeniorCitizen": 0
        }
        
        response = client.post("/predict", json=cliente)
        assert response.status_code == 200
        
        data = response.json()
        assert "predicao" in data
        assert "probabilidade_churn" in data
        assert "nivel_risco" in data
        assert "acao_recomendada" in data
        assert data["predicao"] in ["Yes", "No"]
        assert 0 <= data["probabilidade_churn"] <= 1
    
    def test_predict_low_risk_client(self):
        """Testa predição para cliente de baixo risco."""
        cliente = {
            "tenure": 60,
            "MonthlyCharges": 55.00,
            "TotalCharges": 3300.00,
            "Contract": "Two year",
            "InternetService": "DSL",
            "PaymentMethod": "Credit card (automatic)",
            "OnlineSecurity": "Yes",
            "TechSupport": "Yes",
            "PaperlessBilling": "No",
            "SeniorCitizen": 1
        }
        
        response = client.post("/predict", json=cliente)
        assert response.status_code == 200
        
        data = response.json()
        assert data["nivel_risco"] == "BAIXO"
        assert data["probabilidade_churn"] < 0.4
    
    def test_predict_invalid_contract(self):
        """Testa validação de contrato inválido."""
        cliente = {
            "tenure": 12,
            "MonthlyCharges": 75.00,
            "TotalCharges": 900.00,
            "Contract": "Invalid",
            "InternetService": "DSL",
            "PaymentMethod": "Electronic check",
            "OnlineSecurity": "No",
            "TechSupport": "No",
            "PaperlessBilling": "Yes",
            "SeniorCitizen": 0
        }
        
        response = client.post("/predict", json=cliente)
        assert response.status_code == 422
    
    def test_predict_missing_field(self):
        """Testa validação de campo faltando."""
        cliente = {
            "tenure": 12,
            "MonthlyCharges": 75.00
            # Missing required fields
        }
        
        response = client.post("/predict", json=cliente)
        assert response.status_code == 422
    
    def test_predict_invalid_tenure(self):
        """Testa validação de tenure negativo."""
        cliente = {
            "tenure": -5,
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
        
        response = client.post("/predict", json=cliente)
        assert response.status_code == 422


class TestBatchPredictEndpoint:
    """Testes para o endpoint /predict/batch."""
    
    def test_batch_predict_multiple_clients(self):
        """Testa predição em lote para múltiplos clientes."""
        batch = {
            "clientes": [
                {
                    "tenure": 2,
                    "MonthlyCharges": 89.99,
                    "TotalCharges": 179.98,
                    "Contract": "Month-to-month",
                    "InternetService": "Fiber optic",
                    "PaymentMethod": "Electronic check",
                    "OnlineSecurity": "No",
                    "TechSupport": "No",
                    "PaperlessBilling": "Yes",
                    "SeniorCitizen": 0
                },
                {
                    "tenure": 60,
                    "MonthlyCharges": 55.00,
                    "TotalCharges": 3300.00,
                    "Contract": "Two year",
                    "InternetService": "DSL",
                    "PaymentMethod": "Credit card (automatic)",
                    "OnlineSecurity": "Yes",
                    "TechSupport": "Yes",
                    "PaperlessBilling": "No",
                    "SeniorCitizen": 1
                }
            ]
        }
        
        response = client.post("/predict/batch", json=batch)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_clientes"] == 2
        assert len(data["resultados"]) == 2
        assert "resumo" in data
    
    def test_batch_predict_empty_list(self):
        """Testa erro para lista vazia de clientes."""
        batch = {"clientes": []}
        
        response = client.post("/predict/batch", json=batch)
        assert response.status_code == 400
    
    def test_batch_predict_summary(self):
        """Testa se o resumo é calculado corretamente."""
        batch = {
            "clientes": [
                {
                    "tenure": 60,
                    "MonthlyCharges": 55.00,
                    "TotalCharges": 3300.00,
                    "Contract": "Two year",
                    "InternetService": "DSL",
                    "PaymentMethod": "Credit card (automatic)",
                    "OnlineSecurity": "Yes",
                    "TechSupport": "Yes",
                    "PaperlessBilling": "No",
                    "SeniorCitizen": 1
                }
            ]
        }
        
        response = client.post("/predict/batch", json=batch)
        assert response.status_code == 200
        
        data = response.json()
        resumo = data["resumo"]
        assert "alto_risco" in resumo
        assert "medio_risco" in resumo
        assert "baixo_risco" in resumo
        assert "percentual_alto_risco" in resumo


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
