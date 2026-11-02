# Modul 04 - Implementasi Pencarian Uninformed

# Persiapan Library
from collections import deque        # Untuk implementasi antrian (Queue) pada BFS
from IPython.display import clear_output  # Untuk membersihkan output sel (animasi teks)
import time                          # Untuk memberikan jeda waktu antar langkah (animasi)
import json, os, sys, tempfile, subprocess, importlib.util  # Untuk menjalankan viewer Flet
import io, contextlib                # Untuk menyembunyikan print saat evaluasi
import numpy as np
import matplotlib.pyplot as plt      # Untuk visualisasi perbandingan

from visualisasi import buka_flet

VISUALIZE = True    # True = buka jendela Flet saat agen dijalankan, False = hanya teks
ANIM_DELAY = 0.8    # Jeda (detik) animasi pergerakan agen di notebook


#Definisikan lingkungan pohon 
# Key   = node (induk)
# Value = daftar anak (suksesor) dari node tersebut, urut dari kiri ke kanan
# Node yang tidak menjadi key adalah daun (leaf)

pohon_1 = {
    "A": ["B", "C", "D"],
    "B": ["E", "F", "G"],
    "C": ["H", "I"],
    "D": ["J", "K", "L"],
    "E": ["M", "N"],
    "F": ["O"],
    "G": ["P", "Q"],
    "H": ["R", "S"],
    "I": ["T"],
    "J": ["U"],
    "K": ["V", "W"],
    "L": ["X"],
    "M": ["Y"],
    "W": ["Z"],
}

start_node = "A" # Titik awal pencarian
goals_node = "Z" # Titik tujuan Pencarian

environment = pohon_1 # Pilih lingkungan pohon


# Menampilkan tree dalam bentuk teks
# Menampilkan struktur pohon dalam bentuk teks dan ringkasannya

def print_tree(tree, node, prefix="", is_last=True, is_root=True):
    """Mencetak pohon secara rekursif dengan indentasi."""
    if is_root:
        print(node)
    else:
        print(prefix + ("└── " if is_last else "├── ") + node)
    children = tree.get(node, [])
    for idx, child in enumerate(children):
        new_prefix = prefix if is_root else prefix + ("    " if is_last else "│   ")
        print_tree(tree, child, new_prefix, idx == len(children) - 1, False)

def tree_summary(tree, root):
    """Menghitung jumlah node, kedalaman maksimum, dan percabangan maksimum."""
    total, max_depth, max_branch = 0, 0, 0
    stack = [(root, 0)]
    while stack:
        node, depth = stack.pop()
        total += 1
        max_depth = max(max_depth, depth)
        max_branch = max(max_branch, len(tree.get(node, [])))
        stack.extend((c, depth + 1) for c in tree.get(node, []))
    return total, max_depth, max_branch


