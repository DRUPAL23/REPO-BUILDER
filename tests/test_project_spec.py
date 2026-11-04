import pytest
from pydantic import ValidationError
from repo_builder.models import ApplicationType,ArchitectureConfig,Platform,ProjectSpec,StackConfig
from repo_builder.planning import classify_application_type,normalize_features,plan_project
def spec(**kw):
 d={"name":"Demo","slug":"demo","description":"Demo application"}; d.update(kw); return ProjectSpec(**d)
def test_schema_round_trip():
 x=spec(); assert ProjectSpec.model_validate_json(x.model_dump_json())==x
 assert x.platforms==[Platform.WEB]
def test_rejects_invalid_slug_and_unknown_fields():
 with pytest.raises(ValidationError): spec(slug="../bad")
 with pytest.raises(ValidationError): spec(extra=True)
def test_platform_constraints():
 with pytest.raises(ValidationError): spec(application_type="mobile",platforms=["web"])
 with pytest.raises(ValidationError): spec(application_type="api",platforms=["web"])
 assert spec(application_type="mobile",platforms=["android"]).platforms==[Platform.ANDROID]
def test_stack_architecture_configuration():
 x=spec(stack_config=StackConfig(frontend="react-native"),architecture=ArchitectureConfig(multi_tenant=True))
 assert x.stack_config.frontend=="react-native" and x.architecture.multi_tenant
def test_application_classification():
 assert classify_application_type("Build an Android mobile app")[0]==ApplicationType.MOBILE
 assert classify_application_type("Create a REST API service")[0]==ApplicationType.API
 assert classify_application_type("Build a SaaS subscription platform")[0]==ApplicationType.SAAS
 kind,platforms=classify_application_type("Build a web app and Android mobile app")
 assert kind==ApplicationType.HYBRID and Platform.WEB in platforms and Platform.ANDROID in platforms
def test_feature_dependency_diagnostics():
 assert normalize_features(["login","admin","login"])==["user authentication","admin"]
 result=plan_project(spec(features=["admin dashboard"]))
 assert result.issues[0].code=="missing_feature_dependency"
 assert "user authentication" in result.issues[0].message
