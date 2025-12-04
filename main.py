from avl_tree import AVLTree
from books_db import load_books, save_books
from book import Book
from user_db import authenticate, register_user
import time
import pandas as pd 

avl = AVLTree()
root = None
book_list = []


def print_menu(title, options):
    items = [f"{i}. {opt}" for i, opt in enumerate(options, 1)]
    width = max(len(title), *(len(it) for it in items)) + 4
    line = "+" + "-" * width + "+"
    print("\n" + line)
    print(f"| {title.center(width - 2)} |")
    print(line)
    for it in items:
        print(f"| {it.ljust(width - 2)} |")
    print(line)


def login():
    print("\n======== LOGIN SISTEM ========")
    username = input("Username : ")
    password = input("Password : ")

    user = authenticate(username, password)
    if user is None:
        print("Login gagal! Username atau password salah.\n")
        return

    if user.role == "admin":
        print(f"\nSelamat datang Admin, {user.username}!\n")
        admin_menu()
    else:
        print(f"\nSelamat datang {user.username} \n")
        user_menu()


def register():
    print("\n======== REGISTER ========")
    username = input("Buat username : ")
    password = input("Buat password : ")
    if not username.strip() or not password.strip():
        print("Username dan password tidak boleh kosong.\n")
        return
    created = register_user(username, password)
    print("Registrasi berhasil! Silakan login.\n" if created else "Registrasi gagal: username sudah digunakan.\n")


