import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI 
from langchain.llms import HuggingFaceHub 
from langchain.chat_models import ChatOpenAI
from htmlTemplate import css, bot_template, user_template


# note streamlit page config must be at the top
st.set_page_config(page_title = "Chat with multiple PDFs", page_icon=":books:")
# like the website or page need to add css add topn the 
# the cass will add the css code on top of streamlit app page
# css will place the html components
# then htmls components like user, bot templates will communicate with the query and answer 
st.write(css, unsafe_allow_html=True) 


def get_pdf_text(pdf_docs):
    '''
    GET PDF FROM TEXT
    '''
    # will store all text from the pdfs
    text = ""
    for pdf in pdf_docs:
        # create pdf reader object initialized with the pdf input
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            # extract text from each page
            text += page.extract_text()

    return text


def get_text_chunks(raw_text):
    '''
    OBTAIN CHUNKS FROM RAW TEXT
    '''
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len # the length function for chunk is the len() from python
    )

    # split texts
    chunks = text_splitter.split_text(raw_text)
    # returns list of chunks
    return chunks


def get_vectorstore(text_chunks):
    '''
    CREATE VECTORSTORE
    '''
    #embeddings = OpenAIEmbeddings()

    # implement Instructor embedding as open source model
    #embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-large")
    #embeddings = HuggingFaceInstructEmbeddings()
    embeddings = HuggingFaceEmbeddings()

    # create vectorstroe
    vectorstore = FAISS.from_texts(
        texts = text_chunks,
        embedding = embeddings
    )

    return vectorstore


def get_conversation_chain(vectorstore):
    '''
    CREATE LANGCHAIN CONVERSTATION CHAIN 
    '''
    # as we are creating a chatbot which has memory
    # thus inititalize memory object
    # set memory key and it will return message
    memory = ConversationBufferMemory(memory_key = "chat_history", return_messages = True)
    # llm = ChatOpenAI()

    # using open source model from huggingface
    llm = HuggingFaceHub(
        repo_id = "google/flan-t5-xxl",
        model_kwargs = {"temperature":0.5, "max_length":512})

    converstation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return converstation_chain


def handle_userinput(user_query):
    '''
    HANDLE USER QUERY
    '''
    response = st.session_state.conversation({'question':user_query}) 

    # create a new session state variable
    st.session_state.chat_history = response["chat_history"]

    # loop through chat history
    for i, message in enumerate(st.session_state.chat_history):
        if i%2 ==0:
            # here we streamlit write we passs user template as message
            # we need to print the content of the message only
            st.write(user_template.replace("{{MSG}}",message.content), unsafe_allow_html=True)
        else:
            # we write bot template
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html = True)

    return response



def main():
    # now langchain can acces the env variables retrieved by the above function
    '''
    GUI
    '''
    # st.set_page_config(page_title = "Chat with multiple PDFs", page_icon=":books:")
    # its a good practice to initialize session state variable
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # header of the page
    st.header("Chat with multiple PDFs :books:")

    load_dotenv()

    # we need to handle that user submission
    user_query = st.text_input("Ask a question about your documents:")

    if user_query:
        response = handle_userinput(user_query)
        

    st.write(user_template.replace("{{MSG}}","Hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello human"), unsafe_allow_html=True)
    
    # create sidebar for documnets upload
    with st.sidebar:
        # write the contents of sidebar
        st.subheader("Your documents!")
        # retrieves list of user pdf inputs
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on Process", accept_multiple_files=True)
        
    
        # to add logic to button clik operation
        if st.button("Process"):
            # while button process is pressed
            # a spinner will apppear as mentioned below
            with st.spinner("Processing"):
                # after spinner Processsing is esecuted the following functions will be executed

                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # shows the entire raw text in the sidebar

                # get the text chunks or splits
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks[:5])

                # create vectordb or vector store
                vectorstore = get_vectorstore(text_chunks)
                st.write("VECTORSTORE CREATED")

                # create conversation chain
                # it initializes a conversation chain
                # which takes llm as input
                # stores the previous conversation in memorybuffer
                # it has retriever object, which helps to retrieve based on the prompt generated(current query + memory) 
                # the send the relevant docs to the llm 
                
                # we have initialized conversation chain using a streamlit session_state varaible
                # the reason is we want this variable to be releavant outside the sidebar scope
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.write("CONVERSATION CHAIN CREATED")
                #st.write(HUGGINGFACE_API_TOKEN)

if __name__ == "__main__":
    # the purpose is whenever we will execute theis python file
    # the following functions will be executed
    main()