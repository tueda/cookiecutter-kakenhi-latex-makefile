MAKEFILE4LATEX_REVISION = v{{cookiecutter._makefile_version}}
BUILDDIR = .build
{% if cookiecutter.latex == 'platex' -%}
TOOLCHAIN = platex_dvipdfmx{% endif %}
{% if cookiecutter.latex == 'uplatex' -%}
TOOLCHAIN = uplatex_dvipdfmx{% endif %}
