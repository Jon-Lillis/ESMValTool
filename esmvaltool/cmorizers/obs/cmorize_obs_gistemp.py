"""ESMValTool CMORizer for CRU data.

Tier
    Tier 2: other freely-available dataset.

Source
    https://data.giss.nasa.gov/gistemp/
    https://data.giss.nasa.gov/pub/gistemp/gistemp250_GHCNv4.nc.gz

Last access
    20200303

"""

import gzip
import logging
import os
import shutil

import iris

from . import utilities as utils

logger = logging.getLogger(__name__)


def _clean(filepath):
    """Remove unzipped input file."""
    if os.path.isfile(filepath):
        os.remove(filepath)
        logger.info("Removed cached file %s", filepath)


def _extract_variable(short_name, var, cfg, filepath, out_dir):
    """Extract variable."""
    raw_var = var.get('raw', short_name)
    cube = iris.load_cube(filepath, utils.var_name_constraint(raw_var))

    # Fix units
    cmor_info = cfg['cmor_table'].get_variable(var['mip'], short_name)
    cube.convert_units(cmor_info.units)
    utils.convert_timeunits(cube, 1950)

    # Fix coordinates
    utils.fix_coords(cube)
    utils.add_height2m(cube)

    # Fix metadata
    attrs = cfg['attributes']
    attrs['mip'] = var['mip']
    utils.fix_var_metadata(cube, cmor_info)
    utils.set_global_atts(cube, attrs)

    # Save variable
    utils.save_variable(cube,
                        short_name,
                        out_dir,
                        attrs,
                        unlimited_dimensions=['time'])


def _unzip(short_name, var, raw_filepath, out_dir):
    """Unzip `*.gz` file."""
    raw_var = var.get('raw', short_name)
    zip_path = raw_filepath.format(raw_name=raw_var)
    if not os.path.isfile(zip_path):
        logger.debug("Skipping '%s', file '%s' not found", short_name,
                     zip_path)
        return None
    logger.info("Found input file '%s'", zip_path)
    filename = os.path.basename(zip_path.replace('.gz', ''))
    new_path = os.path.join(out_dir, filename)
    with gzip.open(zip_path, 'rb') as zip_file:
        with open(new_path, 'wb') as new_file:
            shutil.copyfileobj(zip_file, new_file)
    logger.info("Succefully extracted file to %s", new_path)
    return new_path


def cmorization(in_dir, out_dir, cfg, _):
    """Cmorization func call."""
    raw_filepath = os.path.join(in_dir, cfg['filename'])

    # Run the cmorization
    for (short_name, var) in cfg['variables'].items():
        logger.info("CMORizing variable '%s'", short_name)
        filepath = _unzip(short_name, var, raw_filepath, out_dir)
        if filepath is None:
            continue
        _extract_variable(short_name, var, cfg, filepath, out_dir)
        _clean(filepath)
