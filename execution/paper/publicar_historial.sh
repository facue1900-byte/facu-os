#!/bin/bash
# Publica el historial de la carpeta de 10.000 en la rama claude/cartera-original, para que
# el juez de la nube la vea (data/ está gitignoreado y antes no llegaba a ninguna rama).
# Arma el commit por plumbing: no toca el working tree, el índice ni la rama donde estés
# trabajando, y corre sin molestar aunque haya otra sesión editando este repo.
set -euo pipefail
OS=/Users/Facu/facu-os
ARCHIVO=$OS/data/paper/historial.csv
RAMA=claude/cartera-original
cd "$OS"

# Sin esto, una red colgada deja el proceso esperando y launchd no lanza la corrida siguiente.
export GIT_SSH_COMMAND='ssh -o ConnectTimeout=20 -o ServerAliveInterval=15 -o ServerAliveCountMax=2 -o BatchMode=yes'

[[ -s $ARCHIVO ]] || { echo "No existe o está vacío: $ARCHIVO" >&2; exit 2; }

BLOB=$(git hash-object -w "$ARCHIVO")
ARBOL=$(printf '100644 blob %s\thistorial.csv\n' "$BLOB" | git mktree)

# ls-remote da 2 si la rama no existe y otro código si falló la red: no son lo mismo.
RC=0
git ls-remote --exit-code --heads origin "$RAMA" > /dev/null || RC=$?
[[ $RC -eq 0 || $RC -eq 2 ]] || { echo "No se pudo consultar origin (código $RC)" >&2; exit "$RC"; }

PADRE=()
if [[ $RC -eq 0 ]]; then
  git fetch -q origin "+refs/heads/$RAMA:refs/remotes/origin/$RAMA"
  ANTERIOR=$(git rev-parse "refs/remotes/origin/$RAMA")
  # Sin cambios no se commitea: si no, cada corrida fallida ensuciaría la rama.
  [[ $(git rev-parse "$ANTERIOR^{tree}") == "$ARBOL" ]] && exit 0
  PADRE=(-p "$ANTERIOR")
fi

COMMIT=$(git commit-tree "$ARBOL" "${PADRE[@]+"${PADRE[@]}"}" -m "paper: historial $(date -u '+%Y-%m-%d %H:%M') UTC")
git push -q origin "$COMMIT:refs/heads/$RAMA"
git update-ref "refs/remotes/origin/$RAMA" "$COMMIT"