def get_valid_input(prompt, allow_empty=False, is_numeric=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            if is_numeric and value:
                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    return value
                print("Harus berupa angka. Coba lagi.")
            else:
                return value
        elif allow_empty:
            return ""
        else:
            print("Input tidak boleh kosong atau hanya spasi. Coba lagi.")


def print_books_table(books):
    if not books:
        print("Tidak ada buku untuk ditampilkan.\n")
        return

    headers = ["ID", "Judul", "Penulis", "Tahun", "Kategori", "Stok", "Lokasi"]
    col_widths = [6, 35, 25, 8, 18, 8, 15]

    for i, header in enumerate(headers):
        max_len = len(header)
        for book in books:
            value = str(getattr(book, ["key", "title", "author", "year", "category", "stock", "location"][i]))
            max_len = max(max_len, len(value))
        col_widths[i] = max(col_widths[i], max_len + 2)

    print("┏" + "┳".join("━" * w for w in col_widths) + "┓")

    header_row = "┃"
    for i, h in enumerate(headers):
        header_row += f" {h.center(col_widths[i]-2)} ┃"
    print(header_row)

    print("┣" + "╋".join("━" * w for w in col_widths) + "┫")

    for book in books:
        row = "┃"
        values = [
            book.key,
            book.title,
            book.author,
            book.year,
            book.category,
            str(book.stock),
            book.location
        ]
        for i, val in enumerate(values):
            row += f" {val.ljust(col_widths[i]-2)} ┃"
        print(row)

    print("┗" + "┻".join("━" * w for w in col_widths) + "┛")
    print()

def admin_add():
    global root, book_list
    print("\n=== Tambah Buku ===")
    new_id = str(max([int(b.key) for b in book_list], default=0) + 1)
    print(f"ID Buku (otomatis): {new_id}")

    title = get_valid_input("Judul: ")
    author = get_valid_input("Penulis: ")
    year = get_valid_input("Tahun Terbit: ", is_numeric=True)
    category = get_valid_input("Kategori: ")
    stock = get_valid_input("Stok: ", is_numeric=True)
    location = get_valid_input("Lokasi Rak: ")

    book = Book(new_id, title, author, year, category, stock, location)
    book_list.append(book)
    save_books(book_list)
    root = avl.insert(root, book)

    print("Buku berhasil ditambahkan!\n")
    print_books_table(book_list)
    time.sleep(3)


def admin_delete():
    global root, book_list
    print("\n=== Hapus Buku ===")
    if not book_list:
        print("Belum ada buku.\n")
        return
    print_books_table(book_list)
    key = input("\nMasukkan ID Buku (kosongkan untuk batal): ").strip()
    if not key:
        print("Dibatalkan.\n")
        return
    if not any(b.key == key for b in book_list):
        print("Buku tidak ditemukan.\n")
        return

    book_list = [b for b in book_list if b.key != key]
    save_books(book_list)
    root = avl.delete(root, key)
    print(f"Buku dengan ID {key} berhasil dihapus!\n")
    print_books_table(book_list)


def admin_update():
    global root, book_list
    print("\n=== Ubah Data Buku ===")
    if not book_list:
        print("Belum ada buku.\n")
        return
    print_books_table(book_list)
    key = input("\nMasukkan ID Buku yang ingin diubah: ").strip()
    if not key:
        return

    book = next((b for b in book_list if b.key == key), None)
    if not book:
        print("Buku tidak ditemukan.\n")
        return

    print("\n(Tekan Enter jika tidak ingin mengubah field berikut)\n")
    title = get_valid_input(f"Judul baru ({book.title}): ", allow_empty=True) or book.title
    author = get_valid_input(f"Penulis baru ({book.author}): ", allow_empty=True) or book.author
    year_input = get_valid_input(f"Tahun baru ({book.year}): ", allow_empty=True, is_numeric=True)
    year = year_input if year_input else book.year
    category = get_valid_input(f"Kategori baru ({book.category}): ", allow_empty=True) or book.category
    stock_input = get_valid_input(f"Stok baru ({book.stock}): ", allow_empty=True, is_numeric=True)
    stock = int(stock_input) if stock_input else book.stock
    location = get_valid_input(f"Lokasi baru ({book.location}): ", allow_empty=True) or book.location

    # Update
    book.title, book.author, book.year = title, author, year
    book.category, book.stock, book.location = category, stock, location

    save_books(book_list)
    root = avl.delete(root, key)
    root = avl.insert(root, book)

    print("\nData berhasil diubah!\n")
    print_books_table(book_list)
    time.sleep(3)


def admin_show_all():
    print("\n=== Daftar Semua Buku ===")
    print_books_table(book_list) 


def admin_menu():
    while True:
        print_menu("MENU ADMIN", [
            "Lihat Buku",
            "Tambah Buku",
            "Ubah Buku",
            "Hapus Buku",
            "Cari Buku",
            "Logout",
        ])
        pilih = input("Pilih: ")
        if pilih == "1": admin_show_all()
        elif pilih == "2": admin_add()
        elif pilih == "3": admin_update()
        elif pilih == "4": admin_delete()
        elif pilih == "5":
            while True:
                print_menu("CARI BUKU", [
                    "Cari Berdasarkan ID",
                    "Cari Berdasarkan Kata di Judul",
                    "Cari Berdasarkan Rentang ID",
                    "Kembali",
                ])
                sub = input("Pilih: ")
                if sub == "1": search()
                elif sub == "2": search_by_contains()
                elif sub == "3": get_books_in_range()
                elif sub == "4": break
        elif pilih == "6": break
    
def search():
    print("\n=== Cari Buku ===")
    key = input("Masukkan ID Buku: ").strip()

    result = avl.search(root, key)
    if result:
        print_books_table([result])
    else:
        print("Buku tidak ditemukan.\n")

def search_by_contains():
    keyword = input("\nMasukkan kata di judul: ").strip().lower()
    if not keyword:
        print("Kata kunci kosong.\n")
        return
    hasil = [b for b in book_list if keyword in b.title.lower()]
    print_books_table(hasil) if hasil else print("Tidak ditemukan.\n")
    

def get_books_in_range():
    try:
        min_id = int(input("ID minimum: "))
        max_id = int(input("ID maksimum: "))
        hasil = [b for b in book_list if min_id <= int(b.key) <= max_id]
        print_books_table(hasil)
    except:
        print("Input tidak valid.\n")


def borrow_book():
    print("\n=== Pinjam Buku ===")
    if not book_list:
        print("Tidak ada buku.\n")
        return
    print_books_table(book_list)
    key = input("\nMasukkan ID Buku: ").strip()
    book = avl.search(root, key)
    if not book:
        print("Buku tidak ditemukan.\n")
        return
    if book.stock <= 0:
        print("Stok habis.\n")
        return
    book.stock -= 1
    save_books(book_list)
    print(f"Selamat kamu Berhasil meminjam buku {book.title} | Sisa stok saat ini: {book.stock}\n")


def user_menu():
    while True:
        print_menu("MENU PENGUNJUNG", [
            "Lihat Buku", 
            "Cari Buku", 
            "Pinjam Buku", 
            "Keluar"])
        pilih = input("Pilih: ")
        if pilih == "1": admin_show_all()
        elif pilih == "2":
            while True:
                print_menu("CARI BUKU", [
                    "Cari Berdasarkan ID", 
                    "Cari Berdasarkan Kata di Judul", 
                    "Cari Berdasarkan Rentang ID", 
                    "Kembali"])
                sub = input("Pilih: ")
                if sub == "1": search()
                elif sub == "2": search_by_contains()
                elif sub == "3": get_books_in_range()
                elif sub == "4": break
        elif pilih == "3": borrow_book()
        elif pilih == "4": break

if __name__ == "__main__":
    book_list = load_books()
    for b in book_list:
        root = avl.insert(root, b)

    while True:
        print_menu("SELAMAT DATANG DI PERPUSTAKAAN", ["Login", "Register", "Keluar"])
        pilihan = input("Pilih: ")
        if pilihan == "1": login()
        elif pilihan == "2": register()
        elif pilihan == "3": break