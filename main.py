from dotenv import load_dotenv
import os
import gradio as gr
from gradio import ChatMessage
from pydantic_ai import Agent 
from pydantic_ai.messages import ModelRequest, ModelResponse, TextPart, UserPromptPart, ModelMessage
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

################################# - Agent - #################################
agent_plain = Agent(
    "openai:gpt-4.1",
    system_prompt=(
        "You are a helpful assistant. Be concise and reply with one sentence"
    )
)
exa_server = MCPServerStdio(  
    "npx",
    args=[
        "-y",
        "exa-mcp-server"
    ],
    env={
        "EXA_API_KEY": "2b824dd4-2573-4f98-a5c5-be06c9dd48f1"
    }
)
agent_tooled = Agent(
    "openai:gpt-4.1",
    instructions=(
        "You are a strategic sourcing manager in a procurement department."
        "You will be given a prompt of a highly specialised product, material or service that is required."
        "Your job is to find several companies that have the capability to supply those products, materials or services."
        "Your answers should always be presented in a table that includes the following columns in order:"
        "Company Name, Cababilities (Short description of these, relative to the input prompt), Website, HQ City, HQ State, HQ Country, Contact Details, Company Linkedin Page, Number of Employees Listed on Linkedin, Qualifications (status on licensing, insurance and bonding. Include links to the relevant pages on company or public body websites where available), Leadership Profile (links to the three most senior employee profiles you can find on linkedin)."
        "Only provide a maximum of 5 companies, unless the user specifies a number greater than that to return."
        "If the user provides a company name or website in the prompt, use the find similar tool within exa search to identify companies to return."
        "After the results are provided, ask the user if they would like to request more detail about these companies in Craft."
    ),
    toolsets=[exa_server]
)

################################# - Agent Calls - #################################

# Parse gradio history into Pydantic format
def parse_history(history: list[dict[str,str]]) -> list[ModelMessage]:
    message_history: list[ModelMessage] = []
    for msg in history:
        if msg["role"] == "user":
            message_history.append(ModelRequest(parts=[UserPromptPart(content=f"You: {msg['content']}")]))  
        message_history.append(ModelResponse(parts=[TextPart(content=f"Craft: {msg['content']}")]))

    return message_history

# Sync Agent call function
def call_plain_agent(message: str, history: list[ChatMessage]) -> str:
    response = agent_plain.run_sync(message, message_history=parse_history(history))
    # message_history = response.new_messages()
    return response.output

# Call agent with tools
async def call_tooled_agent(message,history):
    response = await agent_tooled.run(message,message_history=parse_history(history))
    # message_history = response.new_messages()
    return response.output

################################# - Gradio FrontEnd - #################################

with gr.Blocks(
    fill_height=True,
    theme=gr.themes.Default(primary_hue="blue", secondary_hue="purple",font=[gr.themes.GoogleFont("proxima-nova"), "Arial", "sans-serif"]),
    css="""
        footer {
            display: none !important;
        }
        .footer {
            display: none !important;
        }
        .gradio-container footer {
            display: none !important;
        }
        .gradio-container .footer {
            display: none !important;
        }
        [data-testid="footer"] {
            display: none !important;
        }
        .built-with-gradio {
            display: none !important;
        }
        .svelte-1gfkn6j {
            display: none !important;
        }
    """
) as demo:

    with gr.Row():
        with gr.Column(scale=1,min_width=70):
            logo = gr.Image('favicon.png', show_label=False,container=False,show_download_button=False,show_fullscreen_button=False)
        with gr.Column(scale=30):
            title = gr.Markdown('# Craft Sourcing Assistant')
    with gr.Row():
        chat = gr.ChatInterface(
            call_tooled_agent,
            type="messages",
            fill_height=True,
            chatbot=gr.Chatbot(
                type="messages",
                show_label=False,
                label="SourceBot",
                avatar_images=("user.svg","aiChat.svg"),
                layout="panel",
                min_height=800
            ),
            textbox=gr.Textbox(
                placeholder="Type your sourcing query here",
                submit_btn=True
            )
        )

if __name__ == "__main__":
    demo.launch()
