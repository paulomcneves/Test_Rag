import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def test_query(question, expected_keywords=None):
    print(f"\n🔵 Pergunta: {question}")
    response = requests.post(
        f"{BASE_URL}/query",
        json={"text": question}
    )

    if response.status_code == 200:
        data = response.json()
        print(f"🟢 Resposta: {data['response']}")

        if data['sources']:
            print("\n📄 Documentos consultados:")
            for i, source in enumerate(data['sources'], 1):
                print(f"{i}. {source['source']}")
                print(f"   Trecho: {source['content'][:100]}...")

        if expected_keywords:
            if any(keyword.lower() in data['response'].lower() for keyword in expected_keywords):
                print("✅ Palavras-chave encontradas na resposta")
            else:
                print("❌ Palavras-chave NÃO encontradas")
    else:
        print(f"🔴 Erro: {response.status_code} - {response.text}")

    time.sleep(1)  # Intervalo entre requisições
    return data['response']


# Sequência de testes
if __name__ == "__main__":
    print("🚀 Iniciando testes da API RAG...\n")

    # Teste 1: Consulta simples
    test_query("Qual é o salário mínimo para Operador de Máquinas em MG?", ["R$ 2.589,00"])

    # Teste 2: Consulta com contexto diferente
    test_query("Qual o piso salarial para comerciários em SP?", ["R$ 1.850,00"])

    # Teste 3: Consulta com histórico (deve lembrar do contexto anterior)
    test_query("E quais são os benefícios para esse profissional?", ["vale-alimentação", "assistência médica"])

    # Teste 4: Consulta genérica (testando fallback)
    test_query("Resuma os principais pontos da convenção dos metalúrgicos", ["Cláusula", "Salário", "Benefícios"])

    # Teste 5: Consulta sem resposta no documento
    test_query("Qual o valor do vale-transporte?", ["não encontrei", "informações relevantes"])

    print("\n🧪 Testes concluídos!")