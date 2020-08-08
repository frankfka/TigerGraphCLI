from typing import Optional, Any

import typer


def print_to_console(content: Any, is_err: bool = False, is_header: bool = False):
    """Print some content to console.

    - Specifying is_err may result in special formatting if configured.
    - Specifying is_header will add wrapping symbols to emphasize the content
    """
    if is_header:
        content = f"===== {content} ====="
    typer.echo(content, err=is_err)


def get_input_str(prompt: str, hide_input: bool = False, default: Optional = None) -> str:
    """Prompt for an input string from the user

    - Specifying hide_input will not show the user's current input, useful for passwords
    - Specifying default will return the default if user skips the prompt, otherwise empty values are invalid
    """
    return typer.prompt(prompt, hide_input=hide_input, default=default)


def get_input_bool(prompt: str, default: Optional[bool] = False) -> bool:
    """Prompt for a yes/no boolean from the user with an optional default"""
    return typer.confirm(prompt, default=default)


def get_input_from_editor(initial_value: str) -> str:
    """Launches the system editor with initial_value and returns the final saved result when user finishes editing"""
    return typer.edit(text=initial_value)


def terminate(exit_code: int = 0, message: Optional[str] = None, is_err: bool = False):
    """Terminates the current CLI session with a given exit code and message"""
    if message:
        print_to_console(message, is_err=is_err)
    raise typer.Exit(code=exit_code)
