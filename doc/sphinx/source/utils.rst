.. _utils:

Utilities
*********

This section provides information on tools that are useful when developing
ESMValTool.
Tools that are specific to ESMValTool live in the
`esmvaltool/utils <https://github.com/ESMValGroup/ESMValTool/tree/main/esmvaltool/utils>`_
directory, while others can be installed using the usual package managers.

.. _pre-commit:

Pre-commit
==========

`pre-commit <https://pre-commit.com/>`__ is a handy tool that can run many
tools for checking code quality with a single command.
Usually it is used just before committing, to avoid accidentally committing
mistakes.
It knows knows which tool to run for each filetype, and therefore provides
a convenient way to check your code!


To run ``pre-commit`` on your code, go to the ESMValTool directory
(``cd ESMValTool``) and run

::

   pre-commit run

By default, pre-commit will only run on the files that have been changed,
meaning those that have been staged in git (i.e. after
``git add your_script.py``).

To make it only check some specific files, use

::

   pre-commit run --files your_script.py

or

::

   pre-commit run --files your_script.R

Alternatively, you can configure ``pre-commit`` to run on the staged files before
every commit (i.e. ``git commit``), by installing it as a `git hook <https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks>`__ using

::

   pre-commit install

Pre-commit hooks are used to inspect the code that is about to be committed. The
commit will be aborted if files are changed or if any issues are found that
cannot be fixed automatically. Some issues cannot be fixed (easily), so to
bypass the check, run

::

   git commit --no-verify

or

::

   git commit -n

or uninstall the pre-commit hook

::

   pre-commit uninstall


Note that the configuration of pre-commit lives in
`.pre-commit-config.yaml <https://github.com/ESMValGroup/ESMValTool/blob/main/.pre-commit-config.yaml>`_.

.. _nclcodestyle:

nclcodestyle
============

A tool for checking the style of NCL code, based on pycodestyle.
Install ESMValTool in development mode (``pip install -e '.[develop]'``) to make it available.
To use it, run

.. code-block:: bash

    nclcodestyle /path/to/file.ncl

.. _recipe_test_tool:

Colormap samples
================
Tool to generate colormap samples for ESMValTool's default Python and NCL colormaps.

Run

.. code-block:: bash

    esmvaltool colortables python

or

.. code-block:: bash

    esmvaltool colortables ncl

to generate the samples.

.. _running_multiple_recipes:

Running multiple recipes
========================

It is possible to run more than one recipe in one go.
This can for example be achieved by using ``rose`` and/or ``cylc``, tools
that may be available at your local HPC cluster.

Using cylc
----------

A cylc suite for running all recipes is available in
`esmvaltool/utils/testing/regression <https://github.com/ESMValGroup/ESMValTool/blob/main/esmvaltool/utils/testing/regression>`__

To prepare for using this tool:

#. Log in to Mistral or another system that uses `slurm <https://slurm.schedmd.com/quickstart.html>`_
#. Make sure the required CMIP and observational datasets are available and configured in config-user.yml
#. Make sure the required auxiliary data is available (see :ref:`recipe documentation <recipes>`)
#. Install ESMValTool
#. Update config-user.yml so it points to the right data locations

Next, get started with `cylc <https://cylc.github.io/cylc-doc/stable/html/tutorial.html>`_:

#. Run ``module load cylc``
#. Register the suite with cylc ``cylc register run-esmvaltool-recipes ~/ESMValTool/esmvaltool/utils/testing/regression``
#. Edit the suite if needed, this allows e.g. choosing which recipes will be run
#. Validate the suite ``cylc validate run-esmvaltool-recipes --verbose``, this will e.g. list the recipes in the suite
#. Run all recipes ``cylc run run-esmvaltool-recipes``
#. View progress ``cylc log run-esmvaltool-recipes``, use e.g. ``cylc log run-all-esmvaltool-recipes examples-recipe_python_yml.1 --stdout`` to see the log of an individual esmvaltool run. Once the suite has finished running, you will see the message "WARNING - suite stalled" in the log.
#. Stop the cylc run once everything is done ``cylc stop run-esmvaltool-recipes``.
#. Create the index.html overview page by running ``python esmvaltool/utils/testing/regression/summarize.py ~/esmvaltool_output/``

Using Rose and cylc
-------------------
It is possible to run more than one recipe in one go: currently this relies on the user
having access to a HPC that has ``rose`` and ``cylc`` installed since the procedure involves
installing and submitting a Rose suite. The utility that allows you to do this is
``esmvaltool/utils/rose-cylc/esmvt_rose_wrapper.py``.

