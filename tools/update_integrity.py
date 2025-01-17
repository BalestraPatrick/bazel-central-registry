import os

import click
from registry import RegistryClient


@click.command()
@click.argument("module")
@click.option("--version")
@click.option("--registry", default=".")
def update_integrity(module, version, registry):
    """Update the SRI hashes in source.json of MODULE."""
    client = RegistryClient(registry)
    if not client.contains(module):
        raise click.BadParameter(f"{module=} not found in registry")
    client.update_versions(module)
    versions = client.get_module_versions(module)
    version = version or versions[-1][1]
    if not client.contains(module, version):
        raise click.BadParameter(f"{version=} not found for {module=}")
    click.echo(f"Updating integrity of {module=} {version=} in {registry=}")
    client.update_integrity(module, version)


if __name__ == "__main__":
    # Under 'bazel run' we want to run within the source folder instead of the execroot.
    if os.getenv("BUILD_WORKSPACE_DIRECTORY"):
        os.chdir(os.getenv("BUILD_WORKSPACE_DIRECTORY"))
    update_integrity()
