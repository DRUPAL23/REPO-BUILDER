from __future__ import annotations
import re
from enum import Enum
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,field_validator,model_validator
class ApplicationType(str,Enum):
 WEB="web"; MOBILE="mobile"; API="api"; SAAS="saas"; HYBRID="hybrid"
class Platform(str,Enum):
 WEB="web"; ANDROID="android"; IOS="ios"; REST_API="rest-api"; CLI="cli"
class ArchitectureConfig(BaseModel):
 model_config=ConfigDict(extra="forbid")
 style:Literal["modular-monolith","microservices","serverless"]="modular-monolith"
 frontend_backend:bool=True
 multi_tenant:bool=False
 api_first:bool=False
class StackConfig(BaseModel):
 model_config=ConfigDict(extra="forbid")
 frontend:str="nextjs"; backend:str="fastapi"; database:str="postgresql"
 styling:str="tailwind"; language:str="typescript-python"
class ProjectSpec(BaseModel):
 """Versioned project blueprint for application generation."""
 model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
 schema_version:Literal["1.0"]="1.0"
 name:str=Field(min_length=1,max_length=80)
 slug:str=Field(min_length=1,max_length=80)
 description:str=Field(min_length=1,max_length=2000)
 application_type:ApplicationType=ApplicationType.WEB
 platforms:list[Platform]=Field(default_factory=lambda:[Platform.WEB])
 stack:Literal["nextjs-fastapi"]="nextjs-fastapi"
 stack_config:StackConfig=Field(default_factory=StackConfig)
 architecture:ArchitectureConfig=Field(default_factory=ArchitectureConfig)
 target_audience:str|None=Field(default=None,max_length=300)
 requirements:list[str]=Field(default_factory=list,max_length=100)
 features:list[str]=Field(default_factory=list,max_length=100)
 integrations:list[str]=Field(default_factory=list,max_length=50)
 deployment_targets:list[str]=Field(default_factory=list,max_length=20)
 constraints:list[str]=Field(default_factory=list,max_length=50)
 options:dict[str,str|int|float|bool]=Field(default_factory=dict)
 @field_validator("name")
 @classmethod
 def valid_name(cls,v):
  if not v.strip(): raise ValueError("Project name cannot be blank")
  return v
 @field_validator("slug")
 @classmethod
 def valid_slug(cls,v):
  if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",v): raise ValueError("Invalid project slug")
  return v
 @field_validator("requirements","features","integrations","deployment_targets","constraints")
 @classmethod
 def clean_items(cls,values):
  return list(dict.fromkeys(x.strip() for x in values if x and x.strip()))
 @model_validator(mode="after")
 def validate_platforms(self):
  if not self.platforms: raise ValueError("At least one target platform is required")
  if self.application_type==ApplicationType.MOBILE and not any(p in self.platforms for p in (Platform.ANDROID,Platform.IOS)): raise ValueError("Mobile apps require Android or iOS")
  if self.application_type==ApplicationType.API and Platform.REST_API not in self.platforms: raise ValueError("API apps require rest-api platform")
  if self.application_type==ApplicationType.HYBRID and len(self.platforms)<2: raise ValueError("Hybrid apps require two platforms")
  return self
class BuildResult(BaseModel):
 project_name:str
 output_path:str
 files_created:int=0
 validation_passed:bool=False