# ============================================================
# KELAS DASAR AGEN (sama seperti PathFindingAgent)
# ============================================================
class TreeSearchAgent:
    """Kelas dasar untuk agen yang mencari jalur terlebih dahulu pada pohon."""

    def __init__(self, env, start, goal):
        self.env = env                      # Menyimpan referensi lingkungan (pohon)
        self.start = start                  # Node awal
        self.goal = goal                    # Node tujuan
        self.node = start                   # Posisi agen saat ini
        self.path = []                      # Jalur yang ditemukan akan disimpan di sini
        self.steps = 0                      # Menghitung langkah aktual agen
        self.explored_path = [start]        # Menyimpan langkah aktual agen
        self.found_path = False             # Status apakah jalur ditemukan
        self.nodes_expanded = 0             # Jumlah node yang diperiksa saat pencarian
        self.max_frontier = 0               # Ukuran open list terbesar saat pencarian

    def get_children(self, node):
        """Mendapatkan anak (suksesor) dari sebuah node, urut dari kiri ke kanan."""
        return list(self.env.get(node, []))

    def display(self, delay=ANIM_DELAY):
        """Menampilkan pohon dan posisi agen ('<== AGEN')."""
        clear_output(wait=True)             # Bersihkan output sebelumnya
        self._draw(self.start, "", True, True)
        print("-" * 40)
        time.sleep(delay)                   # Jeda sekian detik untuk visualisasi

    def _draw(self, node, prefix, is_last, is_root):
        """Mencetak pohon secara rekursif; node agen diberi tanda."""
        if node == self.node:
            label = f"[{node}] <== AGEN"
        elif node in self.explored_path:
            label = f"({node})"             # Node yang sudah dilewati agen
        else:
            label = node
        if is_root:
            print(label)
        else:
            print(prefix + ("└── " if is_last else "├── ") + label)
        children = self.get_children(node)
        for idx, child in enumerate(children):
            new_prefix = prefix if is_root else prefix + ("    " if is_last else "│   ")
            self._draw(child, new_prefix, idx == len(children) - 1, False)

    def find_path(self, max_steps=1000):
        """Metode untuk mencari jalur. Diimplementasikan oleh subclass (BFS/DFS)."""
        # Metode ini akan di-override di kelas BFS dan DFS
        print("Metode find_path belum diimplementasikan!")
        return []

    def run(self, max_search_steps=1000):
        """
        Menjalankan pencarian jalur, menampilkan status akhir pencarian,
        mensimulasikan pergerakan, dan menampilkan list pergerakan.
        """
        print(f"Memulai pencarian jalur menggunakan {self.__class__.__name__}...")
        # 1. Cari jalur (metode find_path akan menampilkan status akhir open & closed list)
        self.path = self.find_path(max_steps=max_search_steps)

        if not self.path:
            # Jika find_path mengembalikan list kosong
            print("Pencarian selesai. Jalur tidak ditemukan.")
            self.found_path = False
            # Tampilkan posisi akhir agen (masih di node awal)
            self.display()
            print(f"Agen tetap di node awal: {self.node}")
            print(f"List Pergerakan Aktual Agen: {self.explored_path}")  # Hanya berisi node awal
            return self.steps               # Kembalikan 0 langkah
        else:
            # Jika find_path mengembalikan jalur
            print(f"Pencarian selesai. Jalur ditemukan ({len(self.path) - 1} langkah potensial).")
            print("Memulai simulasi pergerakan agen...")
            self.found_path = True
            time.sleep(3)                   # Jeda lebih lama setelah hasil pencarian ditampilkan

            # 2. Ikuti jalur yang ditemukan dengan visualisasi
            # Tampilkan posisi awal sebelum loop
            self.display()
            for i in range(1, len(self.path)):
                # Perbarui posisi agen sesuai jalur dari find_path
                self.node = self.path[i]
                self.steps += 1                         # Hitung langkah aktual
                self.explored_path.append(self.node)    # Catat pergerakan
                self.display()                          # Tampilkan pergerakan

            # 3. Tampilkan hasil akhir simulasi pergerakan
            if self.node == self.goal:
                print(f"Agen berhasil mencapai tujuan dalam {self.steps} langkah aktual.")
            else:
                # Seharusnya tidak terjadi jika find_path benar
                print(f"Agen berhenti di {self.node} setelah {self.steps} langkah aktual.")

            # Menampilkan list pergerakan agen yang sebenarnya
            print(f"Node yang diperiksa saat pencarian: {self.nodes_expanded}")
            print(f"Ukuran open list maksimum: {self.max_frontier}")
            print(f"List Pergerakan Aktual Agen: {self.explored_path}")  # Tampilkan path aktual
            return self.steps               # Kembalikan total langkah aktual


