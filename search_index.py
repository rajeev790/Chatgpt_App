from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os

# Define schema for Whoosh
schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

# Create index directory if not exists
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

# Create index
ix = create_in("indexdir", schema)

# Add documents to index (use this for initialization or updates)
def add_document(title, content):
    writer = ix.writer()
    writer.add_document(title=title, content=content)
    writer.commit()

# Perform search
def search_documents(query_str):
    results = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        search_results = searcher.search(query)
        for result in search_results:
            results.append(result['title'])
    return results
