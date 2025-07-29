# test_rag_system.py
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()


# 1. Testar conexão com OpenAI
def test_openai_connection():
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        response = llm.invoke("Responda com apenas a palavra 'OK'")
        print(f"✅ Teste OpenAI: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Falha OpenAI: {str(e)}")
        return False


# 2. Testar embeddings
def test_embeddings():
    try:
        embeddings = OpenAIEmbeddings()
        vector = embeddings.embed_query("Texto de teste")
        print(f"✅ Embeddings: Vetor de {len(vector)} dimensões gerado")
        return True
    except Exception as e:
        print(f"❌ Falha Embeddings: {str(e)}")
        return False


# 3. Testar vector store
def test_vector_store():
    try:
        embeddings = OpenAIEmbeddings()
        db = Chroma(
            persist_directory="chroma_db/data",
            embedding_function=embeddings,
            collection_name="convencoes"
        )
        docs = db.similarity_search("salário", k=1)
        print(f"✅ Vector Store: {len(docs)} documento(s) encontrado(s)")
        return True
    except Exception as e:
        print(f"❌ Falha Vector Store: {str(e)}")
        return False


# 4. Teste completo do RAG
def test_rag_pipeline():
    from core.rag import get_rag_response

    questions = [
        "Qual é o salário mínimo para Operador de Máquinas em MG?",
        "Quais são os benefícios para metalúrgicos?"
    ]

    for question in questions:
        print(f"\n🔵 Pergunta: {question}")
        result = get_rag_response(question)
        print(f"🟢 Resposta: {result['response']}")
        if result['sources']:
            print("📄 Fontes:")
            for src in result['sources']:
                print(f"- {src['source']}")


if __name__ == "__main__":
    print("🚀 Iniciando testes do sistema RAG...\n")

    if test_openai_connection() and test_embeddings() and test_vector_store():
        print("\n🔥 Todos os testes básicos passaram! Verificando pipeline completo...")
        test_rag_pipeline()
    else:
        print("\n❌ Corrija os problemas básicos antes de testar o pipeline completo")