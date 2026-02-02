# 🧪 Simulador Modular de Reatores e Processos Químicos

Projeto de Engenharia Química que simula e compara diferentes tipos de reatores, permite ajuste com dados experimentais, cálculos de conversão e concentrações finais, com visualização gráfica e interface amigável via Streamlit.

## 🚀 Principais Funcionalidades

- **Simulação cinética** de múltiplos tipos de reatores:
    - Batch
    - CSTR
    - PFR
    - Série
    - Paralelo
    - Reversível
- **Visualização dos perfis de concentração** das espécies envolvidas ao longo do tempo.
- **Exibição automática dos valores finais** (CA, CB, CC e conversão) após o tempo/residência escolhido.
- **Ajuste automático de cinética** a partir de dados experimentais (upload de CSV).
- Estrutura **modular** pronta para adicionar trocador de calor, destilação, otimização, entre outros.

## 📸 Print do Projeto
<img width="1913" height="795" alt="image" src="https://github.com/user-attachments/assets/34a1ecf8-814b-4142-9abe-1edd20187d83" />

## 🏗️ Como Rodar

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seuusuario/seurepositorio.git
   cd seurepositorio
   ```
2. **Instale as dependências:**
   ```bash
   pip install streamlit numpy pandas matplotlib scipy scikit-learn
   ```
3. **Execute o app:**
   ```bash
   streamlit run simulador_cinetica_reatores.py
   ```
4. Abra [http://localhost:8501](http://localhost:8501) no navegador.

## 📂 Estrutura do Projeto

- `simulador_cinetica_reatores.py` — código principal do app em Python/Streamlit
- [Imagens, exemplos de CSV e resultados podem ser adicionados aqui]

## 🧩 Funcionalidades extras (roadmap)

- [ ] Otimização multiobjetivo (max conversão, lucro, sustentabilidade etc.)
- [ ] Módulos completos para trocador de calor e destilação
- [ ] Exportação automática de relatórios (CSV/PDF)
- [ ] Dashboard comparativo múltiplos cenários

## ⚡ Exemplo prático (reação paralela)

Simulação para A→B (k₁=0.4 h⁻¹), A→C (k₂=0.2 h⁻¹), CA₀=2.0 mol/L, tempo=10h:

| Especie | Concentração Final (mol/L) |
|---------|---------------------------|
| CA      | 0.036                     |
| CB      | 1.333                     |
| CC      | 0.667                     |
| Conversão de A | 98.2%              |

## 📑 Licença

[MIT](LICENSE)

## 🙋‍♂️ Contato

Dúvidas, sugestões ou parcerias: abra uma issue ou me procure no [LinkedIn](https://www.linkedin.com/in/seuperfil).

---

**Desenvolvido por [Seu Nome] • Engenharia Química & Ciência de Dados**
