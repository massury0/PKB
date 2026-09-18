import matplotlib.pyplot as plt

hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
data_produksi = []

status = False


def tampilkan_menu():
    print("\n===========================")
    print("   DATA PRODUKSI ALVA FARM")
    print("===========================")
    print("1. Tambah Data Produksi")
    print("2. Lihat Data Produksi")
    print("3. Ubah Data Produksi")
    print("4. Keluar")

def tambah_data():
    print("\n=== TAMBAH DATA PRODUKSI ===")
    
    if status : 
        print("DATA PRODUKSI SUDAH PERNAH DIISI! SILAHKAN GUNAKAN MENU UBAH DATA UNTUK MENGUBAH")
    else :
        for i in hari :
           
            inputData = int(input(f"Masukkan jumlah produksi hari {i}       : "))
            data_produksi.append(inputData)

    


def tampil_data():
    print("\n=== DATA PRODUKSI ===")
        
    if not status : 
        print("DATA PRODUKSI MASIH KOSONG!")
    else :
        for i in range(len(hari)):
            print(f"{i+1}. {hari[i]}        : {data_produksi[i]} kg")
        


        total = sum(data_produksi)
        rata = total / len(hari)
        maxH = max(data_produksi)
        index_max= data_produksi.index(maxH) 
        minH = min(data_produksi)
        index_min= data_produksi.index(minH) 
        print(f"Total Produksi 1 Minggu    : {total} kg")
        print(f"Rata-rata Produksi Perhari : {rata} kg")
        print(f"Hari dengan jumlah produksi terbanyak {hari[index_max]} : {maxH} kg")
        print(f"Hari dengan jumlah produksi paling sedikit {hari[index_min]} : {minH} kg")

        show_graph()

def edit_data():

    print("\n=== UBAH DATA PRODUKSI ===")

    if not status : 
            print("DATA PRODUKSI MASIH KOSONG!")
    else :

        for i in range(len(hari)):
            print(f"{i+1}. {hari[i]}        : {data_produksi[i]} kg")
                    

        index_rubah = int(input("Pilih nomor yang ingin diubah : "))
        print(f"Data Sebelumnya : {data_produksi[index_rubah-1]} kg")

        data_baru = int(input("Masukkan jumlah produksi baru : "))
        data_produksi[index_rubah-1] = data_baru

        print("Data berhasil diubah")

def show_graph():

    x = hari
    y = data_produksi

    plt.plot(x, y, marker='o')
    plt.xlabel('Hari')
    plt.ylabel('Jumlah Produksi (kg)')
    plt.title('Grafik Produksi Harian')
    plt.show()



def main():

    while True:
        tampilkan_menu()

        try:
            pilihan = int(input("Masukkan pilihan : "))

            if pilihan == 1:
                tambah_data()
                global status
                status = True

            elif pilihan == 2:
                tampil_data()

            elif pilihan == 3:
                edit_data()

            elif pilihan == 4:
                print("Terima kasih telah menggunakan program ini.")
                break

            else:
                print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")

        except ValueError:
            print("Input tidak valid. Silakan masukkan angka.")

if __name__ == "__main__":
    main()