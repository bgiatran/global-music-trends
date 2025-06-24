# utils/lang_utils.py

from langdetect import detect

# Attempts to detect the language of a given text string using langdetect
# Returns "unknown" if detection fails or text is invalid
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"