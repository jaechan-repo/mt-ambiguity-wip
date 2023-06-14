from google.cloud import translate
from config import google_translate_project_id
from typing import List

def google_translate(sources: List[str],
                   lang: str,
                   project_id = google_translate_project_id) -> List[str]:
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": sources,
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": lang,
        }
    )
    return [translation.translated_text for translation in response.translations]