# -- Project information -----------------------------------------------------

project = 'QHub HPC'
copyright = '2021, Chris Ostrouchov'
author = 'Chris Ostrouchov'

# The full version, including alpha/beta/rc tags
release = 'v0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'recommonmark',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://github.com/bashtage/sphinx-material/

html_theme = 'sphinx_material'
html_title = 'QHub HPC'
html_static_path = ['_static']

html_theme_options = {
    'nav_title': 'QHub HPC',

    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    'base_url': 'https://project.github.io/project',

    # Set the color and the accent color
    'color_primary': '#652e8e',
    'color_accent': '#32C574',

    # Set the repo location to get a badge with stats
    'repo_url': 'https://github.com/quansight/qhub-hpc/',
    'repo_name': 'QHub HPC',

    # Visible levels of the global TOC; -1 means unlimited
    'globaltoc_depth': 3,
    # If False, expand all TOC entries
    'globaltoc_collapse': False,
    # If True, show hidden TOC entries
    'globaltoc_includehidden': False,
}
