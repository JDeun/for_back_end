from pydantic import BaseModel

class LLMModelBase(BaseModel):
    name: str
    description: str
    output_type: str

class LLMModelCreate(LLMModelBase):
    pass

class LLMModelResponse(LLMModelBase):
    id: int

    class Config:
        orm_mode = True
