# EcoWissen Freiburg - Sustainability RAG System

A Retrieval-Augmented Generation (RAG) system designed to provide intelligent responses about sustainability initiatives and environmental data for Freiburg City. The system combines document retrieval with advanced language models to deliver accurate, context-aware information in both English and German.

## 🌟 Features

- **Bilingual Support**: Full support for English and German interactions
- **Smart Document Retrieval**: Uses vector similarity search to find relevant information
- **Advanced Language Model**: Powered by Meta-Llama-3-8B-Instruct
- **Environmental Awareness**: Tracks and displays carbon footprint of interactions
- **Export Capabilities**: Export conversations to PDF format
- **Fine-tuned Responses**: Custom-trained model for sustainability-related queries

## 🏗️ Architecture

### Backend (RAG-backend/)
- Flask-based API server
- Document processing and retrieval system
- Integration with Chroma vector database
- Custom utilities for reference cleaning and formatting

### Frontend (RAG-frontend/)
- Streamlit-based chat interface
- Bilingual UI with language switching
- Conversation management and export features
- Carbon footprint visualization

### Fine-tuning Pipeline (finetune/)
- Training data preparation scripts
- Model fine-tuning configurations
- Based on OpenLlama 3B architecture
- Q&A pair processing utilities

## 🛠️ Technical Stack

- **Language Models**: Meta-Llama-3-8B-Instruct, OpenLlama 3B
- **Vector Store**: Chroma DB
- **Embeddings**: BAAI/bge-large-en-v1.5
- **Frontend**: Streamlit
- **Backend**: Flask
- **Document Processing**: LangChain
- **ML Framework**: PyTorch, Transformers

## 📋 Requirements

## 🚀 Getting Started

1. **Clone the Repository**

```bash
git clone [repository-url]
cd ecowissen-freiburg
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Start the Backend Server**

```bash
cd RAG-backend
python chatbot.py
```

4. **Launch the Frontend**

```bash
cd RAG-frontend
streamlit run streamlit-chat.py
```

## 📁 Project Structure

```
.
├── RAG-backend/
│   ├── chatbot.py          # Main backend server
│   ├── utils.py            # Utility functions
│   └── database/           # Vector database storage
├── RAG-frontend/
│   ├── streamlit-chat.py   # Frontend interface
│   └── translations.py     # Language translations
├── finetune/
│   ├── prepare_training_data.py
│   └── configs/            # Training configurations
└── requirements.txt
```

## 🌍 Environmental Impact

The system includes built-in carbon footprint tracking to promote awareness of computational resource usage. This aligns with the project's focus on sustainability and environmental consciousness.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Add License Information]

## 📞 Contact

[Add Contact Information]

---

Built with 💚 for a sustainable future in Freiburg
