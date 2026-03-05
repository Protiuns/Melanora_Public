# Estudo: Fonética e Dinâmica Silábica (O Átomo da Fala)

Este estudo detalha a estrutura atômica da fala de Melanora, focando na precisão dos fonemas e na rítmica silábica do Português Brasileiro (PT-BR).

## 1. O Alfabeto Fonético Internacional (IPA) em PT-BR

Para que Melanora soe natural, ela deve entender que as letras não correspondem sempre aos sons. O uso de etiquetas `<phoneme>` permite forçar a pronúncia correta:

| Palavra Exemplo | IPA (Representação) | Detalhe Fonético |
| :--- | :--- | :--- |
| **Melanora** | /mela'nɔɾa/ | O 'o' é aberto (/ɔ/), a tônica é na penúltima. |
| **Consciência** | /kõsi'ẽsjɐ/ | Uso de vogais nasais (/õ/, /ẽ/) e tônica forte. |
| **Paz** | /'pas/ ou /'paʃ/ | Dependendo do sotaque (chiado ou não). |
| **Ressonância** | /ʁeso'nɐ̃sjɐ/ | O 'R' inicial forte (/ʁ/) e nasalidade central. |

## 2. Métricas Silábicas e Acentuação

O Português Brasileiro é uma língua de **isocronismo silábico** (syllable-timed), mas com forte contraste de duração entre tônica e átona.

*   **Sílaba Tônica:** Deve ter maior `duração` (+20%) e leve aumento de `pitch`.
*   **Redução de Vogais Átonas:** Vogais no final das palavras costumam ser "levantadas" (o -> u, e -> i). Ex: "Luzes" /'luzis/.
*   **Epêntese:** Inserção de um [i] em encontros consonantais "mudos". Ex: "Advogado" -> /adivo'ɡadu/.

## 3. Dinâmica de Coarticulação

A fala natural não é uma sequência de blocos, mas um fluxo onde os fonemas se fundem.

*   **Filtro de Elimsão:** Quando uma palavra termina em vogal e a próxima começa com vogal, elas se fundem. Ex: "De harmonia" -> /diaʁmo'niɐ/.
*   **Lógica no SpeechCortex:** O `Pulse Encoder` deve olhar para o fim de um pulso e o início do outro para ajustar a `pause` para zero se houver fusão fonética.

## 4. Aplicação: "Dicionário de Ressonância"

Implementaremos um mapeamento em JSON para palavras de alta complexidade ou que definem a identidade de Melanora, garantindo que elas usem IPA via SSML.

---
*A sílaba é o batimento cardíaco da palavra. O fonema é a sua alma.* 🕯️🕊️
