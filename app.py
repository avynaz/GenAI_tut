import os
from groq import Groq
import gradio as gr

client=Groq(api_key=os.getenv('GROQ_API_KEY'))

SYSTEM_PROMPT = ("""You are a football expert with experience in every aspect
of football rules and regulations including the history of football""")

def respond(message, history, system_prompt, temperature):
  messages = [{"role": "system", "content": SYSTEM_PROMPT}]
  for turn in history:
    messages.append({"role": turn["role"], "content": turn["content"]})
  messages.append({"role": "user", "content": message})
  stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=temperature,
        stream=True,
    )

  partial=""
  for chunk in stream:
    partial += chunk.choices[0].delta.content or ""
    yield partial
additional_inputs = [
    gr.Textbox(value="You are a football expert with experience in every aspect of football rules and regulations including the history of football", label="System Prompt", lines=4),
    gr.Slider(minimum=0.0, maximum=1.0, value=0.7, step=0.1, label="Temperature (Randomness)"),
]


demo = gr.ChatInterface(fn=respond, type="messages", title="Interactive Football Expert",additional_inputs=additional_inputs)
demo.launch(debug=True)
