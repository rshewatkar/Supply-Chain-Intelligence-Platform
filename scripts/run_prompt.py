from app.rag.prompts import PromptBuilder

def main():
    print("=" *60)
    print("Supply Chain Intelligence Platform")
    print("RAG Prompt Builder")
    print("=" *60)
    
    question = input(
        ":\nEnter your question: "
        ).strip()
    
    if not question:
        print("Question cannot be empty.")
        return
    
    context = input(
        ":\nEnter retrieved context: "
        ).strip()
    
    if not context:
        print("Context cannot be empty.")
        return
    
    builder = PromptBuilder()
    
    prompt = builder.build(
        question=question,
        context=context,)
    
    print("\n" +"=" *60)
    print("Generated Prompt:")
    print("=" *60)
    
    print(prompt)
    
    print("\n" + "=" *60)
    print("Prompt Builder Completed")
    print("=" *60)
    
if __name__ == "__main__":
    main()
          