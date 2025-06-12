import logging
import jinja2

from dataclasses import dataclass, field

from kiutils.board import Board
from kiutils.items.gritems import GrLine
from kiutils.items.common import Position


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



def polygonize(items):
    index = {(i.start.X, i.start.Y):i for i in items}
    yield items[0]
    i = index[(items[0].end.X, items[0].end.Y)]
    while i is not items[0]:
        yield i
        i = index[(i.end.X, i.end.Y)]

def main(config, layout_file, o, verbose=0):
    # Set up the render context
    log = logging.getLogger("toolmaster")
    log.info(f"Starting toolmaster_of_brainerd")
    log.info(f"Reading layout file {layout_file}...")
    board = Board().from_file(layout_file)
    mounting_holes = [footprint for footprint in board.footprints if footprint.tags and "mounting hole" in footprint.tags]
    perimeter = [gr for gr in board.graphicItems if isinstance(gr, GrLine) and gr.layer == "Edge.Cuts"]
    width = max([gr.start.X for gr in board.graphicItems if isinstance(gr, GrLine)]) - min([gr.start.X for gr in board.graphicItems if isinstance(gr, GrLine)])
    height = max([gr.start.Y for gr in board.graphicItems if isinstance(gr, GrLine)]) - min([gr.start.Y for gr in board.graphicItems if isinstance(gr, GrLine)])
    environment = jinja2.Environment(loader=jinja2.PackageLoader('toolmaster_of_brainerd', 'templates'),
                                     lstrip_blocks=True, trim_blocks=True,
                                     extensions=['jinja2.ext.do'])
    environment.filters['sanitize'] = sanitize
    environment.filters['isinstance'] = isinstance
    environment.filters['polygonize'] = polygonize
    log = log.getChild("template")
    try:
        o.write(environment.get_template('board_template.scad').render(**locals()))
    except Exception as e:
        log.error(f"Error rendering template")
        raise