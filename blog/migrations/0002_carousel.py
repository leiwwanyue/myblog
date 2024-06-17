# Generated by Django 5.0.6 on 2024-05-29 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='carousel_images/')),
                ('link', models.URLField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
