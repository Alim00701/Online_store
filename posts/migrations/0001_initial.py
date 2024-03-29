# Generated by Django 4.1.4 on 2022-12-15 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('created_date', models.DateField(auto_now=True)),
                ('modified_date', models.DateField(auto_now_add=True)),
                ('rate', models.FloatField()),
            ],
        ),
    ]
