# Collection of git hooks to be used with [pre-commit framework](http://pre-commit.com/)


## Table of content

* [Table of content](#table-of-content)
* [How to install](#how-to-install)
  * [1. Install dependencies](#1-install-dependencies)
  * [2. Install the pre-commit hook globally](#2-install-the-pre-commit-hook-globally)
  * [3. Add configs and hooks](#3-add-configs-and-hooks)
  * [4. Run](#4-run)
* [Available Hooks](#available-hooks)


## How to install

### 1. Install dependencies


* [`pre-commit`](https://pre-commit.com/#install)

<details><summary><b>MacOS</b></summary><br>

```bash
brew install pre-commit
```

</details>

### 2. Install the pre-commit hook globally

```bash
DIR=~/.git-template
git config --global init.templateDir ${DIR}
pre-commit init-templatedir -t pre-commit ${DIR}
```

### 3. Add configs and hooks

Step into the repository you want to have the pre-commit hooks installed and run:

```bash
git init
cat <<EOF > .pre-commit-config.yaml
repos:
- repo: https://github.com/Smarterly/pre-commit.git
  rev: <VERSION> # Get the latest from: https://github.com/Smarterly/pre-commit.git/releases
  hooks:
    - id: php_style_check
EOF
```

### 4. Run

Execute this command to run `pre-commit` on all files in the repository (not only changed files):

```bash
pre-commit run -a
```

## Available Hooks

The available [pre-commit](https://pre-commit.com/) hooks currently supported are:

### php_style_check
