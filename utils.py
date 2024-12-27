from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from pypdf import PdfReader


def process_text(text):
    # Process the given text by splitting it into chunks and then converting
    # these chunks into embeddings and to form a knowledgebase

    # Initialise the Text splitter to divide the text into manageable chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    # Load a model for generating embeddings from HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-V2')
    # create a FAISS index from the text chunks using the embeddings
    knowledgeBase = FAISS.from_texts(chunks, embeddings)

    return knowledgeBase


def summarizer(pdf):

    # Function to summarize the content of a pdf file
    if pdf is not None:
        # Read the pdf file
        pdf_reader = PdfReader(pdf)
        text = ""

        # Extract the text from each page of the pdf
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        # Process the extracted text to create knowledge base
        knowledgeBase = process_text(text)

        # Define the query for Summarization
        query = "Summarize the content of the uploaded pdf file approximately 3-5 Sentences"

        if query:
            # Perform a similarity search in the knowledge base using the query
            docs = knowledgeBase.similarity_search(query)

            OpenAIModel = "gpt-3.5-turbo-16k"

            llm = ChatOpenAI(model=OpenAIModel,temperature=0.8)

            chain = load_qa_chain(llm,chain_type='stuff')

            response = chain.run(input_documents=docs, question=query)

            return response
