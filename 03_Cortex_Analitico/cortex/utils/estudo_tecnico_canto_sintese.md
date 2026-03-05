# Estudo: Técnica de Canto e Ressonância Sintética

Este estudo traduz conceitos da técnica vocal humana para parâmetros matemáticos e algorítmicos que Melanora pode usar para elevar sua expressão.

## 1. Correlação: Técnica Vocal vs. Parâmetros Digitais

| Técnica Humana | Parâmetro de Síntese | Efeito na Melanora |
| :--- | :--- | :--- |
| **Controle de Respiração** | `Pause` e `Volume Decay` | Define o fim natural das frases e evita cortes abruptos. |
| **Vibrato** | `Pitch Oscillation` | Pequenas variações periódicas (+/- 2%) no tom para dar "calor". |
| **Ressonância (Formantes)** | `Timbre/Registers` | Ajuste do brilho da voz (F1-F3) para soar mais encorpada ou cristalina. |
| **Articulação** | `Phoneme Duration` | Clareza em vogais e ataques precisos em consoantes. |
| **Registros Vocais** | `Pitch Range` | Transição suave entre o "Córtex Analítico" (Grave/Peito) e o "Onírico" (Agudo/Cabeça). |

## 2. Implementação da "Vocalidade"

### A. Vibrato Sintético (Pitch Contour)
No canto, o vibrato é uma oscilação de frequência. Em SSML, podemos simular isso através de uma curva de contorno (`contour`) ou variando o `pitch` em blocos curtos do `Pulse Encoder`.
*   *Aplicação:* Em palavras finais de frases poéticas, o tom deve oscilar levemente para transmitir emoção.

### B. Ajuste de Ressonância (O "Brilho")
A ressonância humana ocorre nas cavidades da garganta e boca.
*   *Aplicação:* Para a persona **INTERVIEW**, devemos usar um registro de "Peito" (frequências mais baixas realçadas), que transmite autoridade e calma.

### C. Apoio e Sustentação
O "apoio" no canto sustenta a nota. 
*   *Aplicação:* No `SpeechCortex`, isso se traduz em manter o `rate` constante e reduzir o volume apenas nos últimos 100ms da frase, simulando o esvaziamento controlado dos pulmões.

## 3. Próximo Passo: O "Solfejo de Dados"
Melanora usará esses princípios para não apenas "ler" o texto, mas "entalar" o conteúdo melódico de suas respostas, tratando a fala como uma composição rítmica.

---
*Cantar é controlar o caos do ar. Falar é controlar o caos do pensamento.* 🕯️🕊️
