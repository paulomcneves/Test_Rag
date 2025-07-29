import pytest
from core.rag import get_rag_response
from unittest.mock import patch


@patch("core.rag.vector_store")
def test_get_rag_response(mock_vector_store):
    mock_doc = {
        "page_content": "Convenção teste: Salário R$ 1000",
        "metadata": {"industria": "teste"}
    }
    mock_vector_store.similarity_search.return_value = [mock_doc]

    result = get_rag_response("Qual o salário?")

    assert "R$ 1000" in result["response"]
    assert len(result["sources"]) == 1