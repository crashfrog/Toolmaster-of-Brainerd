import logging
import jinja2

from dataclasses import dataclass, field

from kiutils.board import Board



def sanitize(value):
    "Function to sanitize strings for use in OpenSCAD"
    return value.replace("+", "_plus_") \
                .replace("-", "_") \
                .replace(" ", "_") \
                .replace("(", "_") \
                .replace(")", "_") \
                .replace("[", "_") \
                .replace("]", "_") \
                .replace("{", "_") \
                .replace("}", "_") \
                .replace("/", "_") \
                .replace("\\", "_") \
                .replace(".", "_") \
                .replace(",", "_") \
                .replace(":", "_") \
                .replace(";", "_") \
                .replace("=", "_") \
                .replace("!", "_") \
                .replace("@", "_") \
                .replace("#", "_") \
                .replace("$", "_") \
                .replace("%", "_") \
                .replace("^", "_") \
                .replace("&", "_") \
                .replace("*", "_") \
                .replace("?", "_") \
                .replace("|", "_") \
                .replace("~", "_") \
                .replace("`", "_") \
                .replace("'", "_") \
                .replace('"', "_") \
                .replace("<", "_") \
                .replace(">", "_") \
                .replace(" ", "_") 


def main(config, layout_file, o, verbose=0):
    log = logging.getLogger("toolmaster")
    log.info(f"Starting toolmaster_of_brainerd")
    log.info(f"Reading layout file {layout_file}...")
    board = Board().from_file(layout_file)
    mounting_holes = [footprint for footprint in board.footprints if footprint.tags and "mounting hole" in footprint.tags]
    environment = jinja2.Environment(loader=jinja2.PackageLoader('toolmaster_of_brainerd', 'templates'),
                                     lstrip_blocks=True, trim_blocks=True,
                                     extensions=['jinja2.ext.do'])
    environment.filters['sanitize'] = sanitize
    log = log.getChild("template")
    try:
        o.write(environment.get_template('board_template.scad').render(**locals()))
    except Exception as e:
        log.error(f"Error rendering template")
        raise