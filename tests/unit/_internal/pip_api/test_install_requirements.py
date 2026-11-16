from __future__ import annotations

import typing as _t

import pytest
from pip._internal.req import InstallRequirement

from piptools._internal import _pip_api


@pytest.mark.parametrize("use_pep517", (True, False))
def test_copy_install_requirement_removes_pip_25_3_unsupported_opts(use_pep517):
    req = _pip_api.create_install_requirement_from_line("foolib==0.1")

    updated_req = _pip_api.copy_install_requirement(req, use_pep517=use_pep517)
    assert not hasattr(updated_req, "use_pep517")


@pytest.mark.parametrize(
    ("req_line", "formatted", "editable"),
    (
        pytest.param("foo", "<any>", False, id="bare"),
        pytest.param("foo==1.2", "==1.2", False, id="exact"),
        pytest.param(
            "foo>1.2,~=1.1,<1.5", "~=1.1,>1.2,<1.5", False, id="unsorted-gt-first"
        ),
        pytest.param(
            "foo~=1.1,<1.5,>1.2", "~=1.1,>1.2,<1.5", False, id="unsorted-approx-first"
        ),
        pytest.param(
            "git+https://github.com/django/django.git#egg=django",
            "<any>",
            True,
            id="git(django)",
        ),
        pytest.param("file:///home/user/package", "<any>", True, id="file://..."),
    ),
)
def test_format_specifier(
    req_line: str,
    formatted: str,
    editable: bool,
    from_line: _t.Callable[[str], InstallRequirement],
    from_editable: _t.Callable[[str], InstallRequirement],
) -> None:
    """Test that a requirement gets its specifier set formatted as expected."""
    if editable:
        ireq = from_editable(req_line)
    else:
        ireq = from_line(req_line)
    assert _pip_api.format_specifier(ireq) == formatted
