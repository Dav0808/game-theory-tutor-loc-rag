from src.rag_pypeline import ask_question


def main():
    while True:
        question = input("\nAsk a game theory question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        answer = ask_question(question)
        print("\nTutor:", answer)

if __name__ == "__main__":
    main()
