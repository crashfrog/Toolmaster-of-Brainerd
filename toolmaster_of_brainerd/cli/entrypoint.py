import click
import sys
import strictyaml
import logging

from toolmaster_of_brainerd.toolmaster_of_brainerd import main

logging.basicConfig(level=logging.INFO)

class YamlFile(click.ParamType):
    name = 'tomlfile'

    def convert(self, value, param, ctx):
        try:
            with open(value, 'r') as f:
                return strictyaml.load(f.read())
        except IOError:
            self.fail(f"Could not open file {value!r}", param, ctx)
        except strictyaml.YAMLError as e:
            self.fail(f"Error decoding TOML in {value!r}: {e}", param, ctx)



@click.command()
@click.argument('layout', type=click.Path(dir_okay=False, exists=True))
@click.option('-o', '--output', type=click.File(mode='w'), default='-')
@click.option('-c', '--config', type=YamlFile(), default=".toolmasterofbrainerd/config.yaml",
              help='Configuration options in TOML format')
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
def cli(layout,  output, config, verbose=0):
    return main(config, layout, output, verbose=verbose)



if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