Base suite
..........
The base suite to run esmvaltool via rose-cylc is `u-bd684`; you can find
this suite in the Met Office Rose repository at:

https://code.metoffice.gov.uk/svn/roses-u/b/d/6/8/4/trunk/

When ``rose`` will be working with python3.x, this location will become
default and the pipeline will aceess it independently of user, unless, of
course the user will specify ``-s $SUITE_LOCATION``; until then the user needs
to grab a copy of it in ``$HOME`` or specify the default location via ``-s`` option.

Environment
...........
We will move to a unified and centrally-installed esmvaltool environment;
until then, the user will have to alter the env_setup script:

``u-bd684/app/esmvaltool/env_setup``

with the correct pointers to esmvaltool installation, if desired.

To be able to submit to cylc, you need to have the `/metomi/` suite in path
AND use a `python2.7` environment. Use the Jasmin-example below for guidance.

Jasmin-example
..............
This shows how to interact with rose-cylc and run esmvaltool under cylc
using this script:

.. code:: bash

   export PATH=/apps/contrib/metomi/bin:$PATH
   export PATH=/home/users/valeriu/miniconda2/bin:$PATH
   mkdir esmvaltool_rose
   cd esmvaltool_rose
   cp ESMValTool/esmvaltool/utils/rose-cylc/esmvt_rose_wrapper.py .
   svn checkout https://code.metoffice.gov.uk/svn/roses-u/b/d/6/8/4/trunk/ ~/u-bd684
   [enter Met Office password]
   [configure ~/u-bd684/rose_suite.conf]
   [configure ~/u-bd684/app/esmvaltool/env_setup]
   python esmvt_rose_wrapper.py -c config-user.yml \
   -r recipe_autoassess_stratosphere.yml recipe_OceanPhysics.yml \
   -d $HOME/esmvaltool_rose
   rose suite-run u-bd684

Note that you need to pass FULL PATHS to cylc, no `.` or `..` because all
operations are done remotely on different nodes.

A practical actual example of running the tool can be found on JASMIN:
``/home/users/valeriu/esmvaltool_rose``.
There you will find the run shell: ``run_example``, as well as an example
how to set the configuration file. If you don't have Met Office credentials,
a copy of `u-bd684` is always located in ``/home/users/valeriu/roses/u-bd684`` on Jasmin.

.. _compare_recipe_runs:

Comparing recipe runs
=====================

A command-line tool is available for comparing one or more recipe runs to
known good previous run(s).
This tool uses `xarray <https://docs.xarray.dev/en/stable/>`_ to compare NetCDF
files and difference hasing provided by
`imagehash <https://pypi.org/project/ImageHash/>`_ to compare PNG images.
All other file types are compared byte for byte.

To use it, first install the package imagehash_:

.. code-block:: bash

   pip install imagehash

Next, go to the location where ESMValTool is installed and run

.. code-block:: bash

    python esmvaltool/utils/testing/regression/compare.py ~/reference_output/ ~/output/recipe_python_20220310_180417/

where the first argument is a reference run or a directory containing such
runs and the second and following arguments are directories with runs to compare
to the reference run(s).

To compare all results from the current version to the previous version, use e.g.:

.. code-block:: bash

    python esmvaltool/utils/testing/regression/compare.py /shared/esmvaltool/v2.4.0 /shared/esmvaltool/v2.5.0

To get more information on how a result is different, run the tool with the
``--verbose`` flag.

Testing recipe settings
=======================

A tool for generating recipes with various diagnostic settings, to test of those work.
Install ESMValTool in development mode (``pip install -e '.[develop]'``) to make it available.
To use it, run

.. code-block:: bash

    test_recipe --help


.. _draft_release_notes.py:

draft_release_notes.py
======================

`draft_release_notes.py <https://github.com/ESMValGroup/ESMValTool/blob/main/esmvaltool/utils/draft_release_notes.py>`__
is a script for drafting release notes based on the titles and labels of
the GitHub pull requests that have been merged since the previous release.

To use it, install the package pygithub_:

.. code-block:: bash

   pip install pygithub

Create a `GitHub access token`_ (leave all boxes for additional
permissions unchecked) and store it in the file ``~/.github_api_key``.

Edit the script and update the date and time of the previous release and run
the script:

.. code-block:: bash

   python esmvaltool/utils/draft_release_notes.py ${REPOSITORY}

``REPOSITORY`` can be either ``esmvalcore`` or ``esmvaltool`` depending on the
release notes you want to create.

Review the resulting output (in ``.rst`` format) and if anything needs changing,
change it on GitHub and re-run the script until the changelog looks acceptable.
In particular, make sure that pull requests have the correct label, so they are
listed in the correct category.
Finally, copy and paste the generated content at the top of the changelog.

