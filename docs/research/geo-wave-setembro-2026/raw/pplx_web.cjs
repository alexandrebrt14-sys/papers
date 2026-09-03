// Perplexity WEB (assinatura Pro, navegador logado via CDP 9222) como substituto da API sem crédito.
// Uso: node pplx_web.cjs <nome> "<pergunta>"  -> grava raw/<nome>.md
const PWC_PATH = 'C:/Users/Caramaschi.CARAMASCHI-PC/AppData/Roaming/npm/node_modules/@playwright/mcp/node_modules/playwright-core';
const { chromium } = require(PWC_PATH);
const fs = require('fs');
const path = require('path');
const [, , name, question] = process.argv;

(async () => {
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9222', { timeout: 15000 });
  const ctx = browser.contexts()[0] || (await browser.newContext());
  const page = await ctx.newPage();
  page.setDefaultTimeout(60000);
  let code = 0;
  try {
    const url = 'https://www.perplexity.ai/search/new?q=' + encodeURIComponent(question);
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    let last = '', stable = 0, text = '';
    for (let i = 0; i < 60; i++) {           // até ~5 min
      await page.waitForTimeout(5000);
      text = await page.evaluate(() => document.body ? document.body.innerText : '');
      if (text.length > 1500 && text === last) { stable++; } else { stable = 0; }
      last = text;
      if (stable >= 3) break;                  // 15 s sem mudança = resposta concluída
    }
    const links = await page.evaluate(() => Array.from(document.querySelectorAll('a[href^="http"]'))
      .map(a => a.href).filter(h => !h.includes('perplexity.ai')).filter((v, i, a) => a.indexOf(v) === i).slice(0, 80));
    const out = `# ${name} (Perplexity WEB Pro, ${page.url()})\n\n${text}\n\n## Links na página\n` + links.map(l => '- ' + l).join('\n');
    fs.writeFileSync(path.join(__dirname, 'raw', name + '.md'), out, 'utf8');
    console.log(`[OK] ${name}: ${text.length} chars, ${links.length} links, ${page.url()}`);
  } catch (e) {
    console.error(`[FAIL] ${name}: ${e && e.message ? e.message : e}`);
    code = 1;
  } finally {
    try { await page.close(); } catch {}
    try { await browser.close(); } catch {}
  }
  process.exit(code);
})();
