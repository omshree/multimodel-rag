from retrieve import query_rag_system

# Initialize the chat messages history
messages = [{"role": "assistant", "content": "How can I help?"}]


def query_expansion(messages, query):
    # print(messages)
    exp_query = '\n'.join([f"'role': {m['role']}, 'content': {m['content']}" for m in messages])

    query_xp = exp_query+f' Now based on previous chat please provide the answer for query: {query}\n Answer:'
    return query_xp

if __name__=="__main__":
    while True:
        prompt = input("User: ")
        
        query = query_expansion(messages, prompt)
        # print(query)
        response = query_rag_system(query)
        print(response['content'])

        inp = input("do you want to continue or do you want to start over?: ")
        if inp =='start':
            messages = [{"role": "assistant", "content": "How can I help?"}]
        else:
            messages.append(response)
        
        
        