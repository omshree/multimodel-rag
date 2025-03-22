import json
import chromadb
import numpy as np
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from sentence_transformers import CrossEncoder
from symspellpy import SymSpell

from sklearn.metrics.pairwise import cosine_similarity




embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en")
re_ranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L2-v2")

chroma_client = chromadb.PersistentClient(path="./chroma_db")



# spelling correction
sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)

def correct_spelling(text):
    suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
    return suggestions[0].term if suggestions else text


def index_documents(json_file):
    try:
        collection = chroma_client.get_collection(name="papers-metadata")
        print('found existing collection')
        
    except:
        collection = chroma_client.get_or_create_collection(name="papers-metadata")
        print('Creating new collection')
        with open(json_file, "r") as file:
            papers = json.load(file)

        for paper in papers.values():
            doc_id = paper["id"]
            text = f"The paper with title as {paper['title']} written by {paper['authors']}. This paper talks about:\n {paper['abstract']}"
            embedding = embed_model.get_text_embedding(text)

            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{"title": paper["title"], "abstract": paper["abstract"], "authors": paper["authors"]}],
            )
    return collection


def search(query, collection, top_k=5):
    query = correct_spelling(query)
    query_embedding = embed_model.get_text_embedding(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    docs = [res for res in results["documents"][0]]
    return docs

def rerank(docs):
    query_doc_pairs = [[query, doc] for doc in docs]
    scores = re_ranker.predict(query_doc_pairs)

    ranked_docs = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)
    return ranked_docs

def weighted_sum(lst):
    return sum(value / (index + 1) for index, value in enumerate(lst))/len(lst)

def cosine_w_rank(query, docs, ranked_docs):
    query_embedding = embed_model.get_text_embedding(query)
    docs_embeddings = np.array([embed_model.get_text_embedding(doc) for doc in docs])
    ranked_docs_embeddings = np.array([embed_model.get_text_embedding(doc) for doc in ranked_docs])

    docs_similarities = cosine_similarity([query_embedding], docs_embeddings)[0]

    ranked_docs_similarities = cosine_similarity([query_embedding], ranked_docs_embeddings)[0]

    return weighted_sum(docs_similarities), weighted_sum(ranked_docs_similarities)



if __name__ == "__main__":
    collection = index_documents("../data/arxiv-metadata-snapshot.json")

    query = input("Search query: ")

    docs = search(query, collection)
    print('Without rerank top 5 results\n')
    print(docs[0])
    
    ranked_docs = rerank(docs)
    print('With rerank top 5 results\n')
    print(ranked_docs[0][1])

    print(cosine_w_rank(query, docs, [docs[1] for docs in ranked_docs]))
