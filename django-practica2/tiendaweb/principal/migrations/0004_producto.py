# Generated by Django 4.2.13 on 2024-06-24 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_cliente_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagen', models.ImageField(upload_to='productos/')),
                ('descripcion', models.TextField()),
            ],
        ),
    ]
