# Generated by Django 5.1.6 on 2025-02-13 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0004_alter_category_options_contact_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='Category',
            new_name='category',
        ),
    ]
