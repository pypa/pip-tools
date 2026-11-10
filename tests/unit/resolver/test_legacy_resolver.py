"""
Test the ``LegacyResolver`` class in pip-tools, which wraps pip usage of the legacy
(non-backtracking) resolver.
"""

from __future__ import annotations

import contextlib
import pathlib

import pytest

from piptools.cache import DependencyCache
from piptools.exceptions import PipToolsError
from piptools.repositories.base import BaseRepository
from piptools.resolver import LegacyResolver


@pytest.mark.parametrize(
    (
        "deprecated_pip_features",
        "expected_error_ctx",
    ),
    (
        pytest.param(
            ["legacy-resolver"],
            contextlib.nullcontext(),
            id="legacy-resolver",
        ),
        pytest.param(
            [],
            pytest.raises(
                PipToolsError,
                match=r"Legacy resolver deprecated feature must be enabled\.",
            ),
            id="resolvelib",
        ),
    ),
)
def test_legacy_resolver_init_only_succeeds_if_flag_is_enabled(
    repository: BaseRepository,
    depcache: DependencyCache,
    tmp_path: pathlib.Path,
    deprecated_pip_features: list[str],
    expected_error_ctx: contextlib.AbstractContextManager[object],
) -> None:
    """
    Test that, given a repository object, a legacy resolver can only be initialized if
    the options contain the ``legacy-resolver`` flag.
    """
    repository.options.deprecated_features_enabled = deprecated_pip_features

    # `expected_error_ctx` is a `pytest.raises()` context manager or
    # a `nullcontext` depending on which case we are testing --
    # `nullcontext` effectively requires that is no error
    with expected_error_ctx:
        LegacyResolver(
            repository=repository,
            constraints=[],
            existing_constraints={},
            cache=depcache,
        )
