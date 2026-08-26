# O console da Meta, passo a passo

O trecho mais lento e mais frágil da montagem. Não tem API: é o usuário no
navegador, tela por tela. **Peça print a cada etapa** — as telas são parecidas,
o fluxo muda com frequência e um clique errado só aparece como erro três passos
depois.

Onde está escrito `{APP_URL}`, use o endereço final de produção.

---

## 1. Criar o app

`developers.facebook.com` → **Meus Apps** → **Criar app**.

**Confira o email de contato antes de avançar.** Ele vem preenchido com o email
da conta logada, que pode não ser a do usuário (perfil compartilhado, conta de
outra pessoa no mesmo navegador). O app fica preso ao perfil do Facebook onde
foi criado — corrigir depois é recomeçar. O email de contato em si pode ser
qualquer um; o que importa é o **perfil** ser o certo, e ele precisa ter acesso
à conta do Instagram que vai ser automatizada.

Etapas: Detalhes do app → **Casos de uso** → Empresa → Requisitos → Visão geral.

## 2. Caso de uso — a primeira armadilha

A tela abre em "Em destaque", e **o caso de uso certo não está lá**.

Filtre por **Business Messaging** e escolha:

> **Gerenciar mensagens e conteúdo no Instagram**

Marque só esse. Cada caso de uso extra arrasta permissões que viram requisito na
hora de publicar.

**Nunca escolha "Autenticar e solicitar dados de usuários com o Login do
Facebook".** Parece o caminho óbvio e é o errado: leva ao fluxo que exige página
do Facebook vinculada — exatamente o que esta arquitetura evita.

## 3. Onde tudo mora

No sistema novo, não existe item "Instagram" no menu lateral. Tudo está em:

**Painel → "Personalizar o caso de uso 'Gerenciar mensagens e conteúdo no
Instagram'" → Configuração da API com login do Instagram**

Essa tela tem os itens numerados 1 a 4. É pra onde voltar sempre.

Ignore o card "Torne-se um Provedor de Tecnologia" — serve pra quem acessa dados
de outras empresas. Não é o caso e é burocracia à toa.

## 4. As credenciais — a segunda armadilha

Nessa tela aparecem **ID do app do Instagram** e **Chave secreta do app do
Instagram**.

**Não são as mesmas do app do Facebook**, que ficam em Configurações → Básico e
têm nomes quase idênticos. Trocar as duas é o erro mais comum, e o sintoma é
genérico (falha no login sem explicação).

O ID é público. A chave secreta é segredo: **nunca peça por chat ou print** —
abra o arquivo de ambiente e deixe o usuário colar direto.

No item **1**, clique em "Add all required permissions" (adiciona
`instagram_business_basic`, `manage_comments`, `manage_messages`).

## 5. Webhook (item 3)

- **URL de callback:** `{APP_URL}/api/webhook`
- **Verify token:** o mesmo valor da variável de ambiente
- **Campos assinados:** `comments` e `messages`

A verificação funciona mesmo com o app em desenvolvimento — o aviso de que "o
app deve estar publicado" vale pra **receber eventos**, não pra verificar.

Se falhar aqui, teste antes de mexer na Meta:

```
curl "{APP_URL}/api/webhook?hub.mode=subscribe&hub.verify_token=SEU_TOKEN&hub.challenge=teste"
```

Deve responder `teste`. Se responder 403, o token diverge. Se vier 302 pra
vercel.com, é a Deployment Protection.

## 6. Redirect do OAuth (item 4) — a terceira armadilha

**É o passo mais fácil de pular**, porque o item 2 ("Gerar tokens de acesso")
puxa a atenção pro cadastro de testador e o 4 fica esquecido embaixo.

Item **4. Configurar o login da empresa no Instagram** → **Configurar** →
campo **URL de redirecionamento**:

```
{APP_URL}/api/oauth/callback
```

A Meta compara caractere por caractere: `https`, sem barra final, tudo
minúsculo, sem espaço colado no fim (colar do editor às vezes traz espaço).

Sintoma de estar faltando ou divergente: **`Invalid redirect_uri`**.

## 7. Testador do Instagram — a quarta armadilha

Enquanto o app não está publicado, só contas com função atribuída conseguem
autorizar. São **dois passos**, e o segundo é o que todo mundo esquece.

**No console:** Funções do app → Funções → **Adicionar pessoas** → marque
**"Testador do Instagram"** (última opção, ícone do Instagram — o texto cita uma
API antiga, mas é essa mesmo) → digite o usuário → Adicionar.

**No celular:** o convite precisa ser **aceito**. Enquanto não for, o status fica
`Pendente` e a autorização falha com **"Função de desenvolvedor é insuficiente"**.

O caminho oficial é *Instagram → Configurações → Apps e sites → Convites de
testador*, **mas esse item costuma não aparecer na lista visível**. Também não
está na Central de Contas (é o palpite natural e está errado).

O que funciona: **Configurações e atividade → barra de busca no topo → "Apps e
sites"**. A busca acha telas que a navegação esconde. Vale também conferir as
notificações do Instagram — às vezes o convite chega por lá.

Confirme o status na tabela de Funções antes de tentar conectar. `Pendente` =
não adianta tentar.

## 8. Publicar — a quinta armadilha

**Em modo de desenvolvimento a Meta não entrega webhook nenhum.** O usuário
comenta, não acontece nada, e parece bug do app. Não é: é o app não publicado.

Menu **Publicar**. O botão fica cinza até os requisitos fecharem. Em
**Configurações do app → Básico**:

- **URL da Política de Privacidade:** `{APP_URL}/privacidade`
- **Exclusão de dados do usuário:** `{APP_URL}/exclusao-de-dados`
- **Categoria:** obrigatório e costuma vir vazio — é o que trava sem dizer

Esses dois endereços precisam existir e responder 200 **publicamente**. A
arquitetura já cria as duas páginas; confira que estão no ar antes de publicar.

Pode ignorar: informações do encarregado de proteção de dados (só vale pra quem
opera na União Europeia), ícone do app e termos de serviço.

Se os campos vierem preenchidos com `facebook.com`, são placeholders — troque
pelos endereços reais. Apontar política de privacidade pro site da Meta é
inverdade e pode reprovar.

## 9. Nível de acesso

Publicado, o app roda com **acesso padrão**: funciona pra quem tem função no app
(dono e testadores). Isso basta pra automatizar a conta do próprio usuário.

Rodar pra terceiros — clientes, por exemplo — exige **acesso avançado**, com
análise do app pela Meta: vídeo demonstrando o fluxo, justificativa de cada
permissão e prazo de dias. Diga isso na hora certa; não é bloqueio pro uso
próprio, mas é bloqueio pra revenda.
