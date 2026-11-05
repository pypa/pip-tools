# Control Unsafe Packages

`pip-compile` treats a few packages as unsafe to pin.
By default these are `pip`, `setuptools` and the long-retired `distribute`,
since they're the tools doing the installing.
Users can pin them anyway, or choose their own list, which is also a way to
keep a package out of the output entirely.

## See the Default Output

Suppose your `requirements.in` lists `setuptools` and `six`.
`six` is pinned as usual, but `setuptools` ends up at the bottom as a comment:

```console
$ pip-compile --no-header requirements.in
six==1.17.0
    # via -r requirements.in

# The following packages are considered to be unsafe in a requirements file:
# setuptools
```

Because it's only a comment, `pip install -r requirements.txt` won't install it.

## Pin Unsafe Packages

Pass [`--allow-unsafe`](/reference/pip-compile) to pin them like any other
package:

```console
$ pip-compile --no-header --allow-unsafe requirements.in
six==1.17.0
    # via -r requirements.in

# The following packages are considered to be unsafe in a requirements file:
setuptools==84.2.1
    # via -r requirements.in
```

This will be the default in the next major release.
To keep the current behavior after that, pass
[`--no-allow-unsafe`](/reference/pip-compile).

## Use Unsafe Packages With Hashes

With [`--generate-hashes`](/reference/pip-compile), leaving unsafe packages
unpinned can break installs.
pip refuses to install an unpinned package from a file that has hashes, unless
it's already installed, so `pip-compile` warns you:

```console
$ pip-compile --no-header --generate-hashes requirements.in
six==1.17.0     --hash=sha256:...
    # via -r requirements.in

# WARNING: The following packages were not pinned, but pip requires them to be
# pinned when the requirements file includes hashes and the requirement is not
# satisfied by a package already installed. Consider using the --allow-unsafe flag.
# setuptools
```

Pass `--allow-unsafe` as well to pin them with their hashes.

## Choose Which Packages Are Unsafe

Pass [`--unsafe-package`](/reference/pip-compile) to name the packages
yourself.
It replaces the default list instead of adding to it, so `setuptools` is pinned
again here:

```console
$ pip-compile --no-header --unsafe-package six requirements.in
setuptools==84.2.1
    # via -r requirements.in

# The following packages are considered to be unsafe in a requirements file:
# six
```

To keep the defaults as well, repeat the option for each package:

```console
$ pip-compile --no-header --unsafe-package six --unsafe-package setuptools requirements.in

# The following packages are considered to be unsafe in a requirements file:
# setuptools
# six
```

## Combine Both Options

If you pass both, `--allow-unsafe` takes priority.
Packages named with `--unsafe-package` are still listed in the unsafe section,
but they're pinned:

```console
$ pip-compile --no-header --allow-unsafe --unsafe-package six requirements.in
setuptools==84.2.1
    # via -r requirements.in

# The following packages are considered to be unsafe in a requirements file:
six==1.17.0
    # via -r requirements.in
```

## Keep Your Own Project Out of the Output

An extra can refer back to its own project to reuse other extras:

```toml
[project.optional-dependencies]
test = ["iniconfig"]
dev = ["foo-example[test]"]
```

Compiling `dev` then lists `foo-example` itself, pinned to a local path:

```console
$ pip-compile --no-header --extra dev pyproject.toml
foo-example[test] @ file:///path/to/project
    # via foo-example (pyproject.toml)
iniconfig==2.3.1
    # via foo-example
```

To leave it out, mark your project as unsafe:

```console
$ pip-compile --no-header --extra dev --unsafe-package foo-example pyproject.toml
iniconfig==2.3.1
    # via foo-example

# The following packages are considered to be unsafe in a requirements file:
# foo-example
```
