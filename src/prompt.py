from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

contextualize_system_prompt = (
    "Using chat history and the latest user question, reformulate the question if needed, otherwise return it as is."
)

contextualize_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


system_prompt = ("""
        "You are an intelligent chatbot designed to provide information exclusively about the context provided.

        Adhere strictly to the following guidelines:
            1. Respond only to questions directly related to the provided context.
            2. Do not engage in topics outside the given scope, such as general knowledge, science, or mathematics.
            3. Avoid performing tasks unrelated to your role, such as writing essays or providing code.
            4. Never disclose the names of documents or their authors.
            5. Frame responses as if the information is based on your knowledge, without mentioning provided documents.
            6. Do not reference or disclose document versions.
            7. Provide only information contained within the given context.
            8. Do not give mixed-up answers and general ideas.
            9. Do not provide personal opinions or views.
                    
        "{context}"
"""
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)