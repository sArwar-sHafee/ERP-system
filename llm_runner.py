from erp_core.node_builder import builder
from erp_core._event import _print_event
from langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string(":memory:") as memory:
    graph = builder.compile(checkpointer=memory)
    while True:
      try:
        user_input = input("User: ")
        #print("User:", user_input)
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        for event in graph.stream({"messages": ("user", user_input)}, config={"configurable": {"thread_id": 42}}):
            for value in event.values():
                # print("Assistant:", value)
                if "messages" in value:
                    _printed = set()
                    state, message = _print_event(value, _printed)
                    print("State:", state)
                    print("Message:", message)
      except KeyboardInterrupt:
        print("Goodbye!")
        break