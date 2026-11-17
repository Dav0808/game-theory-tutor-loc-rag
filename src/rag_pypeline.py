from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from .helper_functions import format_docs
from .vector_store import vector_store
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Game Theory Tutor. Answer only using the supplied context."),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

question = "What is a Nash equilibrium?"


retriever = vector_store.as_retriever(search_kwargs={"k": 5})

chain_input = {
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
}

## instantiate LLM
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    reasoning=False,
    keep_alive="10m",
)

def ask_question(question):
    response = chain.invoke(question)
    return response.content

chain = chain_input | prompt | llm




