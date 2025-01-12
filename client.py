# cli_client.py
import requests
import sys
import os
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_menu():
    clear_screen()
    print("=== Sistem Manajemen Universitas ===")
    print("1. Manajemen Mahasiswa ")
    print("2. Manajemen Mata Kuliah ")
    print("3. EXIT")
    print("================================")

def print_submenu(menu_type):
    clear_screen()
    print(f"=== Manajemen {menu_type}  ===")
    print("1. INSERT - Menambah data baru")
    print("2. READALL - Menampilkan semua data")
    print("3. GETID - Mencari data berdasarkan ID")
    print("4. UPDATE - Mengubah data")
    print("5. DELETE - menghapus data")
    print("6. Kembali ke Menu Utama")
    print("===========================")

# Mahasiswa Functions
def insert_mahasiswa():
    print("\n=== Menambah data Mahasiswa ===")
    nim = input("Masukkan NIM: ").strip()
    nama = input("Masukkan Nama: ").strip()
    while True:
        tanggal_lahir = input("Masukkan Tanggal Lahir (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            break
        except ValueError:
            print("format Tanggal tidak sesuai! tolong gunakan format YYYY-MM-DD")
    alamat = input("Masukkan Alamat: ").strip()
    while True:
        jenis_kelamin = input("Masukkan Jenis Kelamin (L/P): ").strip().upper()
        if jenis_kelamin in ['L', 'P']:
            break
        print("Error: Jenis Kelamin harus 'L' Atau 'P'!")
    
    if not all([nim, nama, tanggal_lahir, alamat, jenis_kelamin]):
        print("Error: Semua data harus disi!")
        input("\nTekan Enter untuk melanjutkan...")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/mahasiswa", json={
            "nim": nim,
            "nama": nama,
            "tanggal_lahir": tanggal_lahir,
            "alamat": alamat,
            "jenis_kelamin": jenis_kelamin
        })
        
        if response.status_code == 201:
            print("\nData Mahasiswa berhasil ditambahkan")
            print(f"ID: {response.json()['id']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def read_all_mahasiswa():
    print("\n=== Semua Data Mahasiswa ===")
    try:
        response = requests.get(f"{BASE_URL}/mahasiswa")
        if response.status_code == 200:
            mahasiswa_list = response.json()
            if not mahasiswa_list:
                print("data mahasiswa tidak ditemukan.")
            else:
                print("\nID\tNIM\t\tNama\t\tTanggal Lahir\tAlamat\t\tJenis Kelamin")
                print("-" * 100)
                for mhs in mahasiswa_list:
                    print(f"{mhs['id']}\t{mhs['nim']}\t{mhs['nama']}\t{mhs['tanggal_lahir']}\t{mhs['alamat']}\t{mhs['jenis_kelamin']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def get_mahasiswa_by_id():
    print("\n=== Find Mahasiswa by ID ===")
    try:
        id = int(input("Masukkan mahasiswa ID: "))
        response = requests.get(f"{BASE_URL}/mahasiswa/{id}")
        
        if response.status_code == 200:
            mhs = response.json()
            print("\nMahasiswa Details:")
            print(f"ID: {mhs['id']}")
            print(f"NIM: {mhs['nim']}")
            print(f"Nama: {mhs['nama']}")
            print(f"Tanggal Lahir: {mhs['tanggal_lahir']}")
            print(f"Alamat: {mhs['alamat']}")
            print(f"Jenis Kelamin: {mhs['jenis_kelamin']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Tolong masukkan data no ID yang benar")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def update_mahasiswa():
    print("\n=== Ubah Data Mahasiswa ===")
    try:
        id = int(input("Masukkan ID mahasiswa untuk mengubah data: "))
        
        response = requests.get(f"{BASE_URL}/mahasiswa/{id}")
        if response.status_code != 200:
            print(f"\nError: Data Mahasiswa tidak ditemukan")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        current_mhs = response.json()
        print("\nDetail saat ini:")
        print(f"NIM: {current_mhs['nim']}")
        print(f"Nama: {current_mhs['nama']}")
        print(f"Tanggal Lahir: {current_mhs['tanggal_lahir']}")
        print(f"Alamat: {current_mhs['alamat']}")
        print(f"Jenis Kelamin: {current_mhs['jenis_kelamin']}")
        
        print("\nMasukkan detail baru (tekan Enter untuk mempertahankan nilai saat ini):")
        update_data = {}
        
        nim = input("Data NIM terbaru: ").strip()
        if nim:
            update_data['nim'] = nim
            
        nama = input("Data Nama terbaru: ").strip()
        if nama:
            update_data['nama'] = nama
            
        tanggal_lahir = input("Data Tanggal Lahir (YYYY-MM-DD) terbaru: ").strip()
        if tanggal_lahir:
            try:
                datetime.strptime(tanggal_lahir, '%Y-%m-%d')
                update_data['tanggal_lahir'] = tanggal_lahir
            except ValueError:
                print("Format tanggal tidak valid! Bidang ini tidak akan diperbarui.")
                
        alamat = input("Data Alamat terbaru: ").strip()
        if alamat:
            update_data['alamat'] = alamat
            
        jenis_kelamin = input("Data Jenis Kelamin (L/P) terbaru: ").strip().upper()
        if jenis_kelamin:
            if jenis_kelamin in ['L', 'P']:
                update_data['jenis_kelamin'] = jenis_kelamin
            else:
                print("Jenis Kelamin tidak valid! Bidang ini tidak akan diperbarui.")
        
        if not update_data:
            print("\nTidak ada perubahan yang dilakukan.")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        response = requests.put(f"{BASE_URL}/mahasiswa/{id}", json=update_data)
        
        if response.status_code == 200:
            print("\nSukses! Data Mahasiswa diperbarui.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Silakan masukkan nomor ID yang valid")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def delete_mahasiswa():
    print("\n=== Hapus Data Mahasiswa ===")
    try:
        id = int(input("Masukkan ID mahasiswa untuk menghapus: "))
        
        confirm = input(f"Apakah anda yakin ingin menghapus mahasiswa {id}? (Y/N): ").lower()
        if confirm != 'y':
            print("\nPenghapusan dibatalkan.")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        response = requests.delete(f"{BASE_URL}/mahasiswa/{id}")
        
        if response.status_code == 200:
            print("\nBerhasil! Data Mahasiswa diperbaharui.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Silakan masukkan nomor ID yang valid")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

# Mata Kuliah Functions
def insert_matkul():
    print("\n=== Menambahkan Data baru Mata Kuliah ===")
    kode_mk = input("Masukkan Kode MK: ").strip()
    nama_mk = input("Masukkan Nama MK: ").strip()
    while True:
        try:
            sks = int(input("Masukkan SKS: ").strip())
            if 1 <= sks <= 6:  # Assuming valid SKS range is 1-6
                break
            print("SKS harus antara 1 dan 6!")
        except ValueError:
            print("Silakan masukkan nomor yang valid untuk SKS!")
    
    if not all([kode_mk, nama_mk]):
        print("Error: Semua data wajib diisi!")
        input("\nTekan Enter untuk melanjutkan...")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/matkul", json={
            "kode_mk": kode_mk,
            "nama_mk": nama_mk,
            "sks": sks
        })
        
        if response.status_code == 201:
            print("\Data Mata Kuliah berhasil ditambahkan.")
            print(f"ID: {response.json()['id']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def read_all_matkul():
    print("\n=== Semua Data Mata Kuliah ===")
    try:
        response = requests.get(f"{BASE_URL}/matkul")
        if response.status_code == 200:
            matkul_list = response.json()
            if not matkul_list:
                print("Tidak ada data mata kuliah yang ditemukan.")
            else:
                print("\nID\tKode MK\t\tNama MK\t\t\tSKS")
                print("-" * 70)
                for mk in matkul_list:
                    print(f"{mk['id']}\t{mk['kode_mk']}\t\t{mk['nama_mk']}\t\t{mk['sks']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def get_matkul_by_id():
    print("\n=== Mencari data Mata Kuliah berdasarkan ID ===")
    try:
        id = int(input("Masukkan mata kuliah ID: "))
        response = requests.get(f"{BASE_URL}/matkul/{id}")
        
        if response.status_code == 200:
            mk = response.json()
            print("\nDetail Data Mata Kuliah:")
            print(f"ID: {mk['id']}")
            print(f"Kode MK: {mk['kode_mk']}")
            print(f"Nama MK: {mk['nama_mk']}")
            print(f"SKS: {mk['sks']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Silakan masukkan nomor ID yang valid")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def update_matkul():
    print("\n=== Ubahh data Mata Kuliah ===")
    try:
        id = int(input("Masukkan data ID mata kuliah untuk memperbarui: "))
        
        response = requests.get(f"{BASE_URL}/matkul/{id}")
        if response.status_code != 200:
            print(f"\nError: Mata Kuliah not found")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        current_mk = response.json()
        print("\nDetail data saat ini:")
        print(f"Kode MK: {current_mk['kode_mk']}")
        print(f"Nama MK: {current_mk['nama_mk']}")
        print(f"SKS: {current_mk['sks']}")
        
        print("\nMasukkan detail data baru (tekan Enter untuk mempertahankan nilai data saat ini):")
        update_data = {}
        
        kode_mk = input("Data Kode MK terbaru: ").strip()
        if kode_mk:
            update_data['kode_mk'] = kode_mk
            
        nama_mk = input("Data Nama MK terbaru: ").strip()
        if nama_mk:
            update_data['nama_mk'] = nama_mk
            
        sks_input = input("Data SKS terbaru: ").strip()
        if sks_input:
            try:
                sks = int(sks_input)
                if 1 <= sks <= 6:
                    update_data['sks'] = sks
                else:
                    print("Nilai SKS tidak valid! Kolom ini tidak akan diperbarui.")
            except ValueError:
                print("Format SKS tidak valid! Kolom ini tidak akan diperbarui.")
        
        if not update_data:
            print("\nTidak ada perubahan yang dilakukan.")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        response = requests.put(f"{BASE_URL}/matkul/{id}", json=update_data)
        
        if response.status_code == 200:
            print("\nSukses! Data Mata Kuliah diperbarui.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Silakan masukkan nomor ID yang valid")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def delete_matkul():
    print("\n=== Delete Mata Kuliah ===")
    try:
        id = int(input("Masukkan mata kuliah ID untuk menghapus: "))
        
        confirm = input(f"Apakah Anda yakin ingin menghapus data mata kuliah {id}? (Y/N): ").lower()
        if confirm != 'y':
            print("\nPenghapusan data dibatalkan.")
            input("\nTekan Enter untuk melanjutkan...")
            return
        
        response = requests.delete(f"{BASE_URL}/matkul/{id}")
        
        if response.status_code == 200:
            print("\nSukses! Data Mata Kuliah dihapus.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Silakan masukkan nomor ID yang valid")
    except requests.RequestException as e:
        print(f"\nKoneksi ke server error: {e}")
    
    input("\nTekan Enter untuk melanjutkan...")

def mahasiswa_menu():
    while True:
        print_submenu("Mahasiswa")
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            insert_mahasiswa()
        elif choice == '2':
            read_all_mahasiswa()
        elif choice == '3':
            get_mahasiswa_by_id()
        elif choice == '4':
            update_mahasiswa()
        elif choice == '5':
            delete_mahasiswa()
        elif choice == '6':
            break
        else:
            print("\nInvalid choice! Please try again.")
            input("\nTekan Enter untuk melanjutkan...")

def matkul_menu():
    while True:
        print_submenu("Mata Kuliah")
        choice = input("\nMasukkan pilhanmu (1-6): ")
        
        if choice == '1':
            insert_matkul()
        elif choice == '2':
            read_all_matkul()
        elif choice == '3':
            get_matkul_by_id()
        elif choice == '4':
            update_matkul()
        elif choice == '5':
            delete_matkul()
        elif choice == '6':
            break
        else:
            print("\nPilihan tidak valid! Silakan coba lagi.")
            input("\nTekan Enter untuk melanjutkan...")

def main():
    print("\nSelamat datang di Sistem Manajemen Universitas")
    print("Menghubungkan ke server...")
    
    # Test server connection
    try:
        requests.get(f"{BASE_URL}/mahasiswa")
        print("Koneksi server berhasil!")
    except requests.RequestException:
        print("Error: Tidak dapat terhubung ke server!")
        print("Pastikan server berjalan di", BASE_URL)
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    input("\nTekan Enter untuk melanjutkan...")
    
    while True:
        print_main_menu()
        choice = input("\nMasukkan pilihanmu (1-3): ")
        
        if choice == '1':
            mahasiswa_menu()
        elif choice == '2':
            matkul_menu()
        elif choice == '3':
            print("\nTerima kasih telah menggunakan Sistem Manajemen Universitas!")
            print("Sampai jumpa!")
            sys.exit(0)
        else:
            print("\nPilihan tidak valid! Silakan coba lagi.")
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()