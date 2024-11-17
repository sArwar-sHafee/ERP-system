from erp_core.node_builder import compile_graph
from erp_core._event import _print_event
from erp_core.asr_and_tts import transcribe, tts
import gradio as gr
import time

# Function to initialize a new chat state
def new_chat():
    thread_id = int(time.time() * 1000)
    graph = compile_graph()
    message_history = []
    tool_output = None
    print("New Chat Initialized")
    return {
        "thread_id": thread_id,
        "graph": graph,
        "message_history": message_history,
        "tool_output": tool_output,
        "assistant_state": "primary_assistant",
        "previous_state": "primary_assistant",
        "tts_audio": None,
    }

def button_pressed():
   new_chat_init = new_chat()
   return new_chat_init, None, [], None, None

# Main processing function
def run(audio, state):
    try:
        if audio is None:
            return state["assistant_state"], state["message_history"], state["tts_audio"], None, state["tool_output"]
        
        user_input = transcribe(audio)
        print("User:", user_input)

        for event in state["graph"].stream(
            {"messages": ("user", user_input)},
            config={"configurable": {"thread_id": state["thread_id"]}},
        ):
            for value in event.values():
                if "messages" in value:
                    _printed = set()
                    assistant_states, assistant_messages = _print_event(value, _printed)
                    assistant_message = assistant_messages.content
                    if assistant_messages.content != "":
                        assistant_message_true = assistant_messages.content
                    else:
                        assistant_message_true = "..."
                    if assistant_states is None:
                        state["assistant_state"] = state["previous_state"]
                    else:
                        state["previous_state"] = assistant_states
                        state["assistant_state"] = assistant_states
                    if assistant_message != "" and assistant_states is None and "tool_call_id" not in assistant_messages:
                        state["tts_audio"] = tts(assistant_message)
                    if assistant_message == "" and assistant_states is None:
                        state["tool_output"] = assistant_messages.additional_kwargs["tool_calls"]

        state["message_history"].append({"role": "user", "content": user_input})
        state["message_history"].append({"role": "assistant", "content": assistant_message_true})
        
        return (
            state["assistant_state"],
            state["message_history"],
            None,  # Clear audio input
            None,
            state["tool_output"],
        )
    except Exception as e:
        print(e)
        return None, [], None, None, None  # Clear audio input on error

# Gradio interface
with gr.Blocks() as demo:
    chatbot_state = gr.State(new_chat)  # Initialize new state per session
    
    with gr.Row():
        with gr.Column():
            assistant_state_output = gr.Textbox(label="Current Assistant", interactive=False)
            tool_output = gr.Textbox(label="Tool Output", interactive=False)
            tts_output = gr.Audio(type="filepath", label="Assistant Voice Output", autoplay=True)
        with gr.Column():
            chatbot = gr.Chatbot(label="Conversation", type="messages")
    
    audio_input = gr.Audio(sources="microphone", type="numpy", label="Speak", streaming=False)

    audio_input.change(
        fn=run,
        inputs=[audio_input, chatbot_state],  # Pass state as input
        outputs=[assistant_state_output, chatbot, tts_output, audio_input, tool_output],
    )

    button = gr.Button("Click Here to Start a Chat")
    button.click(
        fn=button_pressed,
        outputs=[chatbot_state, assistant_state_output, chatbot, tts_output, tool_output]  # Reset state
    )
# new_chat()
demo.launch()
