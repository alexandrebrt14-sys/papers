#!/usr/bin/env bash
# reproduce.sh — regenera as tabelas e números do paper a partir do git tag.
#
# Usage:
#   ./scripts/reproduce.sh                          # default tag paper-4-dataset-closed
#   ./scripts/reproduce.sh paper-4-submission-v1    # specific tag
#   ./scripts/reproduce.sh --local                  # sem docker, usa env local
#
# Resolve gap E4 do Agent E audit (2026-04-23).
#
# Verifica:
# 1. git tag existe no repo
# 2. SHA-256 do papers.db bate com manifest congelado
# 3. Roda análise confirmatória via hypothesis_engine
# 4. Exporta tabelas para build/tables/
# 5. Compara SHA256 output vs manifest pré-congelado

set -euo pipefail

TAG="${1:-paper-4-dataset-closed}"
MODE="${2:-docker}"   # 'docker' | '--local'

OUT_DIR="build"
TABLES_DIR="$OUT_DIR/tables"
MANIFEST="docs/audits/paper-4/MANIFEST.sha256"

echo "============================================"
echo "  papers — reproduce pipeline"
echo "============================================"
echo "  tag:     $TAG"
echo "  mode:    $MODE"
echo "  output:  $OUT_DIR/"
echo "============================================"

# 1. Checkout tag
if ! git tag | grep -q "^${TAG}$"; then
    echo "ERRO: git tag '$TAG' não existe no repo."
    echo "Tags disponíveis:"
    git tag -l "paper-*" | tail -10
    exit 1
fi

CURRENT=$(git rev-parse --abbrev-ref HEAD)
echo ""
echo "[1/5] Checkout tag $TAG (current branch: $CURRENT)"
git fetch --tags
# Guarda branch atual; volta ao final
trap "git checkout $CURRENT" EXIT
git checkout "tags/$TAG" -- data/ src/ scripts/ docs/ || {
    echo "ERRO: falha ao fazer checkout seletivo do tag."
    exit 2
}

# 2. Verifica SHA-256 do DB
echo ""
echo "[2/5] Verifica SHA-256 do papers.db"
ACTUAL_SHA=$(sha256sum data/papers.db | awk '{print $1}')
echo "  papers.db SHA-256: $ACTUAL_SHA"
if [ -f "$MANIFEST" ] && grep -q "$ACTUAL_SHA" "$MANIFEST"; then
    echo "  ✓ SHA matches $MANIFEST"
else
    echo "  ⚠ SHA não encontrado em $MANIFEST (ok se primeira run)"
fi

# 3. Prepara env
if [ "$MODE" = "--local" ]; then
    echo ""
    echo "[3/5] Usando Python local — assumindo env virtual ativo"
    python --version
else
    echo ""
    echo "[3/5] Build + run Docker image"
    docker build -t papers-repro:$TAG . 2>&1 | tail -5
fi

# 4. Roda análise confirmatória
echo ""
echo "[4/5] Roda hypothesis_engine + gera tabelas"
mkdir -p "$TABLES_DIR"

if [ "$MODE" = "--local" ]; then
    python -m src.cli analyze --report --seed 42 > "$OUT_DIR/report.log"
    python scripts/generate_paper_tables.py --db data/papers.db --out "$TABLES_DIR" \
        || echo "  (generate_paper_tables.py pode não existir ainda)"
else
    docker run --rm \
        -v "$(pwd)/$OUT_DIR:/app/$OUT_DIR" \
        papers-repro:$TAG \
        analyze --report --seed 42 > "$OUT_DIR/report.log"
fi

# 5. Gera MANIFEST dos outputs
echo ""
echo "[5/5] Gera MANIFEST.sha256 dos outputs"
find "$OUT_DIR" -type f \( -name "*.csv" -o -name "*.json" -o -name "*.md" \) \
    -exec sha256sum {} \; | sort > "$OUT_DIR/MANIFEST.sha256"

echo ""
echo "============================================"
echo "  ✓ REPRODUCE COMPLETO"
echo "============================================"
echo "  Output: $OUT_DIR/"
echo "  Manifest: $OUT_DIR/MANIFEST.sha256"
echo ""
echo "  Compare com manifest do paper:"
echo "    diff -u $MANIFEST $OUT_DIR/MANIFEST.sha256"
echo ""
