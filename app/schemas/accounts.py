from pydantic import BaseModel, ConfigDict

class AccountBase(BaseModel):
    # Shared properties for creating or reading an account.
    name: str
    email: str

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    # What we return when reading an account:
    id: int

    # allow reading attributes off ORM objects
    model_config = ConfigDict(from_attributes=True)
