import openai
import config
openai.organization = config.openai_organization
openai.api_key = config.openai_api_key

def translate(sentence, lang):
    prompt = f"Translate the following English sentence to {lang}: {sentence}"
    text = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        max_tokens=512,
        temperature=0, # the higher this value, the less deterministic
        top_p=1, # the higher this value, the wider range of vocab is used
    ).choices[0].message.content.strip()
    return text