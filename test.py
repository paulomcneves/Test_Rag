from core.rag import get_rag_response

def run_test():
    print("=== TESTE CONSOLIDADO ===")

    # Teste 1: Pergunta inicial
    print("\n1. Testando recuperação básica...")
    test_question = "Quais valores de salário são mencionados?"
    result = get_rag_response(test_question)

    print(f"\n🔍 Pergunta: {test_question}")
    print(f"\n💡 Resposta: {result['response']}")

    if result.get('sources'):
        print("\n📄 Fontes encontradas:")
        for i, source in enumerate(result['sources'], 1):
            print(f"{i}. {source['content'][:100]}...")
    else:
        print("\n❌ Nenhuma fonte encontrada!")

    # Teste 2: Continuidade com o histórico embutido na memória
    print("\n2. Testando continuidade...")
    follow_up = "E para auxiliares de produção?"
    follow_result = get_rag_response(follow_up)

    print(f"\n🔍 Follow-up: {follow_up}")
    print(f"\n💡 Resposta: {follow_result['response']}")

if __name__ == "__main__":
    run_test()
