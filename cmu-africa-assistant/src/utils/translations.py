"""
Multi-language support for the application
"""

TRANSLATIONS = {
    "en": {
        # General
        "app_title": "CMU-Africa Information Assistant",
        "app_description": "Ask me anything about CMU-Africa",
        "language": "Language",
        
        # Chat Interface
        "chat_title": "💬 Chat",
        "chat_input": "Ask a question about CMU-Africa...",
        "chat_send": "Send",
        "chat_clear": "Clear History",
        "chat_history_cleared": "Chat history cleared!",
        "sources_title": "📚 Sources",
        "no_sources": "No sources used for this response.",
        "source": "Source",
        "relevance": "Relevance",
        "category": "Category",
        
        # Feedback
        "feedback_title": "Was this answer helpful?",
        "feedback_positive": "👍 Yes",
        "feedback_negative": "👎 No",
        "feedback_comment": "Optional: Tell us more",
        "feedback_submit": "Submit Feedback",
        "feedback_thankyou": "Thank you for your feedback!",
        
        # History
        "history_title": "📜 Chat History",
        "history_empty": "No chat history yet.",
        "history_clear_confirm": "Are you sure you want to clear all history?",
        
        # Admin Panel
        "admin_title": "🛠️ Admin Panel",
        "admin_add_doc": "Add Document",
        "admin_bulk_upload": "Bulk Upload",
        "admin_view_docs": "View Documents",
        "admin_index_stats": "Index Statistics",
        "doc_id": "Document ID",
        "doc_title": "Title",
        "doc_category": "Category",
        "doc_content": "Content",
        "doc_language": "Language",
        "doc_add_button": "Add Document",
        "doc_added": "Document added successfully!",
        "doc_error": "Error adding document",
        "bulk_upload_info": "Upload JSON file with documents",
        "bulk_upload_button": "Upload",
        "bulk_success": "Successfully uploaded {0} documents, {1} failed",
        "stats_total": "Total Documents",
        "stats_dimension": "Vector Dimension",
        "stats_fullness": "Index Fullness",
        
        # Settings
        "settings_title": "⚙️ Settings",
        "settings_api": "API Configuration",
        "settings_openai": "OpenAI API Key",
        "settings_pinecone": "Pinecone API Key",
        "settings_pinecone_env": "Pinecone Environment",
        "settings_save": "Save Settings",
        "settings_saved": "Settings saved!",
        
        # Errors
        "error_api_keys": "⚠️ API keys not configured. Please set up your OpenAI and Pinecone API keys in Settings.",
        "error_connection": "Error connecting to services. Please check your configuration.",
        "error_query": "An error occurred while processing your query.",
    },
    "fr": {
        # Général
        "app_title": "Assistant d'Information CMU-Africa",
        "app_description": "Posez-moi des questions sur CMU-Africa",
        "language": "Langue",
        
        # Interface de Chat
        "chat_title": "💬 Chat",
        "chat_input": "Posez une question sur CMU-Africa...",
        "chat_send": "Envoyer",
        "chat_clear": "Effacer l'historique",
        "chat_history_cleared": "Historique effacé!",
        "sources_title": "📚 Sources",
        "no_sources": "Aucune source utilisée pour cette réponse.",
        "source": "Source",
        "relevance": "Pertinence",
        "category": "Catégorie",
        
        # Retours
        "feedback_title": "Cette réponse était-elle utile?",
        "feedback_positive": "👍 Oui",
        "feedback_negative": "👎 Non",
        "feedback_comment": "Optionnel: Dites-nous en plus",
        "feedback_submit": "Soumettre",
        "feedback_thankyou": "Merci pour votre retour!",
        
        # Historique
        "history_title": "📜 Historique des Conversations",
        "history_empty": "Pas encore d'historique.",
        "history_clear_confirm": "Êtes-vous sûr de vouloir effacer tout l'historique?",
        
        # Panneau d'Administration
        "admin_title": "🛠️ Panneau d'Administration",
        "admin_add_doc": "Ajouter un Document",
        "admin_bulk_upload": "Téléchargement en Masse",
        "admin_view_docs": "Voir les Documents",
        "admin_index_stats": "Statistiques de l'Index",
        "doc_id": "ID du Document",
        "doc_title": "Titre",
        "doc_category": "Catégorie",
        "doc_content": "Contenu",
        "doc_language": "Langue",
        "doc_add_button": "Ajouter",
        "doc_added": "Document ajouté avec succès!",
        "doc_error": "Erreur lors de l'ajout du document",
        "bulk_upload_info": "Télécharger un fichier JSON avec des documents",
        "bulk_upload_button": "Télécharger",
        "bulk_success": "{0} documents téléchargés avec succès, {1} échoués",
        "stats_total": "Total des Documents",
        "stats_dimension": "Dimension du Vecteur",
        "stats_fullness": "Remplissage de l'Index",
        
        # Paramètres
        "settings_title": "⚙️ Paramètres",
        "settings_api": "Configuration API",
        "settings_openai": "Clé API OpenAI",
        "settings_pinecone": "Clé API Pinecone",
        "settings_pinecone_env": "Environnement Pinecone",
        "settings_save": "Sauvegarder",
        "settings_saved": "Paramètres sauvegardés!",
        
        # Erreurs
        "error_api_keys": "⚠️ Clés API non configurées. Veuillez configurer vos clés API OpenAI et Pinecone dans les Paramètres.",
        "error_connection": "Erreur de connexion aux services. Vérifiez votre configuration.",
        "error_query": "Une erreur s'est produite lors du traitement de votre requête.",
    }
}


def get_text(key: str, language: str = "en") -> str:
    """
    Get translated text for a key
    
    Args:
        key: Translation key
        language: Language code
        
    Returns:
        Translated text
    """
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)


def format_text(key: str, language: str = "en", *args) -> str:
    """
    Get translated text with formatting
    
    Args:
        key: Translation key
        language: Language code
        *args: Format arguments
        
    Returns:
        Formatted translated text
    """
    text = get_text(key, language)
    return text.format(*args)