# ============================================================
# BREADTH-FIRST SEARCH (menggunakan Queue / FIFO)
# ============================================================
class BFSAgent(TreeSearchAgent):
    """Agen yang menggunakan Breadth-First Search untuk mencari jalur terpendek."""

    def find_path(self, max_steps=1000):
        """Mencari jalur terpendek menggunakan BFS dan menampilkan hasil pencarian."""
        start_pos = self.start
        goal_pos = self.goal

        queue = deque([(start_pos, [start_pos])])   # Antrian BFS (open list)
        visited = {start_pos}                       # Set node yang sudah ditemukan
        closed = []                                 # Node yang sudah diurai (closed list)
        steps_count = 0
        final_path = []                             # Untuk menyimpan jalur jika ditemukan
        self.max_frontier = len(queue)

        print("--- Memulai Pencarian BFS ---")

        while queue and steps_count < max_steps:
            steps_count += 1
            current_pos, path = queue.popleft()     # Ambil node dari depan antrian

            if current_pos == goal_pos:             # Cek apakah tujuan tercapai
                final_path = path                   # Simpan jalur
                break                               # Hentikan pencarian jika tujuan ditemukan

            closed.append(current_pos)              # Node selesai diurai

            # Eksplorasi anak
            for neighbor in self.get_children(current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)           # Tandai sudah ditemukan
                    new_path = path + [neighbor]    # Buat jalur baru
                    queue.append((neighbor, new_path))  # Masukkan ke akhir antrian
            self.max_frontier = max(self.max_frontier, len(queue))

        self.nodes_expanded = steps_count
        print("Open list akhir (queue) :", [node for node, _ in queue])
        print("Closed list akhir       :", closed)
        return final_path                           # Kembalikan jalur (kosong jika tidak ditemukan)


# ============================================================
# DEPTH-FIRST SEARCH (menggunakan Stack / LIFO)
# ============================================================
class DFSAgent(TreeSearchAgent):
    """Agen yang menggunakan Depth-First Search untuk mencari jalur."""

    def find_path(self, max_steps=1000):
        """Mencari jalur menggunakan DFS dan menampilkan hasil pencarian."""
        start_pos = self.start
        goal_pos = self.goal

        stack = [(start_pos, [start_pos])]          # Tumpukan DFS (open list)
        visited = set()                             # Set node yang sudah diexpand
        closed = []                                 # Urutan node yang sudah diexpand
        steps_count = 0
        final_path = []                             # Untuk menyimpan jalur jika ditemukan
        self.max_frontier = len(stack)

        print("--- Memulai Pencarian DFS ---")

        while stack and steps_count < max_steps:
            steps_count += 1
            current_pos, path = stack.pop()         # Ambil node dari atas tumpukan

            if current_pos in visited:              # Lewati jika sudah pernah diexpand
                continue
            visited.add(current_pos)                # Tandai sudah diexpand

            if current_pos == goal_pos:             # Cek apakah tujuan tercapai
                final_path = path                   # Simpan jalur
                break                               # Hentikan pencarian

            closed.append(current_pos)              # Node selesai diurai

            # Eksplorasi anak (dibalik agar anak paling kiri berada di atas tumpukan)
            for neighbor in reversed(self.get_children(current_pos)):
                if neighbor not in visited:         # Hanya tambahkan yang belum diexpand
                    new_path = path + [neighbor]
                    stack.append((neighbor, new_path))  # Masukkan ke tumpukan
            self.max_frontier = max(self.max_frontier, len(stack))

        self.nodes_expanded = steps_count
        print("Open list akhir (stack) :", [node for node, _ in reversed(stack)])  # atas stack di kiri
        print("Closed list akhir       :", closed)
        return final_path                           # Kembalikan jalur (kosong jika tidak ditemukan)


# ============================================================
# EVALUASI DAN PERBANDINGAN BFS vs DFS
# ============================================================
def evaluate_agent(agent_class, env, start, goal, max_steps=1000):
    """Menjalankan pencarian saja (tanpa animasi) dan mengembalikan metrik kinerja."""
    agent = agent_class(env, start, goal)

    # Sembunyikan print dari find_path agar output evaluasi tidak ramai
    with contextlib.redirect_stdout(io.StringIO()):
        path = agent.find_path(max_steps=max_steps)

    if path and path[-1] == goal:
        return {
            "langkah": len(path) - 1,
            "expanded": agent.nodes_expanded,
            "frontier": agent.max_frontier,
            "path": path,
        }
    return {
        "langkah": float('inf'),
        "expanded": agent.nodes_expanded,
        "frontier": agent.max_frontier,
        "path": [],
    }


