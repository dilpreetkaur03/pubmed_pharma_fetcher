from typing import List, Optional
from pydantic import BaseModel, EmailStr

class Affiliation(BaseModel):
    name: str
    is_non_academic: bool = False
    company_name: Optional[str] = None

class Author(BaseModel):
    name: str
    affiliations: List[Affiliation]
    email: Optional[EmailStr] = None
    is_non_academic: bool = False
    company_affiliation: Optional[str] = None

class Paper(BaseModel):
    pubmed_id: str
    title: str
    publication_date: str
    authors: List[Author]
    non_academic_authors: List[str]
    company_affiliations: List[str]
    corresponding_author_email: Optional[EmailStr] = None
