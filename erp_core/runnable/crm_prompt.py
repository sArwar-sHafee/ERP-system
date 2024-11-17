from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from erp_core.Tools.customer_relationship_management import customer_support
from erp_core.assistant_class import CompleteOrEscalate
from erp_core._llm import llm
customer_relationship_management_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling customer relationship management issues. "
            "The primary assistant delegates work to you whenever the user needs help with their customer relationship management problems. "
            "Introduce yourself as a customer relationship management assistant"
            "Start conversation respectfully."
            "Diagnose the user query based on the user's input"
            "If any information is missing to call proper tool, ask the user for clarification."
            "While ready to call tool ask the user for confirmation once again by repeating the user's query."
            "If the user confirms that it is correct only then call proper tool to solve user query. It is very important."
            "Remember that an issue isn't resolved until the relevant tool or method has successfully been used."
            "\n\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
            ' "CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

customer_relationship_management_tools = [customer_support]
customer_relationship_management_runnable = customer_relationship_management_prompt | llm.bind_tools(
    customer_relationship_management_tools + [CompleteOrEscalate]
)