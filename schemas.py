from typing import Annotated
from pydantic import BaseModel,ConfigDict,EmailStr,Field,SecretStr,StringConstraints,model_validator


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
class RegisterRequest(StrictBaseModel):

    first_name: Annotated[str,StringConstraints(min_length=2,max_length=50,strip_whitespace=True)]
    last_name: Annotated[str,StringConstraints(min_length=2,max_length=50,strip_whitespace=True)]
    email_address: EmailStr
    phone_number: Annotated[str,StringConstraints(min_length=8,max_length=20,strip_whitespace=True)]
    card_info: Annotated[str,StringConstraints(min_length=4,max_length=19,strip_whitespace=True)]
    password: Annotated[SecretStr,Field(min_length=8, max_length=128)]
    re_type_password: SecretStr
    @model_validator(mode="after")
    def check_passwords_match(self):
        if (self.password.get_secret_value()!= self.re_type_password.get_secret_value()):
            raise ValueError("Passwords do not match")
        return self

class LoginRequest(StrictBaseModel):
    email_address: EmailStr
    password: SecretStr

class DepositRequest(StrictBaseModel):
    amount: Annotated[int,Field(gt=0)]

class TransferRequest(StrictBaseModel):
    transfer_amount: Annotated[int,Field(gt=0)]
    receiver_email: EmailStr
    receiver_phone: Annotated[str,StringConstraints(min_length=8,max_length=20,strip_whitespace=True)]
    password: SecretStr

class WithdrawalRequest(StrictBaseModel):
    amount: Annotated[int,Field(gt=0)]
    password: SecretStr

class DeleteAccountRequest(StrictBaseModel):
    password: SecretStr

# class RejisterRequest(BaseModel):
#     first_name: str  = Field(min_length=1, max_length=50)
#     last_name: str = Field(min_length=1, max_length=50)
#     email_address: EmailStr
#     phone_number: str = Field(min_length=9, max_length=30)
#     card_info: str = Field(min_length=10, max_length=19)
#     password: SecretStr
#     re_type_password : str
    

# class RejisterResponse(RejisterRequest):
#     pass
#     # model_config = ConfigDict(from_attributes=True)

# class MenuWalletRequest(BaseModel):
#     choose : int = Field(gt=0,le=6)

# class DepositRequest(BaseModel):
#     amount : int = Field(gt=0)
    
# class TransferRequest(BaseModel):
#     transfer_amount :int = Field(gt=0)
#     receiver_email : EmailStr
#     receiver_phone: str = Field(min_length=9, max_length=30)
#     password : str
    
# class WithdrawalRequest(BaseModel):
#     amount : int = Field(gt=0)
#     password : str
    
# class DeleteAccountRequest(BaseModel):
#     password : str