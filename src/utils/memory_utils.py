from langchain.memory import ConversationBufferMemory

def create_memory(input_key="input", output_key="output"):
    return ConversationBufferMemory(
        input_key=input_key,
        output_key=output_key,
        return_messages=True
    ) 