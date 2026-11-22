# Exercise 07: Two projects, two green test runs

Pick **two** projects that use different setups. Some suggestions (check
their current CONTRIBUTING, these change):

| Project | Clone |
|---|---|
| requests | `git clone https://github.com/psf/requests.git` |
| rich | `git clone https://github.com/Textualize/rich.git` |
| httpx | `git clone https://github.com/encode/httpx.git` |
| flask | `git clone https://github.com/pallets/flask.git` |

You're only *reading and testing* here, so a plain clone is fine. You'll
fork the project you actually contribute to later.

For each project:

- [ ] Clone it next to your course folder (not inside it)
- [ ] Read its CONTRIBUTING file
- [ ] Run `python3 tools/which_setup.py ../PROJECT` from the course folder
- [ ] Set it up the way CONTRIBUTING says
- [ ] Run the test suite (or one test file) until it's green
- [ ] Write down: which tool, which commands, how long the tests took

**Stuck for more than 20 minutes?** Search the project's issues for your
error message. If nothing helps, try the other project, and note what
failed: you just found a possible docs contribution.

**Stretch:** run the project's linters too (`pre-commit run --all-files`, or
the `lint` session in tox or nox).
