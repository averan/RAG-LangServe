# Vademecum RAG Chat

A RAG-based chat system for medical information using LangChain and ChatGPT. This system provides a conversational interface to access medical information from a Vademecum database.

## Features

- FastAPI-based REST API
- RAG (Retrieval Augmented Generation) implementation
- Integration with OpenAI's ChatGPT
- Qdrant vector database for efficient similarity search
- Docker support for easy deployment
- Health check endpoint

## Prerequisites

- Python 3.11+
- OpenAI API Key
- Qdrant Cloud account and credentials

## Environment Setup

1. Clone the repository:
```bash
git clone [your-repo-url]
cd vademecum-rag-chat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your credentials:
```
OPENAI_API_KEY=your_openai_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CLOUD_URL=your_qdrant_cloud_url
```

## Running the Application

### Local Development

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
docker build -t vademecum-rag .
docker run -p 8000:8000 --env-file .env vademecum-rag
```

## API Endpoints

- `/chat`: Main endpoint for the chat interface
- `/health`: Health check endpoint

## Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.