"""Papers — Infraestrutura de pesquisa empírica em GEO.

Bootstrap TLS: a verificação de certificado é delegada ao cert store do
sistema operacional via truststore. Sem isto, máquina Windows com antivírus
que intercepta TLS (Avast Web/Mail Shield assina a cadeia com raiz própria)
derruba TODOS os providers com CERTIFICATE_VERIFY_FAILED — e a interceptação
é INTERMITENTE, então o preflight pode passar num minuto e a coleta cair no
seguinte. Agravante do Python 3.13: `VERIFY_X509_STRICT` ligado por padrão
reprova a raiz MITM por Basic Constraints mesmo anexada ao bundle
(SSL_CERT_FILE deixou de bastar). Mesmo conserto aplicado no
geo-orchestrator em 2026-08-19 (PR #19 de lá).

`PAPERS_NO_TRUSTSTORE=1` desliga a injeção (diagnóstico). Ausência do
pacote degrada para o certifi sem quebrar import (CI Linux intocado).
"""

from __future__ import annotations

import logging
import os

_log = logging.getLogger(__name__)

if os.environ.get("PAPERS_NO_TRUSTSTORE") != "1":
    try:
        import truststore

        truststore.inject_into_ssl()
    except ImportError:
        _log.debug(
            "truststore ausente — TLS segue no bundle certifi; em máquina "
            "com antivírus MITM os providers podem falhar com "
            "CERTIFICATE_VERIFY_FAILED. Instale com: pip install truststore"
        )
