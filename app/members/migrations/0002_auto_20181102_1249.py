# Generated by Django 2.1.3 on 2018-11-02 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='user', verbose_name='프로필 이미지'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, verbose_name='이름'),
        ),
        migrations.AlterField(
            model_name='user',
            name='site',
            field=models.URLField(blank=True, max_length=150, verbose_name='사이트'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='아이디'),
        ),
    ]
