# Generated by Django 3.0.6 on 2020-05-25 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20200524_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCategoryRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.ClientCategory')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Cliente')),
            ],
        ),
    ]
