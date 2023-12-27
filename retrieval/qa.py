from llm.resources import get_qa

qa = None

def get_answer(question, chat_history):
    global qa
    if qa == None:
        qa = get_qa()
    result = qa({'question': question, 'chat_history': chat_history})
    return result['answer']
