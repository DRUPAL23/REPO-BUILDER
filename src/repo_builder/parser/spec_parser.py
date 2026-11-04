"""Convert natural-language briefs into validated project specifications."""
from __future__ import annotations
import re
from collections.abc import Sequence
from repo_builder.models import ProjectSpec
from repo_builder.planning import classify_application_type

_FEATURE_KEYWORDS=(
 ("user authentication",("auth","authentication","login","sign up","signup")),
 ("admin dashboard",("admin","dashboard","back office")),
 ("payments",("payment","checkout","billing","mpesa","m-pesa")),
 ("search",("search","filter")),
 ("notifications",("notification","email alert","sms alert")),
 ("analytics",("analytics","reports","reporting","metrics")),
 ("file uploads",("upload","file attachment","media library")),
 ("API integration",("api","integration","webhook")),
)
def slugify(value:str)->str:
 slug=re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-")
 return slug[:80].strip("-") or "generated-project"
def parse_project_spec(prompt:str,*,name:str|None=None,stack:str="nextjs-fastapi",requirements:Sequence[str]|None=None)->ProjectSpec:
 brief=prompt.strip()
 if not brief: raise ValueError("Project prompt cannot be empty")
 if stack!="nextjs-fastapi": raise ValueError("Only the 'nextjs-fastapi' stack is supported")
 project_name=(name or _infer_name(brief)).strip()
 features=[label for label,keywords in _FEATURE_KEYWORDS if any(k in brief.lower() for k in keywords)]
 kind,platforms=classify_application_type(brief)
 return ProjectSpec(name=project_name,slug=slugify(project_name),description=brief,stack=stack,
                    application_type=kind,platforms=platforms,
                    requirements=list(requirements or []),features=features)
def _infer_name(prompt:str)->str:
 cleaned=re.sub(r"\s+"," ",prompt).strip(" .!?\n\t")
 cleaned=re.sub(r"^(please\s+)?(build|create|develop|make|generate)\s+","",cleaned,flags=re.I)
 clause=re.split(r"[.!?;\n]",cleaned,maxsplit=1)[0]
 clause=re.split(r"\s+(?:with|for|that|which|including|featuring)\s+",clause,maxsplit=1,flags=re.I)[0]
 candidate=" ".join(clause.split()[:6]).strip(" ,:-")
 return candidate[:1].upper()+candidate[1:] if candidate else "Generated Project"
