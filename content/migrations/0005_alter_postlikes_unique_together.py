# Generated by Django 4.2.3 on 2023-09-09 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_postlikes_postcomments'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postlikes',
            unique_together={('post', 'liked_by')},
        ),
    ]
