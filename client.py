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
    print("=== University Management System ===")
    print("1. Mahasiswa Management")
    print("2. Mata Kuliah Management")
    print("3. EXIT")
    print("================================")

def print_submenu(menu_type):
    clear_screen()
    print(f"=== {menu_type} Management ===")
    print("1. INSERT - Add New")
    print("2. READALL - View All")
    print("3. GETID - Find by ID")
    print("4. UPDATE - Update")
    print("5. DELETE - Delete")
    print("6. Back to Main Menu")
    print("===========================")

# Mahasiswa Functions
def insert_mahasiswa():
    print("\n=== Add New Mahasiswa ===")
    nim = input("Enter NIM: ").strip()
    nama = input("Enter Nama: ").strip()
    while True:
        tanggal_lahir = input("Enter Tanggal Lahir (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD")
    alamat = input("Enter Alamat: ").strip()
    while True:
        jenis_kelamin = input("Enter Jenis Kelamin (L/P): ").strip().upper()
        if jenis_kelamin in ['L', 'P']:
            break
        print("Error: Jenis Kelamin must be 'L' or 'P'!")
    
    if not all([nim, nama, tanggal_lahir, alamat, jenis_kelamin]):
        print("Error: All fields are required!")
        input("\nPress Enter to continue...")
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
            print("\nSuccess! Mahasiswa created.")
            print(f"ID: {response.json()['id']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def read_all_mahasiswa():
    print("\n=== All Mahasiswa ===")
    try:
        response = requests.get(f"{BASE_URL}/mahasiswa")
        if response.status_code == 200:
            mahasiswa_list = response.json()
            if not mahasiswa_list:
                print("No mahasiswa found.")
            else:
                print("\nID\tNIM\t\tNama\t\tTanggal Lahir\tAlamat\t\tJenis Kelamin")
                print("-" * 100)
                for mhs in mahasiswa_list:
                    print(f"{mhs['id']}\t{mhs['nim']}\t{mhs['nama']}\t{mhs['tanggal_lahir']}\t{mhs['alamat']}\t{mhs['jenis_kelamin']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def get_mahasiswa_by_id():
    print("\n=== Find Mahasiswa by ID ===")
    try:
        id = int(input("Enter mahasiswa ID: "))
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
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def update_mahasiswa():
    print("\n=== Update Mahasiswa ===")
    try:
        id = int(input("Enter mahasiswa ID to update: "))
        
        response = requests.get(f"{BASE_URL}/mahasiswa/{id}")
        if response.status_code != 200:
            print(f"\nError: Mahasiswa not found")
            input("\nPress Enter to continue...")
            return
        
        current_mhs = response.json()
        print("\nCurrent details:")
        print(f"NIM: {current_mhs['nim']}")
        print(f"Nama: {current_mhs['nama']}")
        print(f"Tanggal Lahir: {current_mhs['tanggal_lahir']}")
        print(f"Alamat: {current_mhs['alamat']}")
        print(f"Jenis Kelamin: {current_mhs['jenis_kelamin']}")
        
        print("\nEnter new details (press Enter to keep current value):")
        update_data = {}
        
        nim = input("New NIM: ").strip()
        if nim:
            update_data['nim'] = nim
            
        nama = input("New Nama: ").strip()
        if nama:
            update_data['nama'] = nama
            
        tanggal_lahir = input("New Tanggal Lahir (YYYY-MM-DD): ").strip()
        if tanggal_lahir:
            try:
                datetime.strptime(tanggal_lahir, '%Y-%m-%d')
                update_data['tanggal_lahir'] = tanggal_lahir
            except ValueError:
                print("Invalid date format! This field will not be updated.")
                
        alamat = input("New Alamat: ").strip()
        if alamat:
            update_data['alamat'] = alamat
            
        jenis_kelamin = input("New Jenis Kelamin (L/P): ").strip().upper()
        if jenis_kelamin:
            if jenis_kelamin in ['L', 'P']:
                update_data['jenis_kelamin'] = jenis_kelamin
            else:
                print("Invalid Jenis Kelamin! This field will not be updated.")
        
        if not update_data:
            print("\nNo changes made.")
            input("\nPress Enter to continue...")
            return
        
        response = requests.put(f"{BASE_URL}/mahasiswa/{id}", json=update_data)
        
        if response.status_code == 200:
            print("\nSuccess! Mahasiswa updated.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def delete_mahasiswa():
    print("\n=== Delete Mahasiswa ===")
    try:
        id = int(input("Enter mahasiswa ID to delete: "))
        
        confirm = input(f"Are you sure you want to delete mahasiswa {id}? (y/N): ").lower()
        if confirm != 'y':
            print("\nDeletion cancelled.")
            input("\nPress Enter to continue...")
            return
        
        response = requests.delete(f"{BASE_URL}/mahasiswa/{id}")
        
        if response.status_code == 200:
            print("\nSuccess! Mahasiswa deleted.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

# Mata Kuliah Functions
def insert_matkul():
    print("\n=== Add New Mata Kuliah ===")
    kode_mk = input("Enter Kode MK: ").strip()
    nama_mk = input("Enter Nama MK: ").strip()
    while True:
        try:
            sks = int(input("Enter SKS: ").strip())
            if 1 <= sks <= 6:  # Assuming valid SKS range is 1-6
                break
            print("SKS must be between 1 and 6!")
        except ValueError:
            print("Please enter a valid number for SKS!")
    
    if not all([kode_mk, nama_mk]):
        print("Error: All fields are required!")
        input("\nPress Enter to continue...")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/matkul", json={
            "kode_mk": kode_mk,
            "nama_mk": nama_mk,
            "sks": sks
        })
        
        if response.status_code == 201:
            print("\nSuccess! Mata Kuliah created.")
            print(f"ID: {response.json()['id']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def read_all_matkul():
    print("\n=== All Mata Kuliah ===")
    try:
        response = requests.get(f"{BASE_URL}/matkul")
        if response.status_code == 200:
            matkul_list = response.json()
            if not matkul_list:
                print("No mata kuliah found.")
            else:
                print("\nID\tKode MK\t\tNama MK\t\t\tSKS")
                print("-" * 70)
                for mk in matkul_list:
                    print(f"{mk['id']}\t{mk['kode_mk']}\t\t{mk['nama_mk']}\t\t{mk['sks']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def get_matkul_by_id():
    print("\n=== Find Mata Kuliah by ID ===")
    try:
        id = int(input("Enter mata kuliah ID: "))
        response = requests.get(f"{BASE_URL}/matkul/{id}")
        
        if response.status_code == 200:
            mk = response.json()
            print("\nMata Kuliah Details:")
            print(f"ID: {mk['id']}")
            print(f"Kode MK: {mk['kode_mk']}")
            print(f"Nama MK: {mk['nama_mk']}")
            print(f"SKS: {mk['sks']}")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def update_matkul():
    print("\n=== Update Mata Kuliah ===")
    try:
        id = int(input("Enter mata kuliah ID to update: "))
        
        response = requests.get(f"{BASE_URL}/matkul/{id}")
        if response.status_code != 200:
            print(f"\nError: Mata Kuliah not found")
            input("\nPress Enter to continue...")
            return
        
        current_mk = response.json()
        print("\nCurrent details:")
        print(f"Kode MK: {current_mk['kode_mk']}")
        print(f"Nama MK: {current_mk['nama_mk']}")
        print(f"SKS: {current_mk['sks']}")
        
        print("\nEnter new details (press Enter to keep current value):")
        update_data = {}
        
        kode_mk = input("New Kode MK: ").strip()
        if kode_mk:
            update_data['kode_mk'] = kode_mk
            
        nama_mk = input("New Nama MK: ").strip()
        if nama_mk:
            update_data['nama_mk'] = nama_mk
            
        sks_input = input("New SKS: ").strip()
        if sks_input:
            try:
                sks = int(sks_input)
                if 1 <= sks <= 6:
                    update_data['sks'] = sks
                else:
                    print("Invalid SKS value! This field will not be updated.")
            except ValueError:
                print("Invalid SKS format! This field will not be updated.")
        
        if not update_data:
            print("\nNo changes made.")
            input("\nPress Enter to continue...")
            return
        
        response = requests.put(f"{BASE_URL}/matkul/{id}", json=update_data)
        
        if response.status_code == 200:
            print("\nSuccess! Mata Kuliah updated.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

def delete_matkul():
    print("\n=== Delete Mata Kuliah ===")
    try:
        id = int(input("Enter mata kuliah ID to delete: "))
        
        confirm = input(f"Are you sure you want to delete mata kuliah {id}? (y/N): ").lower()
        if confirm != 'y':
            print("\nDeletion cancelled.")
            input("\nPress Enter to continue...")
            return
        
        response = requests.delete(f"{BASE_URL}/matkul/{id}")
        
        if response.status_code == 200:
            print("\nSuccess! Mata Kuliah deleted.")
        else:
            print(f"\nError: {response.json().get('error', 'Unknown error occurred')}")
    except ValueError:
        print("\nError: Please enter a valid ID number")
    except requests.RequestException as e:
        print(f"\nError connecting to server: {e}")
    
    input("\nPress Enter to continue...")

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
            input("\nPress Enter to continue...")

def matkul_menu():
    while True:
        print_submenu("Mata Kuliah")
        choice = input("\nEnter your choice (1-6): ")
        
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
            print("\nInvalid choice! Please try again.")
            input("\nPress Enter to continue...")

def main():
    print("\nWelcome to University Management System")
    print("Connecting to server...")
    
    # Test server connection
    try:
        requests.get(f"{BASE_URL}/mahasiswa")
        print("Server connection successful!")
    except requests.RequestException:
        print("Error: Could not connect to server!")
        print("Please make sure the server is running at", BASE_URL)
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    input("\nPress Enter to continue...")
    
    while True:
        print_main_menu()
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            mahasiswa_menu()
        elif choice == '2':
            matkul_menu()
        elif choice == '3':
            print("\nThank you for using University Management System!")
            print("Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice! Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()