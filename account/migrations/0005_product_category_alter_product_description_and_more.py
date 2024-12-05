# Generated by Django 4.2.16 on 2024-12-05 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_product_category_product_is_featured_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('lunch', 'Lunch'), ('breakfast', 'Breakfast'), ('snacks', 'Snacks'), ('drinks', 'Drinks')], default='lunch', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]