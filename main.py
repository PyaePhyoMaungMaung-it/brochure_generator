from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
from openai import OpenAI 
import gradio as gr
import os

load_dotenv(override=True)
google_api_key = os.getenv('GOOGLE_API_KEY')

if google_api_key:
    print(f"Google api key exists and begins {google_api_key[:8]}")
else:
    print("Google api key not set!")

gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
ollama_url = "http://localhost:11434/v1"
gemini = OpenAI(api_key=google_api_key or "", base_url=gemini_url) if google_api_key else None
ollama = OpenAI(base_url=ollama_url, api_key='ollama')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

}

def fetch_website_contents(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "sytle", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n"+ text)[:2_000]

system_message = """
    You are an assistant that analyzes the contents of a company website 
    landing page and creates a short brochure about the company for 
    prospective cutomers, investors and recuits. Respond in markdown
    without code blocks.
"""

def stream_gemini(prompt):
    if gemini is None:
        yield "Gemini is unavailable because GOOGLE_API_KEY is not set."
        return

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    try:
        stream = gemini.chat.completions.create(
            messages=messages,
            model='gemini-2.0-flash',
            stream=True
        )
        result = ""
        for chunk in stream:
            result += chunk.choices[0].delta.content or ""
            yield result
    except Exception as exc:
        yield f"Gemini request failed: {exc}"


def stream_ollama(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    try:
        stream = ollama.chat.completions.create(
            messages=messages,
            model='llama3.2:latest',
            stream=True
        )
        result = ""
        for chunk in stream:
            result += chunk.choices[0].delta.content or ""
            yield result
    except Exception as exc:
        yield f"Ollama request failed: {exc}"

def stream_brochure(company_name, url, model):
    yield ""
    prompt = f"Please generate a company brochure for {company_name}. Here is their landing page: \n"
    prompt += fetch_website_contents(url)
    if model == "gemini":
        result = stream_gemini(prompt)
    elif model == "ollama":
        result = stream_ollama(prompt)
    else:
        raise ValueError("Unknown Model!")
    yield from result

name_input = gr.Textbox(label="Company Name: ")
url_input = gr.Textbox(label="Landing page URL including https:// or http://")
model_selector = gr.Dropdown(["gemini", "ollama"], label="Select a model", value = "gemini")
messaeg_output = gr.Markdown(label="Response: ")

view = gr.Interface(
    fn = stream_brochure,
    title= "Brochure Generator",
    inputs = [name_input, url_input, model_selector],
    outputs  = [messaeg_output],
    examples = [
        ["Edward Donner", "https://edwarddonner.com", "gemini"],
        ["ei maung", "https://eimaung.com", "ollama"]

    ],
    flagging_mode= "never"

)

if __name__ == "__main__":

    view.launch(inbrowser=True )