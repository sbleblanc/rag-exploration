# RAG Exploration
The goal of this project id to build various proofs of concept to better understand RAG, RAG optimizations and TextGrad (and similar).

## Current Scope
The current scope of the project is to build a RAG pipeline to answer question about Project Diablo 2. The idea is to:

1. Dump the [wiki](https://wiki.projectdiablo2.com/wiki/Main_Page)
2. Convert the XML dump to legible documents
3. Encode the documents using an embedding model and save it to a vector database
4. Use an open-source LLM to query information

This is an experimentation project, os it will most likely not be released as a fully tested and documented project. Good practice will still be applied as time permits, but some things might be more "rugged".

### Data
I want to use DVC to build a data processing pipeline to fetch and convert to documents. Since I'm all out of storage space, the remote use is simply local. I will eventually port the data online so the project can be reproduced.

### Vector Database
As this is still a very low-scale project, I might use [sqlite-vec](https://github.com/asg017/sqlite-vec) to avoid having to run a service (e.g. [ChromaDB](https://www.trychroma.com/)). This way everything will be "self-contained" and the sqlite database can even be built and tracked with DVC.

### Embedding Model
Not sure yet, will have to find one with a relatively small size and trained on a task that works well with the data I intend to use.

### LLM
I was experimenting with Mistral-7b and phi3.5 with rough prompts, which made them hallucinate both really bad. Having only 8GB of VRAM, I'd prefer a smaller model and since the data is fairly specific.