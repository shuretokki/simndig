# Generated by Django 5.2.1 on 2025-05-31 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matakuliah', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kelaswajib',
            name='matakuliah_ptr',
        ),
        migrations.RemoveField(
            model_name='kelaswajib',
            name='prasyarat',
        ),
        migrations.RemoveField(
            model_name='matakuliah',
            name='_nim',
        ),
        migrations.RemoveField(
            model_name='matakuliah',
            name='email',
        ),
        migrations.DeleteModel(
            name='KelasPilihan',
        ),
        migrations.DeleteModel(
            name='KelasWajib',
        ),
    ]
