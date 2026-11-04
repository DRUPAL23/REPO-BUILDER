from __future__ import annotations
from dataclasses import dataclass
import re
from repo_builder.models import ApplicationType,Platform,ProjectSpec
@dataclass(frozen=True)
class PlanningIssue:
 code:str
 message:str
 severity:str="warning"
@dataclass(frozen=True)
class PlanningResult:
 application_type:ApplicationType
 platforms:tuple[Platform,...]
 features:tuple[str,...]
 issues:tuple[PlanningIssue,...]
 @property
 def valid(self): return not any(x.severity=="error" for x in self.issues)
DEPENDENCIES={"admin dashboard":("user authentication",),"role-based access":("user authentication",),"subscriptions":("payments","user authentication"),"order management":("payments",),"mpesa payments":("payments",)}
ALIASES={"mpesa":"mpesa payments","m-pesa":"mpesa payments","login":"user authentication","authentication":"user authentication"}
def classify_application_type(brief:str):
 text=brief.lower()
 mobile=bool(re.search(r"\b(mobile app|android app|ios app|iphone app)\b",text))
 api=bool(re.search(r"\b(rest api|backend api|api service|public api)\b",text))
 saas=bool(re.search(r"\b(saas|subscription platform|multi-tenant)\b",text))
 web=bool(re.search(r"\b(website|web app|web application|marketplace|dashboard|e-commerce|ecommerce)\b",text))
 ps=[]
 if web or not(mobile or api): ps.append(Platform.WEB)
 if mobile:
  if "android" in text: ps.append(Platform.ANDROID)
  if "ios" in text or "iphone" in text: ps.append(Platform.IOS)
  if not any(p in ps for p in (Platform.ANDROID,Platform.IOS)): ps.extend([Platform.ANDROID,Platform.IOS])
 if api: ps.append(Platform.REST_API)
 ps=list(dict.fromkeys(ps))
 kind=ApplicationType.SAAS if saas else ApplicationType.HYBRID if len(ps)>1 else ApplicationType.MOBILE if mobile else ApplicationType.API if api else ApplicationType.WEB
 return kind,ps
def normalize_features(features):
 out=[]
 for item in features:
  value=ALIASES.get(item.strip().lower(),item.strip().lower())
  if value and value not in out: out.append(value)
 return out
def plan_project(spec:ProjectSpec):
 features=normalize_features(spec.features); issues=[]
 for feature in features:
  for dep in DEPENDENCIES.get(feature,()):
   if dep not in features: issues.append(PlanningIssue("missing_feature_dependency",f"{feature} requires {dep}."))
 if spec.application_type==ApplicationType.SAAS and not spec.architecture.multi_tenant:
  issues.append(PlanningIssue("saas_tenancy_not_enabled","Confirm whether SaaS tenant isolation is required."))
 return PlanningResult(spec.application_type,tuple(spec.platforms),tuple(features),tuple(issues))
