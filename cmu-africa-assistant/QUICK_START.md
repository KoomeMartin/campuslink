# Quick Start Guide - CMU-Africa Information Assistant

## 🚀 Application is Running!

Your CMU-Africa Information Assistant is now running at: **http://localhost:8501**

## ⚙️ Configuration Steps

### Step 1: Get Your API Keys

You'll need API keys from two services:

#### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-...`)

#### Pinecone API Key & Environment
1. Go to [Pinecone](https://www.pinecone.io/)
2. Sign up or log in (free tier available)
3. Create a new project (if you haven't already)
4. Go to "API Keys" section
5. Copy your API Key
6. Note your Environment (e.g., `us-east-1`, `us-west-1`)

### Step 2: Configure in the Application

In the sidebar (left side of the screen):

1. **OpenAI API Key**: Paste your OpenAI API key
2. **Pinecone API Key**: Paste your Pinecone API key  
3. **Pinecone Environment**: Enter your Pinecone environment (e.g., `us-east-1`)
4. Click **"Save Configuration"** button

**Note**: The application will automatically:
- Connect to Pinecone
- Create an index if it doesn't exist
- Load the sample CMU-Africa knowledge base

This may take 15-30 seconds on first setup.

## 💬 Using the Chat Interface

Once configured, you can:

1. **Ask Questions** in the chat input at the bottom:
   - "What are the shuttle bus timings?"
   - "What Master's programs does CMU-Africa offer?"
   - "Tell me about the MSEAI program"
   - "Are there scholarships available?"

2. **View Sources**: Click on "📚 Sources" below responses to see where the information came from

3. **Provide Feedback**: Use 👍 or 👎 buttons to rate responses

4. **Change Language**: Select from English, Français, or Kinyarwanda in the sidebar

5. **Manage Chats**: 
   - Click "➕ New Chat" to start fresh
   - View previous sessions in the sidebar
   - Delete old chats with 🗑️ button

## 🔧 Admin Panel

Access the Admin Panel from the sidebar navigation to:

- **Add Documents**: Add new information to the knowledge base
- **Bulk Upload**: Upload multiple documents via JSON file
- **View Feedback**: See user feedback and statistics
- **Manage Knowledge Base**: Delete outdated documents

## 🌍 Multi-Language Support

Switch between languages in the sidebar:
- 🇬🇧 English
- 🇫🇷 Français (French)
- 🇷🇼 Kinyarwanda

The UI and responses will adapt to your selected language.

## 📊 Sample Knowledge Base

The application comes pre-loaded with information about:
- 🚌 Bus/Shuttle Services
- 🎓 Degree Programs (MSIT, MSECE, MSEAI)
- 👨‍🏫 Faculty & Research
- 🏫 Campus Facilities
- 💰 Admissions & Scholarships
- 💼 Career Services
- 📞 Contact Information

## 🛠️ Troubleshooting

### Application won't start
```bash
cd /home/ubuntu/code_artifacts/cmu-africa-assistant
streamlit run app.py
```

### Can't connect to Pinecone
- Verify your API key is correct
- Check your environment name matches Pinecone dashboard
- Ensure you have an active Pinecone account

### OpenAI errors
- Verify your API key is valid
- Check you have credits available
- Ensure API key has proper permissions

### Configuration not saving
- Re-enter all three fields (OpenAI key, Pinecone key, Environment)
- Click "Save Configuration" button
- Wait for success message

## 📝 Updating Knowledge Base

### Via Admin Panel
1. Go to Admin Panel (from sidebar)
2. Fill in document details
3. Click "Upload to Knowledge Base"

### Via JSON File
1. Edit `data/cmu_africa_knowledge_base.json`
2. Add new entries following the format
3. Use Admin Panel > Bulk Upload to reload

### JSON Format:
```json
{
  "id": "unique_id",
  "title": "Document Title",
  "category": "Category",
  "content": "Your content here...",
  "keywords": ["keyword1", "keyword2"]
}
```

## 🔒 Security Tips

- **Never share your API keys** publicly
- **Use environment variables** for production
- **Monitor your API usage** on OpenAI and Pinecone dashboards
- **Rotate keys** regularly for security

## 📚 More Information

For detailed documentation, see:
- **README.md** - Comprehensive documentation
- **Data Folder** - Sample knowledge base files
- **Source Code** - Well-commented Python files

## 🎯 Next Steps

1. ✅ Configure API keys
2. ✅ Test the chat interface
3. ✅ Try different languages
4. ✅ Add custom CMU-Africa data
5. ✅ Share with your team
6. 🚀 Deploy to production (see README.md)

## 💡 Tips for Best Results

- **Be specific** in your questions
- **Use natural language** - the AI understands context
- **Check sources** to verify information
- **Provide feedback** to help improve responses
- **Update knowledge base** regularly with latest CMU-Africa info

## 📞 Need Help?

- Check **README.md** for detailed troubleshooting
- Review application logs in `/tmp/streamlit_output.log`
- Contact CMU-Africa IT support for assistance

---

**Enjoy using your CMU-Africa Information Assistant! 🎓**
