# Generated by Django 5.2.1 on 2025-05-31 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadiri', '0002_dosen_nip_dosen_tanggal_mulai_kerja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atmin',
            name='angkatan',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='dpa',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='ipk',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='jurusan',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='kelas',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='atmin',
            name='ukt',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='angkatan',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='dpa',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='ipk',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='jurusan',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='kelas',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='dosen',
            name='ukt',
        ),
    ]
