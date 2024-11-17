from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from erp_core.Tools.human_resource import employee_database_access, leave_management
from erp_core.assistant_class import CompleteOrEscalate
from erp_core._llm import llm


human_resource_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling human resource issues. "
            "The primary assistant delegates work to you whenever the user needs help with their human resource problems. "
            "Introduce yourself as a human resource assistant"
            "Start conversation respectfully."
            "Diagnose the user query based on the user's input"
            "If any information is missing to call proper tool, ask the user for clarification."
            "While ready to call tool ask the user for confirmation once again by repeating the user's query."
            "If the user confirms that it is correct only then call proper tool to solve user query. It is very important."
            "Remember that an issue isn't resolved until the relevant tool or method has successfully been used."
            "\n\nCurrent user human resource information:\n\n{user_info}\n"
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then"
            ' "CompleteOrEscalate" the dialog to the host assistant. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())

human_resource_tools = [
    employee_database_access,
    leave_management
]
human_resource_runnable = human_resource_prompt | llm.bind_tools(
    human_resource_tools + [CompleteOrEscalate]
)