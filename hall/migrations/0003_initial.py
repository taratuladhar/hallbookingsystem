# Generated by Django 4.1.7 on 2023-10-01 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hall', '0002_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_title', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
            ],
        ),
    ]