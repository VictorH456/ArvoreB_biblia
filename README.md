# 📖🌳 Btree Bible Processor

Uma implementação de alta performance de Árvore B em Python para processar e analisar o texto completo da Bíblia em inglês. O sistema permite a inserção, busca e remoção de palavras, além de contabilizar a frequência de ocorrência de cada termo. Ideal para fins acadêmicos e experimentação com estruturas de dados.

## 👨‍💻 Autor
- **Nome**: Victor Hugo Souza Costa  
- **Disciplina**: Análise de Algoritmos – UFRR

---

## 📌 Visão Geral

Este projeto utiliza uma Árvore B de grau configurável (padrão: 100) para armazenar e gerenciar palavras da Bíblia. É otimizado para grandes volumes de dados, como os cerca de 800.000 tokens do texto bíblico.

---

## 🚀 Funcionalidades

- ✅ Inserção de palavras com contagem de ocorrências
- 🔍 Busca eficiente por palavra
- 🗑️ Remoção de palavras com decremento ou exclusão total
- 📊 Estatísticas de desempenho em tempo real
- 📂 Leitura de arquivo `.txt` com o texto da Bíblia
- 🧠 Interface por linha de comando para testes manuais

---

## 📂 Estrutura
- btree_bible.py: Código principal com toda a lógica
- Biblia.txt: Arquivo da Bíblia em inglês (coloque na mesma pasta)
- README.md: Documentação do projeto

---

## 🧪 Como Executar

1. Certifique-se de ter Python 3 instalado.
2. Coloque o arquivo `Biblia.txt` na mesma pasta do script.
3. Execute no terminal:

```bash
python3 btree_bible.py
