# Your First Python Contribution

A free video course that takes you from "I've never opened a pull request"
to a merged contribution to a real Python project.

- **Lesson 01 needs no install.** You open your first pull request in the
  browser and a bot merges it within minutes.
- **Then the real tools:** git, GitHub CLI, virtualenvs, pytest, ruff,
  pre-commit — the things maintainers will actually check.
- **Then a real project:** finding an issue nobody else is working on,
  passing CI, handling review, and using AI tools without annoying maintainers.
- **You finish with a merged PR in a project you chose**, verified by a bot
  and added to the graduates wall. After that you can contribute anywhere.

👉 Start with [the curriculum](CURRICULUM.md).

The hands-on exercises happen right here: in Lesson 01 you star and fork
this repo, then add your own file to [`first-commits/`](first-commits/) as
your first commit. A bot checks it and merges it.

## How this course is made

Lessons and video scripts are drafted with AI and **reviewed by a human
before anything is published**. Commands shown in lessons are run in CI
(`tools/test_commands.py`); the few that need your own account, like logging
in, are marked and explained. Videos are generated from the scripts in this repo
(`tools/render_video.py`), so fixing a mistake means fixing a text file and
re-rendering. If you spot something wrong, please
[open an issue](../../issues) — that's a contribution too.

## Repo layout

```
lessons/NN-slug/   README.md, script.md, exercise.md, quiz.md
first-commits/     one file per learner, added in Lesson 01
tools/             lesson checker, video renderer (Python)
tests/             tests for the tools and lesson structure
```

## Working on the course

```bash
uv run pytest           # check lesson structure and tools
uv run ruff check .     # lint
uv run python tools/render_video.py lessons/00-what-counts   # render a video
```

## License

Code is [MIT](LICENSE). Lesson text and videos are
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
