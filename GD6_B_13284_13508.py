import collections
import collections.abc

# collections.Iterable = getattr(collections.abc, "Iterable", collections.Iterable)
# collections.Iterator = getattr(collections.abc, "Iterator", collections.Iterator)
# collections.Mapping = getattr(collections.abc, "Mapping", collections.Mapping)
# collections.Hashable = getattr(collections.abc, "Hashable", collections.Hashable)

collections.Iterable = collections.abc.Iterable
collections.Iterator = collections.abc.Iterator
collections.Mapping = collections.abc.Mapping
collections.Hashable = collections.abc.Hashable

from kanren import run, var, lall, membero, eq, Relation, facts, conde

father = Relation()
mother = Relation()

facts(father, 
      ('John', 'William'), ('John', 'David'), ('John', 'Adam'),
      ('William', 'Chris'), ('William', 'Stephanie'), 
      ('David', 'Wayne'), ('David', 'Tiffany'), ('David', 'Julie'), ('David', 'Neil'), ('David', 'Peter'),
      ('Adam', 'Sophia')
)

facts(mother,
      ('Megan', 'William'), ('Megan', 'David'), ('Megan', 'Adam'),
      ('Emma', 'Stephanie'), ('Emma', 'Chris'),
      ('Olivia', 'Tiffany'), ('Olivia', 'Julie'), ('Olivia', 'Neil'), ('Olivia', 'Peter'),
      ('Lily', 'Sophia')
)

def parent(x, y):
    return conde((father(x, y),), (mother(x, y),))

def grandparent(x, y):
    z = var()
    return conde((parent(x, z), parent(z, y)),)

def uncle(x, y):
    z = var()
    return conde((father(z, x), grandparent(z, y)),)

def cari_paman(nama):
    x = var()
    hasil = run(0, x, uncle(x, nama))
    ayah = run(0, x, father(x, nama))
    if ayah:
        hasil = [p for p in hasil if p not in ayah]
    return hasil

def pecahkan_puzzle_tech():
    p1, p2, p3, p4 = var(), var(), var(), var()
    pro = [p1, p2, p3, p4]

    aturan = lall(
        membero(('Rina', 'Data Scientist', var(), var()), pro),
        membero((var(), 'Web Developer', 'JavaScript', var()), pro),
        membero((var(), 'AI Engineer', 'C++', var()), pro),
        membero(('Budi', 'AI Engineer', var(), 'Olahraga'), pro),
        membero(('Dini', 'UX Designer', var(), var()), pro),
        membero((var(), var(), 'Swift', 'Gaming'), pro),
        membero((var(), 'Data Scientist', 'Python', var()), pro),
        membero((var(), var(), var(), 'Membaca'), pro),

        eq(p1, (var(), var(), var(), var())),
        eq(p2, (var(), var(), var(), var())),
        eq(p3, (var(), var(), var(), var())),
        eq(p4, (var(), var(), var(), var()))
    )

    return run(0, pro, aturan)


def main():

    while True:
        print("\n=====================================")
        print("      PEMROGRAMAN LOGIKA (KANREN)      ")
        print("=====================================")
        print("1. Memecahkan Puzzle Tim Tech")
        print("2. Cari Anak Pasangan (David & Olivia)")
        print("3. Cari Paman Seseorang")
        print("4. Keluar")
        print("=====================================")


        try:
            pilihan = int(input("Pilih Menu: "))

            if pilihan == 1:
                print("\n=== HASIL PUZZLE TIM TECH ===")
                solutions = pecahkan_puzzle_tech()
                if solutions:
                    solusi = solutions[0]
                    for orang in solusi:
                        print(f"Nama: {orang[0]}, Perofesi: {orang[1]}, Bahasa: {orang[2]}, Hobi: {orang[3]}")

                    pembaca = [o[0] for o in solusi if o[3] == 'Membaca']
                    print(f"\nOrang yang hobi Membaca: {pembaca[0] if pembaca else '-'}")
                else:
                    print("Tidak ada solusi yang ditemukan.")

            elif pilihan == 2:
                print("\n=== ANAK DARI DAVID & OLIVIA ===")
                x = var()
                anak = run(0, x, father('David', x), mother('Olivia', x))
                for a in anak:
                    print(f"- {a}")

            elif pilihan == 3:
                print("\n=== CARI PAMAN ===")
                nama = input("Masukkan nama keponakan: ").strip().capitalize()
                paman = cari_paman(nama)
                if paman:
                    print(f"Paman dari {nama} adalah : {', '.join(paman)}")
                else:
                    print("Data paman tidak ditemukan")

            elif pilihan == 4:
                print("program selesai.")
                break

            else:
                print("Pilihan tidak valid.")

        except ValueError:
            print("Input harus berupa angka.")


if __name__ == "__main__":
    main()