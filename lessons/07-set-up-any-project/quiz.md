# Quiz 07

**1. A project has `uv.lock` in its top folder. How do you run its tests?**

<details><summary>Answer</summary>

`uv sync`, then `uv run pytest`, unless CONTRIBUTING says otherwise.
</details>

**2. You clone a project, set it up and run the tests. Three fail. You
haven't changed anything. What now?**

<details><summary>Answer</summary>

It's a setup problem (or a known failure), not your change. Re-read
CONTRIBUTING, check the Python version, search the issues for the error,
and ask if you're stuck. Don't start your change until you know why.
</details>

**3. What does `-e` do in `python -m pip install -e .`?**

<details><summary>Answer</summary>

Installs the project in editable mode: Python uses your working copy, so
your code changes take effect without reinstalling.
</details>

**4. A project has `noxfile.py`. How do you see what it can run?**

<details><summary>Answer</summary>

`nox --list`. Then run one session with `nox -s NAME`.
</details>

**5. How do you run only the tests with "unquote" in their name?**

<details><summary>Answer</summary>

`python -m pytest -k "unquote"` (add a file path to narrow it further).
</details>
