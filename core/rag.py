from langchain_chroma import Chroma  # Mudança aqui
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage  # Novo import
from typing import Dict, List
from core.config import settings
from core.llm import get_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=settings.OPENAI_API_KEY
)
llm = get_llm()

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="history",
    input_key="question",
    output_key="response"
)

prompt_template = """
Você é um assistente que responde perguntas sobre documentos trabalhistas em formato JSON. 
Sua resposta deve ser um JSON válido com a estrutura:
{{"resposta": "sua_resposta", "fontes": ["fonte1", "fonte2"]}}

Histórico da conversa: 
{history}

Documentos disponíveis:
{context}

Responda APENAS com um JSON válido.

Pergunta: {question}
"""
prompt = PromptTemplate.from_template(prompt_template)

vector_store = Chroma(
    persist_directory=settings.CHROMA_PATH,
    collection_name=settings.COLLECTION_NAME,
    embedding_function=embeddings
)


def get_rag_response(question: str, top_k: int = 2) -> Dict[str, List]:
    try:
        logger.info(f"Processando pergunta: {question}")

        docs = vector_store.similarity_search(query=question, k=top_k)
        logger.info(f"Documentos encontrados: {len(docs)}")

        if not docs:
            return {
                "response": "Não encontrei informações relevantes nos documentos.",
                "sources": []
            }

        relevant_docs = [
                            doc for doc in docs
                            if any(keyword in doc.page_content.lower()
                                   for keyword in question.lower().split())
                        ] or docs[:1]

        context = "\n\n".join(
            f"Documento {i + 1} ({doc.metadata.get('sindicato', 'Sem identificação')}):\n"
            f"{doc.page_content[:300]}{'...' if len(doc.page_content) > 300 else ''}"
            for i, doc in enumerate(relevant_docs))

        # 4. Prepara histórico (atualizado para nova versão)
        history = "\n".join([
            f"Usuário: {msg.content}" if isinstance(msg, HumanMessage)
            else f"Assistente: {msg.content}"
            for msg in memory.chat_memory.messages[-4:]
        ])

        chain = prompt | llm
        response = chain.invoke({
            "context": context,
            "question": question,
            "history": history
        })

        memory.save_context(
            {"question": question},
            {"response": response.content}
        )

        return {
            "response": response.content.strip(),
            "sources": [{
                "content": doc.page_content[:300] + ("..." if len(doc.page_content) > 300 else ""),
                "source": f"{doc.metadata.get('sindicato', 'Fonte')} - {doc.metadata.get('estado', '')}"
            } for doc in relevant_docs]
        }

    except Exception as e:
        logger.error(f"Erro no RAG: {str(e)}", exc_info=True)
        return {
            "response": "Ocorreu um erro ao processar sua solicitação.",
            "sources": []
        }