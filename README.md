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

- Install `just`/`make` (for the sake of this spike, I explain how to install both)
  - I did this via `scoop`.  If you don't have scoop, follow the quick-start
  instructions here: https://scoop.sh/
  - Then install `just`/`make` via `scoop`:

    ```
    scoop install just
    scoop install make
    ```

  - If you don't want to use `scoop`, other options are available: https://github.com/casey/just

Restart VSCode to detect installed changes.

At this point, you should be able to press F5 in VSCode and for the game to launch.
