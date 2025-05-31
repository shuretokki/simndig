from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=50)
    angkatan = models.PositiveIntegerField()
    jurusan = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dpa = models.CharField(max_length=100)  
    status = models.CharField(max_length=50)
    semester = models.PositiveIntegerField()
    ipk = models.DecimalField(max_digits=4, decimal_places=2)  
    ukt = models.DecimalField(max_digits=9, decimal_places=2)  

    def __str__(self):
        return f"{self.nama} ({self.nim})"
    
    class Meta:
        abstract = True
    
    def set_nama(self, nama):
        self.nama = nama
        self.save()

    def set_nim(self, nim):
        self.nim = nim
        self.save()

    def set_kelas(self, kelas):
        self.kelas = kelas
        self.save()

    def set_angkatan(self, angkatan):
        self.angkatan = angkatan
        self.save()

    def set_jurusan(self, jurusan):
        self.jurusan = jurusan
        self.save()

    def set_email(self, email):
        self.email = email
        self.save()

    def set_dpa(self, dpa):
        self.dpa = dpa
        self.save()

    def set_status(self, status):
        self.status = status
        self.save()

    def set_semester(self, semester):
        self.semester = semester
        self.save()

    def set_ipk(self, ipk):
        self.ipk = ipk
        self.save()

    def set_ukt(self, ukt):
        self.ukt = ukt
        self.save()

    
    def get_nama(self):
        return self.nama

    def get_nim(self):
        return self.nim

    def get_kelas(self):
        return self.kelas

    def get_angkatan(self):
        return self.angkatan

    def get_jurusan(self):
        return self.jurusan

    def get_email(self):
        return self.email

    def get_dpa(self):
        return self.dpa

    def get_status(self):
        return self.status

    def get_semester(self):
        return self.semester

    def get_ipk(self):
        return self.ipk

    def get_ukt(self):
        return self.ukt

   
    def ambilKelas(self):
        
        return ["Matematika", "Fisika", "Pemrograman", "Basis Data", "PBO"]

    def absen(self):
        
        return 92.5  
    
    def KHS(self):
       
        return {
            "Matematika": "A",
            "Fisika": "B+",
            "Pemrograman": "A-",
            "Basis Data": "B",
        }

    def bayar_ukt(self):
        
        return 2500000.00

    def lunas_ukt(self):
        
        return self.bayar_ukt() >= self.ukt
    
class Mahasiswa(Student):
    pass
class Dosen(Student):
    pass
class Atmin(Student):
    pass 
