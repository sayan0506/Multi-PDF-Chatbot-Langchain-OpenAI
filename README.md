# Multi-PDF-Chatbot-Langchain-OpenAI

Created a Multi-PDF chatbot, where we created a conversation chain using Langchain, where we input multiple pdfs, and search query related to those pdf in order to fetch reponse from the LLM. Components

1. RAG pipeline using langchain
2. FAISS vector database
3. Embedding models(OpenAI, HF)
4. Conversation chain having memory
5. OpenAI LLM model
6. Streamlit APP

In order to execute the pipeline through streamlit app, execute:

```bash
# Run the Streamlit app
streamlit run app.py

# UI

[image.jpg](https://github.com/sayan0506/Multi-PDF-Chatbot-Langchain-OpenAI/blob/main/images/Screenshot%20from%202024-08-26%2011-08-14.png)
