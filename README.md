# Bank of Ceylon (BOC) - Domain-Specific FAQ ChatBot 🏦

A sophisticated AI-powered chatbot designed specifically for Bank of Ceylon customers, providing instant answers to banking-related queries using Retrieval-Augmented Generation (RAG) technology.

## 🌟 Features

- **Intelligent FAQ System**: Powered by OpenAI's GPT-4o-mini and FAISS vector database
- **Conversational Memory**: Maintains context throughout chat sessions
- **Domain-Specific Knowledge**: Trained exclusively on Bank of Ceylon documentation
- **Multi-Interface Support**: Both web API and interactive Streamlit frontend
- **Real-time Responses**: Fast and accurate answers to banking queries
- **Session Management**: Individual user sessions with chat history
- **Secure & Reliable**: Built with FastAPI for robust API handling

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │   LangChain     │
│   Frontend      │◄──►│    Backend      │◄──►│   RAG Chain     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Session Store  │    │ FAISS Vector    │
                       │   (In-Memory)   │    │   Database      │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   BOC FAQ       │
                                              │   Documents     │
                                              └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API Key
- LangChain API Key (optional, for tracing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Advance-AI-Project---Domain-Specific-FAQ-ChatBot-
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   LANGCHAIN_API_KEY=your_langchain_api_key_here  # Optional
   ```

4. **Start the FastAPI backend**
   ```bash
   uvicorn app:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Launch the Streamlit frontend** (in a new terminal)
   ```bash
   streamlit run frontend/chat.py
   ```

6. **Access the application**
   - Streamlit UI: http://localhost:8501
   - API Documentation: http://localhost:8000/docs (if enabled)

## 📁 Project Structure

```
├── app.py                      # FastAPI backend server
├── setup.py                    # Package configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .env                        # Environment variables (create this)
├── src/
│   ├── llm.py                 # LangChain RAG implementation
│   ├── prompt.py              # System prompts and templates
│   ├── faiss_vectorstore.py   # Vector database setup
│   └── helper.py              # Document processing utilities
├── frontend/
│   └── chat.py                # Streamlit web interface
└── Docs/
    └── boc_chunks.jsonl       # BOC FAQ knowledge base
```

## 🔧 Configuration

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/query` | POST | Submit user queries |
| `/history/{session_id}` | GET | Get chat history |
| `/history/{session_id}` | DELETE | Clear chat history |

### Query Request Format

```json
{
  "session_id": "unique-session-identifier",
  "input": "How do I reset my internet banking password?"
}
```

### Response Format

```json
{
  "answer": "You can reset your password yourself using the 'Forgot Password' link available on the login screen."
}
```

## 🤖 How It Works

1. **Document Processing**: BOC FAQ documents are preprocessed and stored as embeddings in FAISS vector database
2. **Query Processing**: User queries are embedded using OpenAI's text-embedding-3-small model
3. **Retrieval**: Relevant document chunks are retrieved using similarity search
4. **Generation**: GPT-4o-mini generates contextual responses based on retrieved information
5. **Memory**: Conversation history is maintained for contextual follow-up questions

## 💡 Usage Examples

### Common Queries

- "How do I open an account with Bank of Ceylon?"
- "What are the BOC branch opening hours?"
- "How do I register for BOC Smart Online Banking?"
- "What should I do if my credit card is lost or stolen?"
- "Can I change my PIN?"
- "How do I contact customer service?"

### Quick Actions (Streamlit Interface)

The frontend provides quick action buttons for frequently asked questions:
- Account opening procedures
- Online banking registration
- Customer service contact
- Credit card applications
- PIN management
- Payment methods

## 🛠️ Development

### Adding New Knowledge

1. Update the `Docs/boc_chunks.jsonl` file with new FAQ content
2. Restart the application to reload the vector database

### Customizing Prompts

Edit the system prompts in `src/prompt.py` to modify the chatbot's behavior and response style.

### Extending Functionality

- **New Document Types**: Modify `src/helper.py` to support additional document formats
- **Different Embeddings**: Update `src/faiss_vectorstore.py` to use alternative embedding models
- **Enhanced UI**: Customize the Streamlit interface in `frontend/chat.py`

## 🔒 Security Features

- **Domain Restriction**: Responses are limited to BOC-specific information
- **Input Validation**: All user inputs are validated and sanitized
- **Session Isolation**: Each user session is isolated and secure
- **No External Data**: The system never uses external knowledge beyond the provided BOC documentation

## 📊 Performance

- **Response Time**: ~2-3 seconds for typical queries
- **Accuracy**: High precision on BOC-specific questions
- **Scalability**: Supports multiple concurrent users
- **Memory Efficient**: Optimized vector storage and retrieval

## 🐛 Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY is not set" Error**
   - Ensure your `.env` file contains a valid OpenAI API key

2. **FAISS Import Error**
   - Install faiss-cpu: `pip install faiss-cpu`

3. **Port Already in Use**
   - Change the port in the uvicorn command: `--port 8001`

4. **Streamlit Connection Error**
   - Ensure the FastAPI backend is running on the correct port

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section above

## 🔮 Future Enhancements

- [ ] Multi-language support (Sinhala, Tamil)
- [ ] Voice interface integration
- [ ] Advanced analytics dashboard
- [ ] Database persistence for chat history
- [ ] Enhanced document upload capabilities
- [ ] Mobile app development
- [ ] Integration with BOC's existing systems

---