def compare_agents(env, start, goal):
    """Menampilkan ringkasan performa BFS vs DFS dalam tabel dan grafik."""
    agent_classes = [BFSAgent, DFSAgent]
    agent_names = ['BFS Agent', 'DFS Agent']
    results = [evaluate_agent(cls, env, start, goal) for cls in agent_classes]

    # --- Tampilkan Ringkasan ---
    print("\n" + "=" * 78)
    print(" RINGKASAN PERFORMA PENCARIAN")
    print("=" * 78)
    print(f"{'Algoritma':<12} | {'Langkah':<8} | {'Node Diperiksa':<15} | {'Open List Maks':<15} | Jalur")
    print("-" * 78)
    for name, r in zip(agent_names, results):
        langkah = str(r["langkah"]) if r["langkah"] != float('inf') else "Gagal"
        jalur = " -> ".join(r["path"]) if r["path"] else "-"
        print(f"{name:<12} | {langkah:<8} | {r['expanded']:<15} | {r['frontier']:<15} | {jalur}")
    print("=" * 78)

    # --- Visualisasi Perbandingan (3 metrik) ---
    metrics = [
        ("langkah",  "Jumlah Langkah Aktual"),
        ("expanded", "Node yang Diperiksa"),
        ("frontier", "Ukuran Open List Maksimum"),
    ]
    colors = ['skyblue', 'lightgreen']

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (key, title) in zip(axes, metrics):
        original = [r[key] for r in results]
        # Ganti infinity dengan 0 agar bisa digambar
        plot_vals = [v if v != float('inf') else 0 for v in original]

        bars = ax.bar(agent_names, plot_vals, color=colors)
        for bar, orig in zip(bars, original):
            label = str(orig) if orig != float('inf') else "Gagal"
            ax.text(bar.get_x() + bar.get_width() / 2.0, bar.get_height(),
                    label, va='bottom', ha='center', fontweight='bold')

        ax.set_title(title)
        ax.set_ylabel(title)
        ax.set_ylim(bottom=0, top=max(plot_vals + [1]) * 1.2)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.suptitle("Perbandingan Kinerja BFS vs DFS (Semakin Rendah Semakin Baik)",
                 fontweight='bold')
    fig.tight_layout()
    plt.show()

def print_menu():
    """Menampilkan menu pilihan algoritma pencarian."""
    print("Pilih algoritma pencarian:")
    print("1. Breadth-First Search (BFS)")
    print("2. Depth-First Search (DFS)")
    print("3. Tampilkan pohon dan ringkasan")
    print("4. Bandingkan performa BFS vs DFS")
    print("5. Visualisasi pencarian")
    print("0. Exit")

if __name__ == "__main__":

    pass_1 = False
    pass_2 = False

    while(True):
        clear_output(wait=True)
        print_menu()
        print()
        choice = input("Masukkan pilihan (0-5): ")
        choice = int(choice)
        
        if choice == 0:
            print("Terima kasih telah menggunakan program ini.")
            break
        elif choice == 1:
            clear_output(wait=True)
            agent = BFSAgent(environment, start_node, goals_node)
            agent.run()
            input("\nTekan Enter untuk kembali ke menu...")
            pass_1 = True
        elif choice == 2:
            clear_output(wait=True)
            agent = DFSAgent(environment, start_node, goals_node)
            agent.run()
            input("\nTekan Enter untuk kembali ke menu...")
            pass_2 = True
        elif choice == 4:
            if(pass_1 or pass_2):
                clear_output(wait=True)
                compare_agents(environment, start_node, goals_node)
                input("\nTekan Enter untuk kembali ke menu...")
            else:
                clear_output(wait=True)
                print("Silakan jalankan BFS dan DFS terlebih dahulu sebelum membandingkan performa.")
                input("\nTekan Enter untuk kembali ke menu...")
        elif choice == 3:
            clear_output(wait=True)
            print_tree(environment, start_node)
            n_node, n_depth, n_branch = tree_summary(environment, start_node)
            print(f"\nJumlah node: {n_node} | Kedalaman maksimum: {n_depth} | Percabangan maksimum: {n_branch}")
            print(f"Node awal: {start_node} | Node tujuan: {goals_node}")
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == 5:
            clear_output(wait=True)
            buka_flet(environment, start_node, goals_node, "BFS")   # ganti BFS dengan "DFS" jika ingin menggunakan DFS