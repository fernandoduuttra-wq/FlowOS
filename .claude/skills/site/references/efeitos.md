# Biblioteca de efeitos — o que faz um site parecer premium

> Vocabulário de técnicas nomeadas. Serve pra DIRIGIR: em vez de "deixa mais bonito", diz-se "põe um
> Lenis + reveal on scroll". Cada efeito tem: o que é, a lib, e quando (não) usar.
>
> Regra de ouro que atravessa tudo: **profundidade sóbria > firula.** Movimento sutil que serve à
> leitura, não animação que grita. Um site premium usa 3-4 destes bem, não os 15.

---

## Os fundamentais (90% do "parece caro" vem daqui)

### 1. Smooth scroll (scroll manteiga)
- **O que é:** o scroll desliza com inércia em vez de pular linha a linha. É o efeito nº1 que o olho
  lê como "caro", e quase ninguém leigo sabe que tem nome.
- **Lib:** Lenis (`@studio-freight/lenis`). Leve, livre.
- **Cuidado:** respeitar `prefers-reduced-motion`. Não aplicar em conteúdo que precisa de scroll nativo
  (mapas, áreas com scroll interno → `data-lenis-prevent`).

### 2. Reveal on scroll (entrada ao rolar)
- **O que é:** elementos aparecem (fade + sobem alguns px) conforme entram na viewport. Dá ritmo de
  descida, sensação de "o site vai se revelando".
- **Lib:** Framer Motion (`whileInView`) ou IntersectionObserver puro.
- **Cuidado:** stagger sutil (30-80ms entre itens). Exagerou, vira apresentação de PowerPoint.

### 3. Spring / física de mola
- **O que é:** transições com física (stiffness/damping) em vez de easing linear. O olho lê como
  "vivo" e natural, não mecânico.
- **Lib:** Framer Motion (`transition={{ type: 'spring', stiffness, damping }}`).
- **Cuidado:** para texto/leitura, spring suave. Bounce forte é cara de app de criança.

### 4. Hierarquia de easing
- **O que é:** curvas de aceleração certas. `ease-out` pra entradas (rápido→lento, sensação de chegar
  suave), `ease-in-out` pra loops. Nunca `linear` (robótico).
- **Lib:** CSS `cubic-bezier()` ou Framer Motion.
- **Referência de curva boa:** `cubic-bezier(0.16, 1, 0.3, 1)` (o "ease-out expo", padrão premium).

---

## Profundidade (o que separa "chapado" de "com camadas")

### 5. Parallax
- **O que é:** camadas movem em velocidades diferentes no scroll → sensação de profundidade 3D sem 3D.
- **Lib:** Framer Motion (`useScroll` + `useTransform`) ou GSAP ScrollTrigger.
- **Cuidado:** sutil (10-30% de diferença). Muito parallax embrulha o estômago.

### 6. Sombra em duas camadas
- **O que é:** em vez de uma `box-shadow` dura, duas sobrepostas (uma curta e densa + uma longa e
  difusa). É o truque que faz cards parecerem flutuar de verdade.
- **Lib:** CSS puro. Ex: `0 1px 2px rgba(0,0,0,.1), 0 8px 30px rgba(0,0,0,.12)`.
- **Nota:** no território dark do design.json, a profundidade vem MAIS de gradiente/luz que de sombra
  preta. Conferir a regra `forma.sombra` do design.json (hoje: "none", profundidade vem da foto).

### 7. Glassmorphism (vidro)
- **O que é:** painel translúcido com blur do que está atrás (`backdrop-filter: blur`). Header
  flutuante, cards sobre imagem.
- **Cuidado:** custa performance; usar com parcimônia. Fácil de datar (virou clichê 2021).

### 8. Mesh gradient / gradiente orgânico
- **O que é:** gradiente de múltiplos pontos de cor, suave, orgânico (não a faixa linear batida).
- **Lib:** CSS `radial-gradient` empilhados, ou ferramentas (mesh gradient generators).
- **Cuidado:** o `nunca` do design.json proíbe gradiente roxo/hype. Aqui, no dark, um mesh de pretos
  quentes + um respiro de vermelho pode dar profundidade sem cair no hype.

### 9. Noise / grain
- **O que é:** textura sutil de ruído por cima → tira o "digital liso demais", dá tato de impresso/film.
- **Lib:** SVG `feTurbulence` ou PNG de noise com `mix-blend-mode` e opacidade baixa (~3-5%).
- **Ótimo pro território editorial/cinema** — casa com a marca.

---

## Scroll-driven avançado (quando o site é uma experiência)

### 10. Pin + scroll timeline
- **O que é:** uma seção "trava" na tela e a animação avança conforme rola (texto que troca, imagem
  que transforma). O efeito "storytelling" dos sites premiados.
- **Lib:** GSAP + ScrollTrigger (o padrão-ouro pra isso).
- **Cuidado:** é o mais caro de fazer e de manter. Usar só quando a mensagem justifica.

### 11. Horizontal scroll section
- **O que é:** uma faixa que rola na horizontal enquanto a página desce.
- **Lib:** GSAP ScrollTrigger.
- **Cuidado:** confunde no mobile. Ter fallback.

### 12. Text reveal por palavra/linha
- **O que é:** o título se monta palavra por palavra ou por máscara (linha sobe de trás de um recorte).
- **Lib:** GSAP SplitText, ou Framer Motion com stagger.
- **Casa muito com Didone grande** (o território da marca) — o título editorial se montando é elegante.

---

## 3D (o teto, usar só com propósito)

### 13. Embed 3D no-code
- **Lib:** Spline (spline.design) — modela numa ferramenta visual e embeda. Sem código.
- **Quando:** um objeto 3D de hero, um símbolo girando. Rápido.

### 14. 3D em código
- **Lib:** React Three Fiber (Three.js pra React).
- **Quando:** controle total, cena complexa. Caro. Só se o projeto pede mesmo.

### 15. Micro-animação (Lottie)
- **O que é:** animação vetorial leve (ícone que se desenha, loader, ilustração que se move).
- **Lib:** Lottie (arquivos do After Effects / LottieFiles).

---

## Como escolher (mapa rápido)

- **Site sóbrio / Lo-fi:** smooth scroll (1) + reveal sutil (2) + easing certo (4) + noise (9). Só.
- **Landing premium:** o de cima + spring (3) + parallax leve (5) + text reveal (12).
- **Experiência / storytelling:** + pin timeline (10). Aí sim GSAP.
- **Vitrine/produto que pede 3D:** + Spline (13).

**Nunca** empilhar tudo. O refinamento está na contenção: 3-4 efeitos bem feitos > 15 brigando.
Conferir sempre contra a lista `nunca` do `design.json`.
