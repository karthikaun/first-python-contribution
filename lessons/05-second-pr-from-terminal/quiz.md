# Quiz 05

**1. Your username is `Grace-Hopper`. What are your two file names?**

<details><summary>Answer</summary>

`practice/greetings/grace_hopper.py` and `practice/tests/test_grace_hopper.py`.
</details>

**2. Why write the test before the function?**

<details><summary>Answer</summary>

Watching it fail first proves the test really checks something. A test that
passes before you've written any code isn't testing your code.
</details>

**3. Your prompt doesn't start with `(.venv)` and `pytest` says "command not
found". What happened?**

<details><summary>Answer</summary>

The virtual environment isn't active, probably because you opened a new
terminal. Run `source .venv/bin/activate` (or `source .venv/Scripts/activate`
on Windows) from the project folder.
</details>

**4. CI says `ruff format --check` failed. What do you run locally?**

<details><summary>Answer</summary>

`ruff format practice`, then commit and push the reformatted files.
</details>

**5. In pytest's output, which line is what the test expected: `-` or `+`?**

<details><summary>Answer</summary>

`-` is what the test expected; `+` is what your code actually returned.
</details>
