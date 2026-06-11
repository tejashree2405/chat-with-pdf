from services.rag_service import ask_question

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    result = ask_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    print(result["sources"])