Converting Version 1 Namelists to Version 2 Recipes
===================================================

The
`xml2yml <https://github.com/ESMValGroup/ESMValTool/tree/main/esmvaltool/utils/xml2yml>`_
converter can turn the old xml namelists into new-style yml
recipes. It is implemented as a xslt stylesheet that needs a processor
that is xslt 2.0 capable. With this, you simply process your old
namelist with the stylesheet xml2yml.xsl to produce a new yml recipe.

After the conversion you need to manually check the mip information in
the variables! Also, check the caveats below!

Howto
-----

One freely available processor is the Java based
`saxon <http://saxon.sourceforge.net/>`__. You can download the free he
edition
`here <https://sourceforge.net/projects/saxon/files/latest/download?source=files>`__.
Unpack the zip file into a new directory. Then, provided you have Java
installed, you can convert your namelist simply with:

::

   java -jar $SAXONDIR/saxon9he.jar -xsl:xml2yml.xsl -s:namelist.xml -o:recipe.yml

Caveats/Known Limitations
-------------------------

-  At the moment, not all model schemes (OBS, CMIP5, CMIP5_ETHZ…) are
   supported. They are, however, relatively easy to add, so if you need
   help adding a new one, please let me know!
-  The documentation section (namelist_summary in the old file) is not
   automatically converted.
-  In version 1, one could name an exclude, similar to the reference
   model. This is no longer possible and the way to do it is to include
   the models with another ``additional_models`` tag in the variable
   section. That conversion is not performed by this tool.

Authored by **Klaus Zimmermann**, direct questions and comments to
klaus.zimmermann@smhi.se

.. _GitHub access token: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
.. _pygithub: https://pygithub.readthedocs.io/en/latest/introduction.html


Recipe filler
=============

If you need to fill in a blank recipe with additional datasets, you can do that with
the command `recipe_filler`. This runs a tool to obtain a set of additional datasets when
given a blank recipe, and you can give an arbitrary number of data parameters. The blank recipe
should contain, to the very least, a list of diagnostics, each with their variable(s).
Example of running the tool:

.. code-block:: bash

    recipe_filler recipe.yml

where `recipe.yml` is the recipe that needs to be filled with additional datasets; a minimal
example of this recipe could be:

.. code-block:: yaml

    diagnostics:
      diagnostic:
        variables:
          ta:
            mip: Amon  # required
            start_year: 1850  # required
            end_year: 1900  # required


Key features
------------

- you can add as many variable parameters as are needed; if not added, the
  tool will use the ``"*"`` wildcard and find all available combinations;
- you can restrict the number of datasets to be looked for with the ``dataset:``
  key for each variable, pass a list of datasets as value, e.g.
  ``dataset: [MPI-ESM1-2-LR, MPI-ESM-LR]``;
- you can specify a pair of experiments, e.g. ``exp: [historical, rcp85]``
  for each variable; this will look for each available dataset per experiment
  and assemble an aggregated data stretch from each experiment to complete
  for the total data length specified by ``start_year`` and ``end_year``; equivalent to
  ESMValTool's syntax on multiple experiments; this option needs an ensemble
  to be declared explicitly; it will return no entry if there are gaps in data;
- ``start_year`` and ``end_year`` are required and are used to filter out the
  datasets that don't have data in the interval; as noted above, the tool will not
  return datasets with partial coverage from ``start_year`` to ``end_year``;
  if you want all possible years hence no filtering on years just use ``"*"``
  for start and end years;
- ``config-user: rootpath: CMIPX`` may be a list, rootpath lists are supported;
- all major DRS paths (including ``default``, ``BADC``, ``ETHZ`` etc) are supported;
- speedup is achieved through CMIP mip tables lookup, so ``mip`` is required in recipe;

Caveats
-------

- the tool doesn't yet work with derived variables; it will not return any available datasets;
- operation restricted to CMIP data only, OBS lookup is not available yet.


Extracting a list of input files from the provenance
====================================================

There is a small tool available to extract just the list of input files used to generate
a figure from the ``*_provenance.xml`` files (see :ref:`recording-provenance` for more
information).

To use it, install ESMValTool from source and run

.. code-block:: bash

    python esmvaltool/utils/prov2files.py /path/to/result_provenance.xml

The tool is based on the `prov <https://prov.readthedocs.io/en/latest/readme.html>`_
library, a useful library for working with provenance files.
With minor adaptations, this script could also print out global attributes
of the input NetCDF files, e.g. the tracking_id.
