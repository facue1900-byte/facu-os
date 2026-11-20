#!/bin/bash
# La herramienta de la carpeta de Grok: el mismo paper.py que la de 10.000 de Claude, pero con
# su propio libro en data/paper-grok. Es lo único que Grok puede correr en su ciclo.
export PAPER_DIR=/Users/Facu/facu-os/data/paper-grok
exec /Users/Facu/facu-os/.venv/bin/python /Users/Facu/facu-os/execution/paper/paper.py "$@"
