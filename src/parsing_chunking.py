import os
import chromadb
from llama_index.readers.file import MarkdownReader

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.node_parser import SentenceSplitter, HierarchicalNodeParser # :TODO implement the Hierarchical
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.extractors import TitleExtractor

import chromadb
import nest_asyncio
nest_asyncio.apply()

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en")

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=50),
        # TitleExtractor(), :TODO
        # embed_model(), :TODO
    ]
)

import fitz

def parse_pdf_to_markdown(pdf_path, output_md="./data/parsed_output.md"):
    doc = fitz.open(pdf_path)
    md_content = ""

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        tables = page.find_tables()

        md_content += f"\n## Page {page_num + 1}\n\n{text}\n"

        for table in tables:
            md_content += "\n\n### Table\n"
            md_content += str(table.to_pandas())
            md_content += "\n\n"

    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    print(f"Extracted content saved in {output_md}")
    return output_md


def process_md_file(file_path):
    nodes = []

    documents = MarkdownReader().load_data(file_path)
    file_nodes = pipeline.run(documents=documents)

    for node in file_nodes:
        node.metadata = {"folder_path": file_path}
        nodes.append(node)

    return nodes


def get_index_from_collection(collection_name):
    chroma_client = chromadb.PersistentClient(path="../chroma_db")

    print('collection is not found.. creating new')
    collection = chroma_client.get_or_create_collection(name=collection_name)

    # Read and Store Markdown Files
    pdf_file = "data/Portfolio-Analysis-Sample.pdf"
    file_path = parse_pdf_to_markdown(pdf_file)  
     
    nodes = process_md_file(file_path)  
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    doc_index = VectorStoreIndex(
        nodes, storage_context=storage_context, embed_model=embed_model, show_progress=True
    )

    return doc_index

