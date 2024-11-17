from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

from erp_core.Tools.supply_chain_management import product_quantity_check   
from erp_core.assistant_class import CompleteOrEscalate
from erp_core._llm import llm
supply_chain_management_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling supply chain management issues. "
            "The primary assistant delegates work to you whenever the user needs help troubleshooting issues with supply chain management. "
            "Introduce yourself as a supply chain management assistant"
            "Start conversation respectfully."
            "Diagnose the problem based on the user's input and confirm the troubleshooting steps with the customer. "
            "If any information is missing to call proper tool, ask the user for clarification."
            "While ready to call tool ask the user for confirmation once again by repeating the user's query."
            "If the user confirms that it is correct only then call proper tool to solve user query. It is very important."
            "Remember that an issue isn't resolved until the relevant tool or method has successfully been used."
            "\nCurrent time: {time}."
            '\n\nIf the user needs help, and none of your tools are appropriate for it, then "CompleteOrEscalate" the dialog to the host assistant.'
            " Do not waste the user's time. Do not make up invalid tools or functions."
            "\n\nSome examples for which you should CompleteOrEscalate:\n"
            " - 'what's the weather like this time of year?'\n"
            " - 'nevermind I think I'll try again later'\n"
            " - 'I need help with another issue instead'\n"
            " - 'Oh wait, I think the problem resolved itself'\n"
            " - 'Call issue resolved'",
        ),
        ("placeholder", "{messages}"),
    ]

).partial(time=datetime.now())

supply_chain_management_tools = [product_quantity_check]
supply_chain_management_runnable = supply_chain_management_prompt | llm.bind_tools(
    supply_chain_management_tools + [CompleteOrEscalate]
)
