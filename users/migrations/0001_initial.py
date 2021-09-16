# Generated by Django 3.2.7 on 2021-09-16 05:20

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='username')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True, verbose_name='phone')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
        ),
    ]
