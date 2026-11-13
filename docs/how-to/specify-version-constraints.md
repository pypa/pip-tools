# Specify Version Constraints

The requirements you give to `pip-compile` -- in a `requirements.in` file,
in `pyproject.toml`, or in `setup.py` / `setup.cfg` -- are
[PEP 508 requirements](https://peps.python.org/pep-0508/).
The version part of each requirement is a set of
[PEP 440 version specifiers](https://peps.python.org/pep-0440/#version-specifiers).
`pip-compile` passes them to the resolver and pins the exact versions it
resolves in the output file, so the specifiers are the constraints, not the
pins.

## The Operators

| Specifier | Meaning | Example |
| --- | --- | --- |
| `==` | Exactly this version | `django==4.2` |
| `>=` | This version or newer | `django>=4.2` |
| `<=` | This version or older | `django<=4.2.11` |
| `>` | Newer than this version | `django>4.2` |
| `<` | Older than this version | `django<5.0` |
| `!=` | Any version except this one | `django!=4.2.1` |
| `~=` | A compatible release (see below) | `django~=4.2` |
| `===` | Arbitrary equality, for versions which are not PEP 440 compliant | `foo===1.0-custom` |

Separate several specifiers with commas to combine them.
All of them must hold at once:

```text
# requirements.in
django>=4.2,<5.0
requests>=2.31,!=2.32.0
```

A bare name with no specifier means any version is acceptable, and
`pip-compile` will pin whichever version the resolver picks:

```text
# requirements.in
django
```

## Compatible Releases With `~=`

`~=` pins a release series instead of a single version.
It means "at least this version, but within the same series":

- `django~=4.2` allows `4.2` and newer `4.x` releases, but not `5.0`.
  It is equivalent to `django>=4.2,==4.*`.
- `django~=4.2.1` allows `4.2.1` and newer `4.2.x` releases, but not `4.3`.
  It is equivalent to `django>=4.2.1,==4.2.*`.

Use it when you want bugfix updates automatically, but not a new minor or
major release.

## If You Are Coming From Another Tool

Other dependency tools spell the same ideas differently.
`pip-compile` has no equivalent of Poetry's caret (`^`) or Bundler's
pessimistic operator (`~>`), so translate them into PEP 440 specifiers:

| Other tool | Equivalent specifier |
| --- | --- |
| Poetry `foo = "^1.2.3"` | `foo>=1.2.3,<2.0.0` |
| Poetry `foo = "~1.2.3"` | `foo~=1.2.3` |
| Bundler `gem "foo", "~> 1.2"` | `foo~=1.2` |
| Bundler `gem "foo", "~> 1.2.3"` | `foo~=1.2.3` |

For the full rules, see the
[PEP 440 version specifiers](https://peps.python.org/pep-0440/#version-specifiers)
and pip's documentation on
[requirement specifiers](https://pip.pypa.io/en/stable/reference/requirement-specifiers/).
