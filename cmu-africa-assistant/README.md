# CMU-Africa Information Assistant 🎓

A comprehensive AI-powered information assistant for Carnegie Mellon University Africa (CMU-Africa) built with Streamlit, OpenAI GPT-4, and Pinecone vector database. This application uses Retrieval Augmented Generation (RAG) to provide accurate, contextually relevant responses about CMU-Africa.

## 🌟 Features

- **🤖 Intelligent Chat Interface**: Interactive chat interface powered by OpenAI GPT-4
- **🔍 RAG Pipeline**: Retrieval Augmented Generation with Pinecone vector search
- **💬 Chat History**: Persistent chat sessions with full conversation history
- **👍 Feedback System**: User feedback mechanism (thumbs up/down) for response quality
- **🔧 Admin Panel**: Knowledge base management and analytics dashboard
- **🌍 Multi-Language Support**: English, French (Français), and Kinyarwanda
- **📚 Sample Knowledge Base**: Pre-loaded with CMU-Africa information
- **📊 Analytics**: Feedback statistics and usage metrics
- **🔒 Secure Configuration**: Environment-based API key management

## 📋 Table of Contents

- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Features Details](#features-details)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🛠 Technology Stack

- **Frontend**: Streamlit 1.29.0
- **LLM**: OpenAI GPT-4
- **Vector Database**: Pinecone
- **Embeddings**: OpenAI text-embedding-3-small
- **Language**: Python 3.8+
- **Database**: SQLite (for chat history and feedback)

## 📦 Prerequisites

Before you begin, ensure you have the following:

1. **Python 3.8 or higher** installed on your system
2. **OpenAI API Key**: Sign up at [OpenAI](https://platform.openai.com/) and create an API key
3. **Pinecone Account**: Sign up at [Pinecone](https://www.pinecone.io/) and create:
   - API Key
   - Environment name (e.g., `us-east-1`)
   - Note: The application will automatically create the index if it doesn't exist

## 🚀 Installation

### Step 1: Clone or Download the Repository

```bash
# If using git
git clone <repository-url>
cd cmu-africa-assistant

# Or download and extract the ZIP file, then navigate to the directory
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Method 1: Using Environment Variables (Recommended for Production)

1. Copy the `.env.template` file to `.env`:

```bash
cp .env.template .env
```

2. Edit the `.env` file and add your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Pinecone Configuration
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=cmu-africa-knowledge-base

# Application Configuration
APP_TITLE=CMU-Africa Information Assistant
APP_LANGUAGE=en
DEBUG_MODE=False
```

### Method 2: Using the Web Interface (For Testing)

You can also configure API keys directly through the Streamlit interface:

1. Run the application (see next section)
2. Enter your API keys in the sidebar
3. Click "Save Configuration"

**Note**: Web interface configuration is session-based and won't persist across restarts.

## 🎯 Running the Application

### Start the Application

```bash
streamlit run app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`.

### First-Time Setup

When you first run the application:

1. **Configure API Keys**:
   - If using `.env` file: Keys will be loaded automatically
   - If using web interface: Enter keys in the sidebar and click "Save Configuration"

2. **Initial Knowledge Base Loading**:
   - The application will automatically load sample CMU-Africa data into Pinecone
   - This may take a few seconds on first run
   - You'll see a success message when complete

3. **Start Chatting**:
   - Type your questions in the chat input
   - The assistant will provide responses based on the knowledge base

## 📖 Usage Guide

### Main Chat Interface

1. **Ask Questions**:
   ```
   - "What are the shuttle bus timings?"
   - "What Master's programs does CMU-Africa offer?"
   - "Tell me about the MSEAI program"
   - "How can I apply for scholarships?"
   ```

2. **View Sources**:
   - Click on "📚 Sources" below any response to see the retrieved context

3. **Provide Feedback**:
   - Click 👍 or 👎 to rate responses
   - Helps improve the system over time

4. **Change Language**:
   - Select language from the sidebar dropdown
   - Available: English, Français, Kinyarwanda

5. **Manage Chat Sessions**:
   - Click "➕ New Chat" to start a new conversation
   - View and load previous sessions from the sidebar
   - Delete old sessions with the 🗑️ button

### Admin Panel

Access the admin panel from the sidebar navigation or by going to the "Admin Panel" page.

#### Knowledge Base Management

1. **Add Single Document**:
   - Fill in the form with document details
   - Click "Upload to Knowledge Base"

2. **Bulk Upload**:
   - Prepare a JSON file with documents (see format below)
   - Upload the file
   - Click "Upload All Documents"

3. **Delete Documents**:
   - Enter the document ID
   - Click "Delete Document"

**JSON Format for Bulk Upload**:
```json
[
  {
    "id": "unique_doc_id",
    "title": "Document Title",
    "category": "Category Name",
    "content": "Document content goes here...",
    "keywords": ["keyword1", "keyword2"]
  }
]
```

#### View Feedback

- See feedback statistics (positive/negative ratio)
- Browse recent feedback with filters
- Export feedback data as CSV

## 📁 Project Structure

```
cmu-africa-assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env.template                   # Environment variables template
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── data/
│   ├── cmu_africa_knowledge_base.json  # Sample knowledge base
│   ├── chat_history.db            # Chat history database (auto-generated)
│   └── feedback.db                # Feedback database (auto-generated)
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── rag_pipeline.py        # RAG implementation
│   │   ├── chat_interface.py      # Chat management
│   │   └── feedback_handler.py    # Feedback system
│   └── utils/
│       ├── __init__.py
│       ├── config.py              # Configuration management
│       ├── database.py            # Database utilities
│       └── i18n.py                # Internationalization
└── pages/
    └── 1_Admin_Panel.py           # Admin panel page
```

## 🎨 Features Details

### RAG Pipeline

The application uses a sophisticated RAG pipeline:

1. **Document Ingestion**: Documents are chunked and embedded using OpenAI embeddings
2. **Vector Storage**: Embeddings are stored in Pinecone for fast similarity search
3. **Query Processing**: User queries are embedded and matched against the knowledge base
4. **Context Retrieval**: Top-K most relevant documents are retrieved
5. **Response Generation**: GPT-4 generates responses based on retrieved context
6. **Source Citation**: Retrieved sources are displayed with relevance scores

### Chat History

- All conversations are automatically saved to SQLite database
- Sessions can be resumed or deleted
- Full conversation context is preserved
- Search through past conversations

### Feedback System

- Users can rate responses with thumbs up/down
- Optional comment/feedback text
- Feedback is stored and analyzed
- Helps improve response quality over time

### Multi-Language Support

Currently supported languages:
- 🇬🇧 English
- 🇫🇷 Français (French)
- 🇷🇼 Kinyarwanda

The system translates:
- UI elements and labels
- Instructions and prompts
- Responses are generated in the selected language

## 🚀 Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Sign up at [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect your repository
4. Add secrets in the Streamlit Cloud dashboard:
   ```toml
   OPENAI_API_KEY = "your-key"
   PINECONE_API_KEY = "your-key"
   PINECONE_ENVIRONMENT = "us-east-1"
   ```

### Deploying to Custom Domain (campuslink.apps.cximmersion.com)

For deploying to your custom domain:

1. **Using Docker** (Recommended):
   ```bash
   docker build -t cmu-africa-assistant .
   docker run -p 8501:8501 --env-file .env cmu-africa-assistant
   ```

2. **Using Traditional Hosting**:
   - Set up a Linux server
   - Install Python and dependencies
   - Configure reverse proxy (Nginx/Apache)
   - Set up SSL certificate
   - Run with systemd or supervisor

3. **Environment Variables**:
   Ensure all required environment variables are set on the server.

## 🐛 Troubleshooting

### Common Issues

**1. "ModuleNotFoundError" when running the app**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**2. Pinecone connection errors**
```
# Solution: Verify your Pinecone environment and API key
# Check if your environment matches the one in Pinecone dashboard
# Common environments: us-east-1, us-west-1, etc.
```

**3. OpenAI API errors**
```
# Solution: Check your API key and billing status
# Ensure you have credits available
# Verify the API key has proper permissions
```

**4. Knowledge base not loading**
```bash
# Solution: Check the data file exists
ls data/cmu_africa_knowledge_base.json

# Verify JSON format
python -c "import json; json.load(open('data/cmu_africa_knowledge_base.json'))"
```

**5. Chat history not persisting**
```bash
# Solution: Ensure data directory has write permissions
chmod 755 data/
```

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG_MODE=True
```

This will show additional error information in the application.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue with details
2. **Suggest Features**: Share your ideas via issues
3. **Submit Pull Requests**: 
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a PR with description

## 📝 Updating the Knowledge Base

To add more CMU-Africa information:

1. **Edit the JSON file**:
   ```bash
   nano data/cmu_africa_knowledge_base.json
   ```

2. **Add new entries** following this format:
   ```json
   {
     "id": "unique_id",
     "title": "Title",
     "category": "Category",
     "content": "Detailed content here",
     "keywords": ["keyword1", "keyword2"]
   }
   ```

3. **Restart the application** or use the Admin Panel to upload

## 📊 Knowledge Base Categories

Current categories:
- Transportation
- Academic Programs
- Faculty
- Campus Facilities
- Admissions
- Student Life
- Career Services
- Contact
- General

## 🔐 Security Notes

- **Never commit `.env` files** with real API keys
- **Use environment variables** for production deployments
- **Rotate API keys** regularly
- **Monitor API usage** to detect anomalies
- **Restrict admin access** in production environments

## 📞 Support

For questions or issues:
- Check the [Troubleshooting](#troubleshooting) section
- Review existing issues on GitHub
- Contact CMU-Africa IT support

## 📄 License

This project is created for CMU-Africa. Please check with CMU-Africa for licensing information.

## 🎉 Acknowledgments

- Carnegie Mellon University Africa
- OpenAI for GPT-4 and embeddings
- Pinecone for vector database
- Streamlit for the amazing framework

---

**Built with ❤️ for CMU-Africa Community**

For official CMU-Africa information, visit: [https://www.africa.engineering.cmu.edu/](https://www.africa.engineering.cmu.edu/)
