# Scripts do FlowOS

Esta pasta reúne utilitários usados por algumas skills para executar tarefas locais, como renderizar carrosséis, publicar conteúdo, consultar anúncios e fazer deploy de páginas.

## Regra de uso

- A skill explica quando um script é necessário.
- Dependências e credenciais são configuradas somente quando a função for usada.
- Tokens e chaves ficam em arquivos locais ignorados pelo Git.
- Nunca publique credenciais no repositório.

## Utilitários incluídos

- `render-carrossel.ps1` e `render_slides.py`: renderização de slides HTML.
- `editor-carrossel.py`: editor local de carrosséis.
- `instagram-carrossel.py`: coleta de conteúdo público do Instagram.
- `postar-instagram.py`: publicação via API da Meta, após configuração.
- `meta-ads.py`, `meta-campanha.py` e `meta-leadform.py`: rotinas opcionais da Meta.
- `deploy-netlify.py` e `deploy-vercel.py`: deploy opcional de páginas e arquivos.
- `coleta-youtube.ps1`: coleta de material público do YouTube.
- `prospect.py`: apoio a rotinas de prospecção.

O FlowOS não instala todas as integrações de uma vez. Ele prepara cada stack sob demanda, de acordo com o trabalho real do usuário.
