# Generated by Django 3.2.9 on 2021-11-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=40)),
                ('otp', models.IntegerField()),
                ('token', models.CharField(max_length=65)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
