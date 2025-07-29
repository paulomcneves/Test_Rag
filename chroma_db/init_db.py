import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings  # Mudança aqui
from langchain_core.documents import Document

load_dotenv()

convencoes_exemplo = [
    {
        "texto": "Convenção Coletiva 2023-2025 - Sindicato dos Metalúrgicos de MG\n\nCláusula 5ª - Salário Mínimo Profissional:\n- Operador de Máquinas: R$ 2.589,00\n- Auxiliar de Produção: R$ 1.985,00\n\nCláusula 12ª - Benefícios:\n- Vale-alimentação: R$ 800,00 mensais\n- Assistência médica: Cobrir 70% do plano",
        "metadata": {
            "sindicato": "Metalúrgicos",
            "estado": "MG",
            "ano_vigencia": 2023,
            "industria": "metalurgica"
        }
    },
    {
        "texto": "Acordo Coletivo 2024 - Sindicato dos Comerciários de SP\n\nArtigo 3º - Remuneração:\n- Piso salarial: R$ 1.850,00\n- Hora extra: 50% adicional\n\nArtigo 7º - Condições:\n- Jornada semanal: 44 horas\n- Descanso semanal remunerado",
        "metadata": {
            "sindicato": "Comerciários",
            "estado": "SP",
            "ano_vigencia": 2024,
            "industria": "comercio"
        }
    }
]

def criar_banco():
    if os.path.exists("data"):
        import shutil
        shutil.rmtree("data")
        print("♻️ Banco de dados antigo removido")

    documents = [
        Document(
            page_content=item["texto"],
            metadata=item["metadata"]
        ) for item in convencoes_exemplo
    ]

    db = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),  # Mudança crucial aqui
        persist_directory="data",
        collection_name="convencoes"
    )

    print(f"\n✅ Banco recriado com {len(documents)} convenções coletivas")
    print(f"📍 Local: data")
    print(f"🔧 Embedding model: text-embedding-ada-002")

if __name__ == "__main__":
    criar_banco()