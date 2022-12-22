# top-down twisted metal: sweet tooth's revenge

Trello board: https://trello.com/b/1LSRKOHM/twisted-metal

## Development

Getting started on Windows:

*Easiest to screen-share and ask one of us to walk you through this list.*

- install VSCode: <https://code.visualstudio.com/>
- install Git for Windows: <https://gitforwindows.org/>
  - The installer asks you a lot of options.  Ask one of us for help.
- install the recommended VSCode extensions
  - VSCode should prompt for this when you open our code.
  - Alternatively, open the "Extensions" sidebar, type `@recommended` into the
  search box, and install the items in that list.
- Install Python 3.10
  - Install from the python website; do not use the Windows Store version.
  - Install 3.10, *not* 3.11, because a transitive dependency of `arcade` cannot easily
  be installed on Windows on Python 3.11.
  - https://www.python.org/downloads/
- Install Python dependencies:

    ```
    pip install -r requirements.txt
    ```

- Install `make`
  - I did this via `scoop`.  If you don't have scoop, follow the quick-start
  instructions here: https://scoop.sh/
  - Then install `make` via `scoop`:

    ```
    scoop install make
    ```

Restart VSCode to detect installed changes.

At this point, you should be able to press F5 in VSCode and for the game to launch.

### Install git commit hook (optional)

It's easy to forget to run the formatter.  When configured,
git can double-check this every time we commit.  We have a
makefile target to configure this:

```shell
make install-git-hooks
```

This will install a git pre-commit hook.  When installed, git commit will error
when code doesn't match the formatter.  This is a reminder to press Ctrl+Shift+B
and commit the newly-formatted code.

It works by telling git to run `make check` every time you commit.  See the
`Makefile` for details.
