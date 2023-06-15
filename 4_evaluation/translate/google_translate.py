from typing import List
from config import google_translate_project_id

def google_translate(sources: List[str],
                     lang: str,
                     project_id: str = google_translate_project_id) -> List[str]:

    from google.cloud import translate

    def translate_chunk(sources_chunk: List[str]) -> List[str]:
        client = translate.TranslationServiceClient()
        location = "global"
        parent = f"projects/{project_id}/locations/{location}"
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": sources_chunk,
                "mime_type": "text/plain",
                "source_language_code": "en-US",
                "target_language_code": lang,
            }
        )
        return [translation.translated_text for translation in response.translations]

    results = []
    for i in range(0, len(sources), 100):
        sources_chunk = sources[i:i+100]
        results.extend(translate_chunk(sources_chunk))

    return results
