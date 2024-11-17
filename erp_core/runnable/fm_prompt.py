from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from erp_core.Tools.finalcial_management import register_purchase_request, view_expense_report
from erp_core.assistant_class import CompleteOrEscalate
from erp_core._llm import llm
financial_management_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling financial management issues. "
            "The primary assistant delegates work to you whenever the user needs help with their financial management problems. "
            "Introduce yourself as a financial management assistant"
            "Start conversation respectfully."
            "Diagnose the user query based on the user's input"
            "If any information is missing to call proper tool, ask the user for clarification."
            "While ready to call tool ask the user for confirmation once again by repeating the user's query. This is very important"
            "If the user confirms that it is correct only then call proper tool to solve user query. It is very important."
            "Remember that an issue isn't resolved until the relevant tool or method has successfully been used."
            "Remember always provide a response while calling a tool or after calling a tool."
            "\nCurrent time: {time}."
            '\n\nIf the user needs help, and none of your tools are appropriate for it, then "CompleteOrEscalate" the dialog to the host assistant.'
            "Do not make up invalid tools or functions."
            "\n\nSome examples for which you should CompleteOrEscalate:\n"
            " - 'what's the weather like this time of year?'\n"
            " - 'nevermind I think I'll try again later'\n"
            " - 'Financial management issue resolved'",
        ),
        ("placeholder", "{messages}"),
    ]

).partial(time=datetime.now())

financial_management_tools = [register_purchase_request, view_expense_report]
financial_management_runnable = financial_management_prompt | llm.bind_tools(
    financial_management_tools + [CompleteOrEscalate]
)