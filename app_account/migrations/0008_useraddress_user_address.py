# Generated by Django 5.0.4 on 2024-07-06 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_account', '0007_remove_user_address_delete_useraddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_address', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ManyToManyField(blank=True, related_name='addresses', to='app_account.useraddress'),
        ),
    ]