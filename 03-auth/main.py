import gradio as gr
from transformers import MarianMTModel, AutoTokenizer


# Carregar els models de traduccio de helsinki-nlp
# source: https://huggingface.co/Helsinki-NLP/opus-mt-en-es?text=My+name+is+Wolfgang+and+I+live+in+Berlin&library=transformers
# es -> en
model_es_to_en = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-es-en")
tokenizer_es_to_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")

# en -> es
model_en_to_es = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-es")
tokenizer_en_to_es = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")

availableLangs = ["EN", "ES"]

availableModels = { 
    availableLangs[0]: model_en_to_es,
    availableLangs[1]:model_es_to_en
    }

availableTokenizers = {
    availableLangs[0]: tokenizer_en_to_es,
    availableLangs[1]: tokenizer_es_to_en
    }

# Source: https://huggingface.co/docs/transformers/main/en/model_doc/marian#transformers.MarianMTModel.forward.example
def Translate(sourceLang, text):
    tokens = availableTokenizers[sourceLang](text, return_tensors="pt", padding=True)
    translated = availableModels[sourceLang].generate(**tokens)
    translation = availableTokenizers[sourceLang].decode(translated[0], skip_special_tokens=True)

    return translation

def UserAuth(username, password):
    return username == password

with gr.Blocks() as demo:
    gr.Markdown("Translate app")
    with gr.Row():
        inp = gr.TextArea(placeholder="Input")
        out = gr.TextArea()

    button = gr.Button("Translate")

    button.click(fn=Translate, inputs=[
        gr.Radio(availableLangs, label="Source language", value=availableLangs[0]),
        inp
    ], outputs=out)

# Source: https://www.gradio.app/guides/sharing-your-app#password-protected-app
demo.launch(auth=UserAuth)