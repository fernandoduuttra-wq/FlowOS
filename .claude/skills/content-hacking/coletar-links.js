// ============================================================
// COLETAR LINKS — Content Hacking
// ============================================================
// Como usar:
// 1. Abra no Chrome (desktop, logado):
//    https://www.instagram.com/explore/search/keyword/?q=SUA_PALAVRA_CHAVE
// 2. Role a página pra baixo até carregar bastante post (quanto mais rolar, mais links).
// 3. Aperte F12 → aba "Console" → cole este script inteiro → Enter.
// 4. Ele copia a lista pro clipboard E imprime no console, já separada.
// 5. Cole a lista de volta no Claude na skill /content-hacking.
// ============================================================

(() => {
  const anchors = Array.from(document.querySelectorAll('a[href*="/reel/"], a[href*="/p/"]'));
  const reels = new Set();
  const carrosseis = new Set();

  for (const a of anchors) {
    const url = a.href.split('?')[0].replace(/\/$/, '') + '/';
    if (url.includes('/reel/')) reels.add(url);
    else if (url.includes('/p/')) carrosseis.add(url);
  }

  const reelsArr = [...reels];
  const carrosseisArr = [...carrosseis];

  const out =
    `# REELS (vídeos) — ${reelsArr.length}\n` +
    reelsArr.join('\n') +
    `\n\n# CARROSSÉIS / FOTOS — ${carrosseisArr.length}\n` +
    carrosseisArr.join('\n');

  console.log(out);
  console.log(`\n✅ ${reelsArr.length} reels + ${carrosseisArr.length} carrosséis copiados pro clipboard.`);

  // copia pro clipboard
  const ta = document.createElement('textarea');
  ta.value = out;
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); } catch (e) {}
  document.body.removeChild(ta);

  return out;
})();
