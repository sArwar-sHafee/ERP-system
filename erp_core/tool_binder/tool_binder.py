from langchain_core.pydantic_v1 import BaseModel, Field

class ToFinancialManagementDepartment(BaseModel):
    """Transfers work to a specialized assistant to handle final management department issues."""

    request: str = Field(
        description="Any necessary followup questions the financial management department assistant should clarify before proceeding."
    )

class ToProjectManagementDepartment(BaseModel):
    """Transfers work to a specialized assistant to handle project management issues."""

    request: str = Field(
        description="Any necessary followup questions the project management department assistant should clarify before proceeding."
    )

class ToCustomerRelationshipManagementDepartment(BaseModel):
    """Transfers work to a specialized assistant to handle customer relationship management issues."""

    request: str = Field(
        description="Any necessary followup questions the customer relationship management assistant should clarify before proceeding."
    )

class ToHumanResourceDepartment(BaseModel):
    """Transfers work to a specialized assistant to handle human resource issues."""

    request: str = Field(
        description="Any necessary followup questions the human resource department assistant should clarify before proceeding."
    )  

class ToSupplyChainManagementDepartment(BaseModel):
    """Transfers work to a specialized assistant to handle supply chain issues."""

    request: str = Field(
        description="Any necessary followup questions the supply chain department assistant should clarify before proceeding."
    )