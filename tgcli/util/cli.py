from typing import Optional

import typer


def print_to_console(text: str, is_err: bool = False):
    typer.echo(text, err=is_err)


def get_input_str(prompt: str, hide_input: bool = False, default: Optional = None) -> str:
    return typer.prompt(prompt, hide_input=hide_input, default=default)


def get_input_bool(prompt: str, default: Optional[bool] = False) -> bool:
    return typer.confirm(prompt, default=default)


def terminate(exit_code: int = 0, message: Optional[str] = None, is_err: bool = False):
    if message:
        print_to_console(message, is_err=is_err)
    raise typer.Exit(code=exit_code)
