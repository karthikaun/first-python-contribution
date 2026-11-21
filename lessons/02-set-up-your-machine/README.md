# Lesson 02: Set up your machine

**Time:** 3 minute video · 20–30 minute exercise (mostly installers)
**You'll need:** the fork you made in Lesson 01

In Lesson 01 you did everything in the browser. Real projects need you to
run their code and tests on your own computer, so now you install the three
tools every Python contributor uses:

| Tool | What it's for |
|---|---|
| **git** | Tracks changes and makes commits on your computer. |
| **GitHub CLI (`gh`)** | Talks to GitHub from the terminal: logs you in, clones, opens pull requests. |
| **Python** | Runs the project's code and tests. You need 3.10 or newer. |

> **Windows users:** install Git for Windows (step 1) and use the **Git Bash**
> app it adds for every command in this course. Then the commands are the same
> as on macOS and Linux. Wherever you see `python3`, type `py` instead.

## Step 1: Install git, gh and Python

| | macOS | Windows | Linux (Debian/Ubuntu) |
|---|---|---|---|
| git | `xcode-select --install` | [git-scm.com/downloads](https://git-scm.com/downloads) | `sudo apt install git` |
| gh | `brew install gh` ([Homebrew](https://brew.sh)) or the installer from [cli.github.com](https://cli.github.com) | `winget install --id GitHub.cli` | [cli.github.com instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) |
| Python | Installer from [python.org/downloads](https://www.python.org/downloads/) | Installer from [python.org/downloads](https://www.python.org/downloads/) | `sudo apt install python3 python3-venv python3-pip` |

On Windows, tick **Add python.exe to PATH** in the Python installer.

Close and reopen your terminal after installing, so it finds the new tools.

## Step 2: Check the versions

```bash
git --version
python3 --version
gh --version
```

You want git 2.28 or newer and Python 3.10 or newer. If a command says
"not found", the install didn't finish or the terminal needs reopening.

## Step 3: Tell git who you are, privately

Every commit records a name and an email, and anyone can read them once you
push. GitHub gives you a private **noreply** address to use instead of your
real email:

1. On GitHub, open **Settings → Emails**.
2. Tick **Keep my email addresses private**. Also tick **Block command line
   pushes that expose my email**.
3. Copy the address shown there. It looks like
   `12345678+your-username@users.noreply.github.com`.

Then tell git (use your own name and that address):

```bash
git config --global user.name "Your Name"
git config --global user.email "12345678+your-username@users.noreply.github.com"
git config --global init.defaultBranch main
git config --global --list
```

The last command shows what you set. `--global` means "for every repo on this
computer", so you only do this once.

## Step 4: Log in with gh

```bash norun
gh auth login
```

(Not run in CI: it logs in to your own account.) Answer the questions:

1. **Where do you use GitHub?** GitHub.com
2. **Preferred protocol for Git operations?** HTTPS
3. **Authenticate Git with your GitHub credentials?** Yes
4. **How would you like to authenticate?** Login with a web browser

gh shows a one-time code and opens your browser. Paste the code, approve, and
come back. Check it worked:

```bash norun
gh auth status
```

## Step 5: Clone your fork

In Lesson 01 you forked the course repo on GitHub. Now download your fork
(replace `YOUR-USERNAME`):

```bash norun
gh repo clone YOUR-USERNAME/first-python-contribution
cd first-python-contribution
git remote -v
```

You'll see two **remotes**, two places this copy is connected to:

```text
origin    https://github.com/YOUR-USERNAME/first-python-contribution.git (fetch)
origin    https://github.com/YOUR-USERNAME/first-python-contribution.git (push)
upstream  https://github.com/thejesh23/first-python-contribution.git (fetch)
upstream  https://github.com/thejesh23/first-python-contribution.git (push)
```

- **origin** is your fork. You push your work here.
- **upstream** is the original course repo. You get other people's changes from here.

gh adds `upstream` for you because it knows your repo is a fork.

> **Skipped Lesson 01?** Run `gh repo fork thejesh23/first-python-contribution --clone`
> instead. It forks and clones in one go.

## Step 6: Get the latest changes, then run the doctor

Other learners' commits have landed since you forked. Bring your copy up to
date, then run the course's checker:

```bash norun
git pull upstream main
python3 tools/doctor.py
```

Each line should be a green ✔:

```text
✔ Python 3.13.1
✔ venv module available
✔ git 2.47.1
✔ git user.name is 'Ada Lovelace'
✔ git user.email is your private noreply address (12345678+ada@users.noreply.github.com)
✔ gh 2.63.0
✔ gh is logged in as ada
✔ origin is your fork, upstream is the course repo

All set. You're ready for Lesson 03.
```

A red ✘ tells you what to fix. Fix the first one and run it again.

Next: [Lesson 03: just enough git](../03-just-enough-git/).
