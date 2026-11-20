# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The custom openapi templates, rendered with the generator's own Jinja settings."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest
from jinja2 import Environment, FileSystemLoader

from scripts.generation._shared import REGENERATE_COMMAND

_TEMPLATES = Path(__file__).resolve().parents[2] / "scripts" / "openapi_templates"
_TEXT = 'Use "equals" & <b>\\d+</b>.\n\nNot """ this.'


@pytest.fixture
def env() -> Environment:
    environment = Environment(
        loader=FileSystemLoader(_TEMPLATES), autoescape=True, trim_blocks=True
    )
    environment.filters["normalize_symbol"] = lambda name: name
    return environment


def _model_class(env: Environment, schema, properties) -> ast.ClassDef:
    source = env.get_template("models_pydantic_2.jinja2").render(
        schema_name="Thing", schema=schema, properties=properties
    )
    return next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef))


def _property(name: str) -> SimpleNamespace:
    return SimpleNamespace(
        name=name,
        type=SimpleNamespace(converted_type="Optional[str]", import_types=None),
        required=False,
        default="None",
    )


def test_model_docstring_and_field_description_keep_the_schema_text(env):
    schema = SimpleNamespace(
        title="Thing",
        description=_TEXT,
        properties={"op": SimpleNamespace(title=None, description=_TEXT)},
    )

    cls = _model_class(env, schema, [_property("op")])

    assert ast.get_docstring(cls) == f"Thing\n\n{_TEXT}"
    field = next(n for n in cls.body if isinstance(n, ast.AnnAssign))
    assert isinstance(field.value, ast.Call)
    keywords = {k.arg: ast.literal_eval(k.value) for k in field.value.keywords}
    assert keywords["description"] == _TEXT


def test_field_without_schema_text_gets_no_description(env):
    schema = SimpleNamespace(
        title=None,
        description=None,
        properties={"ref": SimpleNamespace(ref="#/components/schemas/Other")},
    )

    cls = _model_class(env, schema, [_property("ref")])

    assert ast.get_docstring(cls) == "Thing model"
    field = next(n for n in cls.body if isinstance(n, ast.AnnAssign))
    assert isinstance(field.value, ast.Call)
    assert "description" not in {k.arg for k in field.value.keywords}


def _model_type(env: Environment, additional_properties) -> type:
    schema = SimpleNamespace(
        title=None,
        description=None,
        properties={"metric": SimpleNamespace(title=None, description=None)},
        additionalProperties=additional_properties,
    )
    source = env.get_template("models_pydantic_2.jinja2").render(
        schema_name="Thing", schema=schema, properties=[_property("metric")]
    )
    namespace: dict = {}
    exec(compile(source, "<template>", "exec"), namespace)  # noqa: S102 - runs the rendered template under test
    return namespace["Thing"]


def test_additional_properties_true_keeps_and_sends_unknown_fields(env):
    thing = _model_type(env, True)(metric="bytes", cutFnRegex={"a": 1})

    assert thing.model_dump(by_alias=True, exclude_unset=True) == {
        "metric": "bytes",
        "cutFnRegex": {"a": 1},
    }


@pytest.mark.parametrize(
    "additional_properties", [None, False, SimpleNamespace(type="string")]
)
def test_other_schemas_keep_dropping_unknown_fields(env, additional_properties):
    thing = _model_type(env, additional_properties)(metric="bytes", extra=1)

    assert thing.model_dump(by_alias=True, exclude_unset=True) == {"metric": "bytes"}


def _rest_function(env: Environment, summary, description) -> ast.FunctionDef:
    source = env.get_template("httpx.jinja2").render(
        async_client=False,
        operation_id="ListThings",
        params="",
        query_params=[],
        header_params=[],
        body_param=None,
        method="get",
        path_name="/things",
        return_type=SimpleNamespace(type=None, status_code=200),
        operation={"summary": summary, "description": description},
    )
    function = ast.parse(source).body[0]
    assert isinstance(function, ast.FunctionDef)
    return function


@pytest.mark.parametrize(
    ("summary", "description", "expected"),
    [
        ("List things.", _TEXT, f"List things.\n\n{_TEXT}"),
        ("List things.", "List things.", "List things."),
        (None, None, None),
    ],
)
def test_rest_function_docstring_is_the_summary_and_description(
    env, summary, description, expected
):
    function = _rest_function(env, summary, description)

    assert ast.get_docstring(function) == expected


def test_service_template_header_names_the_regenerate_command():
    header = (_TEMPLATES / "service.jinja2").read_text(encoding="utf-8").splitlines()[1]
    assert header == f"# Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand."
