# Generated migration for Django models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=50)),
                ('user', models.CASCADE),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=64, verbose_name='Amount')),
                ('source', models.CharField(max_length=100)),
                ('date_received', models.DateField(verbose_name='Date Received')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('category', models.CASCADE),
                ('user', models.CASCADE),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=64, verbose_name='Amount')),
                ('date_incurred', models.DateField(verbose_name='Date Incurred')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('receipt_image', models.ImageField(blank=True, null=True, upload_to='receipts/', verbose_name='Receipt Image')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('category', models.CASCADE),
                ('user', models.CASCADE),
            ],
        ),
    ]