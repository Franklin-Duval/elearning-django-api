# Generated by Django 3.1.2 on 2020-12-24 06:44

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('abbrev', models.CharField(max_length=5, unique=True)),
                ('number_courses', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('detailImage', models.ImageField(null=True, upload_to='images/')),
                ('video', models.FileField(null=True, upload_to='videos/')),
                ('content', models.FileField(null=True, upload_to='contents/')),
                ('rating', models.IntegerField(default=0)),
                ('keywords', models.TextField(null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField(default=False)),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elearning_app.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('number_courses', models.IntegerField(default=0)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('telephone', models.CharField(max_length=20, unique=True)),
                ('type', models.IntegerField(choices=[(1, 'Elève'), (2, 'Enseignant')])),
                ('favoris', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='exams/')),
                ('correction', models.FileField(upload_to='corrections/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning_app.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elearning_app.subject'),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning_app.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearning_app.users')),
            ],
        ),
    ]
