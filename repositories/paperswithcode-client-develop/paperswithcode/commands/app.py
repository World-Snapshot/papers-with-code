import json
import rich
from typer import Typer

from paperswithcode import errors
from paperswithcode.config import config


config_app = Typer(name="config", help="Configuration management.")


@config_app.command(name="list")
def list_values():
    """List all configuration values."""
    if config.format == config.Format.text:
        for i, (key, entries) in enumerate(config.entries.items()):
            if i > 0:
                rich.print()
            rich.print(f"[cyan]\\[{key}][/]")
            for entry in entries:
                rich.print(f"[green]{entry.key}[/]: {entry.value}")

    elif config.format == config.Format.json:
        rich.print(
            json.dumps(
                {
                    section: {entry.key: entry.value for entry in entries}
                    for section, entries in config.entries.items()
                },
                indent=2,
            )
        )


@config_app.command(name="set")
def set_value(key: str, value: str):
    """Set a configuration key."""
    try:
        if key.count(".") != 1:
            raise ValueError(
                f"Invalid configuration key: {key}. " f"Valid format: `section.option`"
            )
        section, option = key.split(".")
        for key, field in config.ENTRIES.items():
            if field.section == section and field.option == option:
                config.set(field=key, value=value)
                config.save()
                break
    except errors.InvalidConfiguration:
        raise
    except Exception as e:
        raise errors.InvalidConfiguration(
            key=key,
            value=value,
            error=e,
            operation=errors.InvalidConfiguration.Op.set,
        )
    list_values()


app = Typer(name="pwc", help="PapersWithCode client.")
app.add_typer(config_app, name="config")
