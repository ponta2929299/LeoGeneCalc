# Generated by Django 5.1.6 on 2025-02-17 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene_type', models.CharField(choices=[('D', '顕性'), ('C', '共顕性'), ('R', '潜性')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Morph',
            fields=[
                ('morph_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('morph_detail', models.TextField()),
                ('gene_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='morph.gene')),
            ],
        ),
    ]
