from typing import List
from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Qdrant
from langchain.chains import ConversationalRetrievalChain
from langserve import add_routes
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
import os
import logging  # Importa el módulo logging

# Load environment variables
load_dotenv()

# Configuración del logging
logging.basicConfig(level=logging.INFO)  # Configura el nivel de logging a DEBUG
logger = logging.getLogger(__name__)  # Crea un logger

# --- Configuración de Credenciales ---
# Elimina los valores por defecto
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_CLOUD_URL = os.getenv("QDRANT_CLOUD_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Vademecum RAG Chat",
    description="A RAG-based chat system for medical information using LangChain and ChatGPT"
)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Initialize vector store with sample data
def initialize_vectorstore():
 # --- Inicialización del Vector Store ---
    try:
        qdrant_client = QdrantClient(url=QDRANT_CLOUD_URL, api_key=QDRANT_API_KEY)
        
        # Verificar existencia de la colección
        collection_name = "vademecum_medicamentos_en"  # Define collection name as a constant
        collection_info = qdrant_client.get_collection(collection_name)
        logger.info(f"Usando colección existente: {collection_name}")
        
        # Inicializar vectorstore para consultas
        vectorstore = QdrantVectorStore(
            client=qdrant_client,
            collection_name=collection_name,
            embedding=embeddings
        )

    except Exception as e:
        logger.error("Error al acceder a Qdrant: %s", e)
        raise SystemExit("No se puede conectar a Qdrant") from e

    return vectorstore

# Initialize the chat model and chain
def initialize_chain():
    vectorstore = initialize_vectorstore()
    llm = ChatOpenAI(temperature=0)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    return chain

# Lazy initialization of the chain
chain = None

@app.get("/chat")
async def chat_endpoint():
    global chain
    if chain is None:
        chain = initialize_chain()
    return chain

@app.get("/health")
def health_check():
    try:
        # Test Qdrant connection
        qdrant_client = QdrantClient(url=QDRANT_CLOUD_URL, api_key=QDRANT_API_KEY)
        collection_name = "vademecum_medicamentos_en"
        collection_info = qdrant_client.get_collection(collection_name)
        logger.info("Health check passed: Qdrant connection successful")
        return {"status": "healthy", "message": "All services operational"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}

# Add routes to the app
add_routes(
    app,
    initialize_chain(),  # Initialize the chain before adding routes
    path="/chat"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)