from __future__ import annotations

import pytest

from piptools._internal import _pip_api


@pytest.mark.parametrize("use_pep517", (True, False))
def test_copy_install_requirement_removes_pip_25_3_unsupported_opts(use_pep517):
    req = _pip_api.create_install_requirement_from_line("foolib==0.1")

    updated_req = _pip_api.copy_install_requirement(req, use_pep517=use_pep517)
    assert not hasattr(updated_req, "use_pep517")
