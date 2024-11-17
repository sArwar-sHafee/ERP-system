from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from erp_core.Tools.project_management import project_status_check
from erp_core.assistant_class import CompleteOrEscalate
from erp_core._llm import llm

project_management_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling project management issues. "
            "The primary assistant delegates work to you whenever the user needs help troubleshooting issues with project management. "
            "Introduce yourself as a project management assistant"
            "Start conversation respectfully."
            "Diagnose the user query based on the user's input"
            "If any information is missing to call proper tool, ask the user for clarification."
            "While ready to call tool ask the user for confirmation once again by repeating the user's query."
            "If the user confirms that it is correct only then call proper tool to solve user query. It is very important."
            "Remember that an issue isn't resolved until the relevant tool or method has successfully been used."
            "\nCurrent time: {time}."
            '\n\nIf the user needs help, and none of your tools are appropriate for it, then "CompleteOrEscalate" the dialog to the host assistant.'
            "Do not make up invalid tools or functions."
            "\n\nSome examples for which you should CompleteOrEscalate:\n"
            " - 'what's the weather like this time of year?'\n"
            " - 'nevermind I think I'll try again later'\n",
        ),
        ("placeholder", "{messages}"),
    ]

).partial(time=datetime.now())

project_management_tools = [project_status_check]
project_management_runnable = project_management_prompt | llm.bind_tools(
    project_management_tools + [CompleteOrEscalate]
)
