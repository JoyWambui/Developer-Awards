# Generated by Django 4.0 on 2021-12-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='images/')),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField()),
            ],
        ),
    ]
