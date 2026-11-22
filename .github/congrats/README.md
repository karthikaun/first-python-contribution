# Maintainer congratulations

When a learner's first commit (Lesson 02) or Exercise 2 pull request (Lesson 05)
passes the bot's checks, the workflow approves the pull request with one of
these messages, posted from the maintainer's own GitHub account, then merges it.

`{login}` is replaced with the learner's GitHub username. Edit the messages
freely; they're read from `main` on every run.

The review is posted with the `MAINTAINER_TOKEN` repository secret: a
fine-grained personal access token for this repository only, with
**Pull requests: Read and write**. Without the secret the step is skipped and
the bot still merges.
