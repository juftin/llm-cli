# Contributing

## Environment Setup

This project uses [uv] and [task] to manage this Python packaging
and running all of its development tasks.

1. Install [uv](https://github.com/astral-sh/uv)

    <details open>
    <summary>Linux / macOS </summary>

    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    </details>

    <details>
    <summary>brew</summary>

    ```shell
    brew install uv
    ```

    </details>

    <details>
    <summary>Windows</summary>

    ```shell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    </details>

2. Install [task](https://github.com/go-task/task)

      <details open>
      <summary>Linux / macOS </summary>

    ```shell
    sh -c "$(curl -LsSf https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
    ```

      </details>

      <details>
      <summary>brew</summary>

    ```shell
    brew install go-task
    ```

      </details>

      <details>
      <summary>Windows</summary>

    You can use `Chocolatey`, `Scoop`, or `Winget`.
    Read more in the [task installation guide](https://taskfile.dev/installation/).

    ```shell
    choco install go-task
    scoop install task
    winget install Task.Task
    ```

      </details>

3. Build the Virtual Environment

    ```shell
    task install
    ```

4. Activate the Virtual Environment

    ```shell
    source .venv/bin/activate
    ```

## Using Task

### Taskfile Cheat Sheet

| Command Description      | Command           | Notes                                               |
| ------------------------ | ----------------- | --------------------------------------------------- |
| Install Project          | `task install`    | Installs the project and development dependencies   |
| Run Tests                | `task test`       | Runs tests with `pytest` and `coverage`             |
| Run Formatting           | `task fmt`        | Runs `ruff` and `pre-commit` code formatters        |
| Run Linting              | `task lint`       | Runs `ruff` code linter                             |
| Run Type Checking        | `task check`      | Runs `mypy` static type checker                     |
| Run Code Fixers          | `task fix`        | Runs `ruff` and `pre-commit` to format and fix code |
| Build the Artifacts      | `task build`      | Build the Python Package and Docker Artifacts       |
| Build the Docker Image   | `task docker`     | Build the Docker Image with the `docker` CLI        |
| Serve the Documentation  | `task docs`       | Serves the documentation on `localhost:8000`        |
| Run a Command            | `task run`        | Run a shell command: `task run -- which python`     |
| Run the pre-commit Hooks | `task pre-commit` | Runs the `pre-commit` hooks                         |

To see all available commands, simply ask `task`:

```bash exec="on" result="markdown" source="tabbed-left" tabs="task CLI|Output"
task --list
```

## Committing Code

This project uses [pre-commit] to run a set of
checks on the code before it is committed. The pre-commit hooks are
installed by hatch automatically when you run it for the first time.

This project uses [semantic-versioning] standards, managed by [semantic-release].
Releases for this project are handled entirely by CI/CD via pull requests being
merged into the `main` branch. Contributions follow the [gitmoji] standards
with [conventional commits].

While you can denote other changes on your commit messages with [gitmoji], the following
commit message emoji prefixes are the only ones to trigger new releases:

| Emoji | Shortcode     | Description                 | Semver |
| ----- | ------------- | --------------------------- | ------ |
| 💥    | \:boom\:      | Introduce breaking changes. | Major  |
| ✨    | \:sparkles\:  | Introduce new features.     | Minor  |
| 🐛    | \:bug\:       | Fix a bug.                  | Patch  |
| 🚑    | \:ambulance\: | Critical hotfix.            | Patch  |
| 🔒    | \:lock\:      | Fix security issues.        | Patch  |

Most features can be squash merged into a single commit on a pull-request.
When merging multiple commits, they will be summarized into a single release.

If you're working on a new feature, your commit message might look like:

```text
✨ New Feature Description
```

Bug fix commits would look like this:

```text
🐛 Bug Fix Description
```

If you're working on a feature that introduces breaking changes, your
commit message might look like:

```text
💥 Breaking Change Description
```

Other commits that don't trigger a release, but get included in the
release notes might look like:

```text
📝 Documentation Update Description
👷 CI/CD Update Description
🧪 Testing Changes Description
🚚 Moving/Renaming Description
⬆️ Dependency Upgrade Description
```

### Pre-Releases

[semantic-release] supports pre-releases. To trigger a pre-release, you
would merge your pull request into an `alpha` or `beta` branch.

### Specific Release Versions

In some cases you need more advanced control around what kind of release you
need to create. If you need to release a specific version, you can do so by creating a
new branch with the version number as the branch name. For example, if the
current version is `2.3.2`, but you need to release a fix as `1.2.5`, you
would create a branch named `1.2.x` and merge your changes into that branch.

See the [semantic-release documentation] for more information about
branch based releases and other advanced release cases.

[pipx]: https://pypa.github.io/pipx/
[pre-commit]: https://pre-commit.com/
[gitmoji]: https://gitmoji.dev/
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[semantic-release]: https://github.com/semantic-release/semantic-release
[semantic-versioning]: https://semver.org/
[semantic-release documentation]: https://semantic-release.gitbook.io/semantic-release/usage/configuration#branches
[uv]: https://github.com/astral-sh/uv
[task]: https://github.com/go-task/task
