class Mahasiswa:
    def __init__(self, id, nim, nama, tanggal_lahir, alamat, jenis_kelamin):
        self.id = id
        self.nim = nim
        self.nama = nama
        self.tanggal_lahir = tanggal_lahir
        self.alamat = alamat
        self.jenis_kelamin = jenis_kelamin

    @staticmethod
    def from_db_row(row):
        return Mahasiswa(
            id=row[0],
            nim=row[1],
            nama=row[2],
            tanggal_lahir=row[3],
            alamat=row[4],
            jenis_kelamin=row[5]
        )

class MataKuliah:
    def __init__(self, id, kode_mk, nama_mk, sks):
        self.id = id
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks

    @staticmethod
    def from_db_row(row):
        return MataKuliah(
            id=row[0],
            kode_mk=row[1],
            nama_mk=row[2],
            sks=row[3]
        )
