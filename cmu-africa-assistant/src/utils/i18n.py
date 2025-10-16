
"""
Internationalization (i18n) support for multi-language
"""
from typing import Dict

# Supported languages and their translations
TRANSLATIONS = {
    "en": {
        "app_title": "CMU-Africa Information Assistant",
        "welcome_message": "👋 Welcome! I'm your CMU-Africa assistant. Ask me anything about our campus!",
        "chat_input_placeholder": "Ask me about CMU-Africa...",
        "thinking": "🤔 Thinking...",
        "error_no_config": "⚠️ Please configure your API keys in the sidebar first.",
        "error_general": "An error occurred. Please try again.",
        "sidebar_config": "⚙️ Configuration",
        "sidebar_openai_key": "OpenAI API Key",
        "sidebar_pinecone_key": "Pinecone API Key",
        "sidebar_pinecone_env": "Pinecone Environment",
        "sidebar_save_config": "Save Configuration",
        "sidebar_language": "Language",
        "feedback_prompt": "Was this response helpful?",
        "feedback_thanks": "Thank you for your feedback!",
        "chat_history": "💬 Chat History",
        "new_chat": "➕ New Chat",
        "admin_panel": "🔧 Admin Panel",
        "knowledge_base": "Knowledge Base Management",
        "add_document": "Add Document",
        "document_title": "Document Title",
        "document_content": "Document Content",
        "upload_button": "Upload to Knowledge Base",
        "view_feedback": "View Feedback",
        "feedback_stats": "Feedback Statistics",
    },
    "fr": {
        "app_title": "Assistant d'Information CMU-Africa",
        "welcome_message": "👋 Bienvenue! Je suis votre assistant CMU-Africa. Posez-moi des questions sur notre campus!",
        "chat_input_placeholder": "Posez-moi des questions sur CMU-Africa...",
        "thinking": "🤔 Réflexion...",
        "error_no_config": "⚠️ Veuillez configurer vos clés API dans la barre latérale d'abord.",
        "error_general": "Une erreur s'est produite. Veuillez réessayer.",
        "sidebar_config": "⚙️ Configuration",
        "sidebar_openai_key": "Clé API OpenAI",
        "sidebar_pinecone_key": "Clé API Pinecone",
        "sidebar_pinecone_env": "Environnement Pinecone",
        "sidebar_save_config": "Enregistrer la Configuration",
        "sidebar_language": "Langue",
        "feedback_prompt": "Cette réponse était-elle utile?",
        "feedback_thanks": "Merci pour votre retour!",
        "chat_history": "💬 Historique des Conversations",
        "new_chat": "➕ Nouvelle Conversation",
        "admin_panel": "🔧 Panneau d'Administration",
        "knowledge_base": "Gestion de la Base de Connaissances",
        "add_document": "Ajouter un Document",
        "document_title": "Titre du Document",
        "document_content": "Contenu du Document",
        "upload_button": "Télécharger vers la Base de Connaissances",
        "view_feedback": "Voir les Commentaires",
        "feedback_stats": "Statistiques de Retour",
    },
    "rw": {
        "app_title": "Umufasha w'Amakuru ya CMU-Africa",
        "welcome_message": "👋 Murakaza neza! Ndi umufasha wawe wa CMU-Africa. Mumbaze ibintu byose kuri campus yacu!",
        "chat_input_placeholder": "Mumbaze ku bijyanye na CMU-Africa...",
        "thinking": "🤔 Ndatekereza...",
        "error_no_config": "⚠️ Nyamuneka shiraho API keys yawe mu ruhande mbere.",
        "error_general": "Habaye ikosa. Nyamuneka ongera ugerageze.",
        "sidebar_config": "⚙️ Iboneza",
        "sidebar_openai_key": "Urufunguzo rwa OpenAI API",
        "sidebar_pinecone_key": "Urufunguzo rwa Pinecone API",
        "sidebar_pinecone_env": "Ibidukikije bya Pinecone",
        "sidebar_save_config": "Bika Iboneza",
        "sidebar_language": "Ururimi",
        "feedback_prompt": "Iyi gisubizo yari ingirakamaro?",
        "feedback_thanks": "Murakoze ku bitekerezo byanyu!",
        "chat_history": "💬 Amateka y'Ibiganiro",
        "new_chat": "➕ Ikiganiro Gishya",
        "admin_panel": "🔧 Ikibaho cy'Ubuyobozi",
        "knowledge_base": "Gucunga Ububiko bw'Ubumenyi",
        "add_document": "Ongeraho Inyandiko",
        "document_title": "Umutwe w'Inyandiko",
        "document_content": "Ibirimo mu Nyandiko",
        "upload_button": "Ohereza ku Bubiko bw'Ubumenyi",
        "view_feedback": "Reba Ibitekerezo",
        "feedback_stats": "Imibare y'Ibitekerezo",
    }
}

# Current language
current_language = "en"

def set_language(lang: str):
    """Set the current language"""
    global current_language
    if lang in TRANSLATIONS:
        current_language = lang

def get_text(key: str, lang: str = None) -> str:
    """Get translated text for a key"""
    lang = lang or current_language
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def get_available_languages() -> Dict[str, str]:
    """Get available languages"""
    return {
        "en": "English",
        "fr": "Français",
        "rw": "Kinyarwanda"
    }
