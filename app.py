import os
import re
import requests
import gradio as gr
from openai import OpenAI
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def is_url(message):
    """Check if the message is a URL."""
    
    return re.match(r'https?://\S+', message)

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""

    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Lỗi khi đọc PDF: {str(e)}"

def summarize_url(url):
    """Summarize the content of a URL."""

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join([p.get_text() for p in soup.find_all("p")])[:4000]
        messages = [
            {"role": "system", "content": "Tóm tắt nội dung bài báo sau bằng tiếng Việt:"},
            {"role": "user", "content": text}
        ]
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-maverick",
            messages=messages
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi khi truy cập URL: {str(e)}"

def search_latest_event(query):
    """Search for the latest events or news related to the query."""

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=3))
            if not results:
                return "Không tìm thấy thông tin phù hợp."

            content = "\n\n".join([f"{r['title']}\n{r['href']}\n{r['body']}" for r in results])
            messages = [
                {"role": "system", "content": "Tóm tắt các thông tin sau bằng tiếng Việt:"},
                {"role": "user", "content": content}
            ]
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-maverick",
                messages=messages
            )
            return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi khi tìm kiếm: {str(e)}"

def ask_about_pdf(pdf_text, question):
    """Ask a question about the content of a PDF."""

    messages = [
        {"role": "system", "content": "Bạn là trợ lý AI giúp trả lời các câu hỏi dựa trên nội dung file PDF."},
        {"role": "user", "content": f"Nội dung PDF:\n{pdf_text}"},
        {"role": "user", "content": f"Câu hỏi: {question}"}
    ]
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick",
        messages=messages
    )
    return completion.choices[0].message.content.strip()

def chat_with_bot(message, history, pdf_file=None):
    """Handle the chat interaction with the bot."""

    if not history:
        history = []

    if is_url(message):
        summary = summarize_url(message)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": summary})
        yield history
        return

    if any(kw in message.lower() for kw in ["sự kiện", "tin tức", "mới nhất", "news"]):
        search_result = search_latest_event(message)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": search_result})
        yield history
        return

    if pdf_file:
        text_from_pdf = extract_text_from_pdf(pdf_file)
        answer = ask_about_pdf(text_from_pdf, message)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": answer})
        yield history
        return

    temp_history = history + [{"role": "user", "content": message}]
    stream = client.chat.completions.create(
        model="meta-llama/llama-4-maverick",
        messages=temp_history,
        stream=True
    )

    bot_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            bot_response += chunk.choices[0].delta.content
            yield history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": bot_response}
            ]

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_response})
    yield history

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("## 🤖 Chat PDF + URL + Tin tức — by AI Assistant")

    chatbot = gr.Chatbot( type='messages', height=450)
    pdf_file = gr.File(label="📄 Tài liệu PDF", file_types=[".pdf"])
    user_input = gr.Textbox(
        show_label=False,
        placeholder="Nhập câu hỏi, URL hoặc nội dung bạn muốn hỏi...",
        lines=1,
        autofocus=True
    )

    def submit_message(message, history, pdf_file):
        history = history or []
        for updated_history in chat_with_bot(message, history, pdf_file):
            yield "", updated_history

    user_input.submit(submit_message, [user_input, chatbot, pdf_file], [user_input, chatbot])


if __name__ == "__main__":
    app.launch()
