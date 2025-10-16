"""
Translation Module - Handles multi-language support
"""

from typing import Optional
from deep_translator import GoogleTranslator


class Translator:
    """
    Wrapper class for translation services
    """
    
    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'fr': 'French',
        'rw': 'Kinyarwanda'
    }
    
    # Language codes for Google Translate
    GOOGLE_LANG_CODES = {
        'en': 'en',
        'fr': 'fr',
        'rw': 'rw'
    }
    
    def __init__(self):
        """Initialize translator"""
        pass
    
    def translate(self, text: str, source_lang: str = 'auto', target_lang: str = 'en') -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto' for auto-detection)
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
        
        # If source and target are the same, no translation needed
        if source_lang == target_lang and source_lang != 'auto':
            return text
        
        # If target is English and no translation needed
        if target_lang == 'en' and source_lang == 'en':
            return text
        
        try:
            # Map language codes to Google Translate codes
            source_code = self.GOOGLE_LANG_CODES.get(source_lang, source_lang)
            target_code = self.GOOGLE_LANG_CODES.get(target_lang, target_lang)
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            translated = translator.translate(text)
            
            return translated if translated else text
        
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text if translation fails
            return text
    
    def translate_to_english(self, text: str, source_lang: str = 'auto') -> str:
        """
        Translate text to English
        
        Args:
            text: Text to translate
            source_lang: Source language code (default: 'auto')
            
        Returns:
            Text translated to English
        """
        return self.translate(text, source_lang, 'en')
    
    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translate text from English to target language
        
        Args:
            text: English text to translate
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        if target_lang == 'en':
            return text
        
        return self.translate(text, 'en', target_lang)
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect the language of the text
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected language code or None
        """
        if not text or not text.strip():
            return None
        
        try:
            # Use Google Translator to detect
            translator = GoogleTranslator(source='auto', target='en')
            translator.translate(text)
            # Note: deep-translator doesn't expose detected language directly
            # This is a limitation; for production, consider using langdetect library
            return 'auto'
        except Exception as e:
            print(f"Language detection error: {e}")
            return None
    
    def get_supported_languages(self) -> dict:
        """
        Get list of supported languages
        
        Returns:
            Dictionary of language codes and names
        """
        return self.LANGUAGES.copy()
    
    def is_supported(self, lang_code: str) -> bool:
        """
        Check if a language is supported
        
        Args:
            lang_code: Language code to check
            
        Returns:
            True if supported, False otherwise
        """
        return lang_code in self.LANGUAGES


# Global translator instance
_translator_instance = None


def get_translator() -> Translator:
    """
    Get or create a singleton translator instance
    
    Returns:
        Translator instance
    """
    global _translator_instance
    
    if _translator_instance is None:
        _translator_instance = Translator()
    
    return _translator_instance
