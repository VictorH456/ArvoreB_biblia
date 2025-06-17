import time
from collections import defaultdict
import re

class BTreeNode:
    def __init__(self, degree, leaf=True):
        self.degree = degree
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.word_count = defaultdict(int)

    def split_child(self, i):
        t = self.degree
        y = self.children[i]
        z = BTreeNode(t, y.leaf)

        z.keys = y.keys[t:]
        y.keys = y.keys[:t-1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys.pop())

    def insert_non_full(self, key):
        i = len(self.keys) - 1

        if self.leaf:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            if i >= 0 and self.keys[i] == key:
                self.word_count[key] += 1
                return
            self.keys.insert(i + 1, key)
            self.word_count[key] = 1
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.degree - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1

        if i < len(self.keys) and key == self.keys[i]:
            return self, self.word_count[key]

        if self.leaf:
            return None, 0
        return self.children[i].search(key)

class BTree:
    def __init__(self, degree=100):
        self.root = BTreeNode(degree)
        self.degree = degree
        self.total_insertions = 0
        self.total_time = 0

    def insert(self, key):
        start = time.time()
        root = self.root
        if len(root.keys) == 2 * self.degree - 1:
            s = BTreeNode(self.degree, False)
            s.children.append(self.root)
            s.split_child(0)
            i = 0
            if s.keys[0] < key:
                i += 1
            s.children[i].insert_non_full(key)
            self.root = s
        else:
            root.insert_non_full(key)
        end = time.time()
        self.total_insertions += 1
        self.total_time += (end - start)

    def search(self, key):
        return self.root.search(key)

    def remove(self, key):
        node, count = self.search(key)
        if node and key in node.word_count:
            if node.word_count[key] > 1:
                node.word_count[key] -= 1
            else:
                node.keys.remove(key)
                del node.word_count[key]

    def print_stats(self):
        avg_time = (self.total_time / self.total_insertions * 1000) if self.total_insertions else 0
        print("\n===== MÉTRICAS DA ÁRVORE B =====")
        print(f"Total de inserções: {self.total_insertions}")
        print(f"Tempo total de inserção: {self.total_time:.4f} s")
        print(f"Tempo médio por inserção: {avg_time:.4f} ms")


def load_words_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().lower()
        words = re.findall(r"\b[a-zA-Z]+\b", text)
        return words

def process_bible_file(filepath, degree=100):
    btree = BTree(degree=degree)
    words = load_words_from_file(filepath)
    print(f"Total de palavras encontradas: {len(words)}")
    start_time = time.time()

    for i, word in enumerate(words):
        btree.insert(word)
        if (i + 1) % 50000 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"  Processadas {i + 1} palavras... ({int(rate)} palavras/seg)")

    print("Inserção completa!")
    btree.print_stats()
    return btree

if __name__ == "__main__":
    btree = process_bible_file("Biblia.txt")

    while True:
        cmd = input("\nComando (search <palavra> / remove <palavra> / stats / exit): ").strip().split()

        if not cmd:
            continue

        action = cmd[0].lower()

        if action == "exit":
            break

        elif action == "search" and len(cmd) > 1:
            word = cmd[1].lower()
            node, _ = btree.search(word)
            if node and word in node.word_count:
                print(f"'{word}' encontrado: {node.word_count[word]} ocorrência(s)")
            else:
                print(f"'{word}' não encontrado")

        elif action == "remove" and len(cmd) > 1:
            word = cmd[1].lower()
            node, _ = btree.search(word)
            if node and word in node.word_count:
                print(f"Removendo '{word}' (ocorrências: {node.word_count[word]})...")
                btree.remove(word)
            else:
                print(f"'{word}' não encontrado para remoção")

        elif action == "stats":
            btree.print_stats()

        else:
            print("Comando inválido. Use: search/remove <palavra>, stats ou exit.")
