# Generated by Django 3.2.3 on 2021-05-24 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_image', models.ImageField(upload_to='post_content_images/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.post')),
            ],
        ),
    ]
