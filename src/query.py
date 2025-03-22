from retrieve import query_rag_system

# We plan to further enhance the RAG pipeline by incorporating the following improvements:

# TODO System prompt: We can define a correct system prompt for the system to apply some poloicies

# TODO Query Expansion - Expanding queries to improve retrieval.

# TODO Re-ranking Methods - Improving the ranking of retrieved documents.

# TODO Fusion Methods - Combining results from multiple retrieval strategies.

# TODO Metadata Filtering - Filtering retrieved documents based on metadata.

# :TODO Adding Metadata - Enriching documents with metadata for better context.

# Due to time constraints, we were unable to extensively implement these features, but we may explore them in the future.




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
        
        
        