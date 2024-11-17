from erp_core.node_builder import compile_graph
from erp_core._event import _print_event
# from langgraph.checkpoint.sqlite import SqliteSaver
from erp_core.asr_and_tts import transcribe
from erp_core.asr_and_tts import tts
import gradio as gr
import time

# from erp_core.node_builder import graph

previous_state = "primary_assistant"
assistant_state = "primary_assistant"
message_history = []
thread_id = int(time.time()*1000)
tts_audio = None
tool_output = None
def new_chat():
    global thread_id, graph, message_history, tool_output
    thread_id = int(time.time()*1000)
    print("New Chat")
    graph = compile_graph()
    message_history = []
    tool_output = None
    return [], None

def run(audio):
    try:
        global previous_state, assistant_state, thread_id, message_history, tts_audio, tool_output
        if audio is None:
            # print(tts_audio)
            return assistant_state, message_history, tts_audio, None, tool_output
        else:
            user_input = transcribe(audio)
            print("User:", user_input)
            
            for event in graph.stream({"messages": ("user", user_input)}, config={"configurable": {"thread_id": thread_id}}):
                for value in event.values():
                    if "messages" in value:
                        _printed = set()
                        
                        assistant_states, assistant_messages = _print_event(value, _printed)
                        assistant_message = assistant_messages.content
                        print("State:", assistant_states)
                        print("Message:", assistant_message)
                        if assistant_states is None:
                            assistant_state = previous_state
                        else:
                            previous_state = assistant_states
                            assistant_state = assistant_states
                        if assistant_message !="" and assistant_states is None and "tool_call_id" not in assistant_message:
                            tts_audio = tts(assistant_message)
                        if assistant_states is None and "tool_call_id" not in assistant_message:
                            tool_output = assistant_message
            message_history.append({"role": "user", "content": user_input})
            message_history.append({"role": "assistant", "content": assistant_message})
            if tts_audio is not None:
                # print(tts_audio)
                return assistant_state, message_history, None, None, None  # Clear audio input
            else:
                return assistant_state, message_history, None, None, None  # Clear audio input
    except Exception as e:
        print(e)
        return None, [], None, None, None  # Clear audio input on error

with gr.Blocks() as demo:
    chatbot_state = gr.State(new_chat())
    with gr.Row():
        with gr.Column():
            assistant_state_output = gr.Textbox(label="Current Assistant", interactive=False)
            tool_output = gr.Textbox(label="Tool Output", interactive=False)
            tts_output = gr.Audio(type="filepath", label="Assistant Voice Output", autoplay=True) #
        with gr.Column():
            chatbot = gr.Chatbot(label="Conversation", type="messages")
    audio_input = gr.Audio(sources="microphone", type="numpy", label="Speak", streaming=False)
            

    audio_input.change(
        fn=run, 
        inputs=audio_input, 
        outputs=[assistant_state_output, chatbot, tts_output, audio_input, tool_output]
        )
    button = gr.Button("New Chat")
    button.click(
        fn=new_chat,
        outputs=[chatbot, tts_output]
    )
graph = compile_graph()
demo.launch(new_chat, share=True)
