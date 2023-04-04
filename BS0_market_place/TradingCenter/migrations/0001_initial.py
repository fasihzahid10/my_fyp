# Generated by Django 3.2.5 on 2021-08-03 03:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, unique=True)),
                ('location', models.TextField()),
                ('description', models.TextField()),
                ('long_description', models.TextField(null=True)),
                ('bannar', models.ImageField(upload_to='image')),
                ('total_rating', models.IntegerField(default=0)),
                ('logo', models.ImageField(upload_to='image')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='check_out',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('amount_pay', models.IntegerField()),
                ('total_bill', models.IntegerField()),
                ('mssid', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='finantial_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('commited_balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='inventory_managment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('long_description', models.TextField(null=True)),
                ('pic', models.ImageField(upload_to='image')),
                ('name', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('total_rating', models.IntegerField(default=0)),
                ('seconds_spends_on_product', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('brands_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.brand')),
            ],
        ),
        migrations.CreateModel(
            name='inventory_orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_order', models.DateTimeField(auto_now=True)),
                ('commited_amount', models.IntegerField()),
                ('amount_buy', models.IntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('is_commited_by_customer', models.BooleanField(default=False)),
                ('is_commited_by_owner', models.BooleanField(default=False)),
                ('is_commited_by_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_finantial_transaction', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
                ('buyers_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.customer')),
                ('check_out', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.check_out')),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.inventory_managment')),
            ],
        ),
        migrations.CreateModel(
            name='request_on_sevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.customer')),
            ],
        ),
        migrations.CreateModel(
            name='sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35, unique=True)),
                ('location', models.TextField()),
                ('description', models.TextField()),
                ('profit_on_brand', models.FloatField()),
                ('type_of_manager_allowed', models.CharField(choices=[('all', 'all'), ('inventory', 'inventory'), ('software', 'software'), ('service', 'service')], default='all', max_length=20)),
                ('total_rating', models.IntegerField(default=0)),
                ('commit_allowed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='services_form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_title', models.CharField(max_length=100)),
                ('background', models.TextField()),
                ('demands', models.TextField()),
                ('first_link_of_inspiration', models.URLField(null=True)),
                ('second_link_of_inspiration', models.URLField(null=True)),
                ('third_link_of_inspiration', models.URLField(null=True)),
                ('completion_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='software_manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('long_description', models.TextField(null=True)),
                ('pic', models.ImageField(upload_to='image')),
                ('name', models.CharField(max_length=30)),
                ('selling_price', models.IntegerField()),
                ('product_url', models.URLField()),
                ('total_rating', models.IntegerField(default=0)),
                ('seconds_spends_on_product', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('brands_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.brand')),
            ],
        ),
        migrations.CreateModel(
            name='software_relations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first', to='TradingCenter.software_manager')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second', to='TradingCenter.software_manager')),
            ],
        ),
        migrations.CreateModel(
            name='software_orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_order', models.DateTimeField(auto_now=True)),
                ('commited_amount', models.IntegerField()),
                ('url', models.URLField()),
                ('is_complete', models.BooleanField(default=False)),
                ('is_commited_by_customer', models.BooleanField(default=False)),
                ('is_commited_by_owner', models.BooleanField(default=False)),
                ('is_commited_by_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
                ('is_finantial_transaction', models.BooleanField(default=False)),
                ('buyers_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.customer')),
                ('check_out', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.check_out')),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.software_manager')),
            ],
        ),
        migrations.CreateModel(
            name='software_featurers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('ref_url', models.URLField(null=True)),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.software_manager')),
            ],
        ),
        migrations.CreateModel(
            name='services_manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('long_description', models.TextField(null=True)),
                ('pic', models.ImageField(upload_to='image')),
                ('name', models.CharField(max_length=30)),
                ('package_price', models.IntegerField()),
                ('total_rating', models.IntegerField(default=0)),
                ('seconds_spends_on_product', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('brands_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.brand')),
            ],
        ),
        migrations.CreateModel(
            name='service_relations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first', to='TradingCenter.services_manager')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second', to='TradingCenter.services_manager')),
            ],
        ),
        migrations.CreateModel(
            name='service_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_order', models.DateTimeField(auto_now=True)),
                ('commited_amount', models.IntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('is_commited_by_customer', models.BooleanField(default=False)),
                ('is_commited_by_owner', models.BooleanField(default=False)),
                ('is_commited_by_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_finantial_transaction', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
                ('check_out', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.check_out')),
                ('request_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.request_on_sevice')),
            ],
        ),
        migrations.CreateModel(
            name='service_featurers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('ref_url', models.URLField(null=True)),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.software_manager')),
            ],
        ),
        migrations.AddField(
            model_name='request_on_sevice',
            name='form',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.services_form'),
        ),
        migrations.AddField(
            model_name='request_on_sevice',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.services_manager'),
        ),
        migrations.CreateModel(
            name='report_on_software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('report', models.TextField()),
                ('rollback_url', models.URLField(null=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.software_orders')),
            ],
        ),
        migrations.CreateModel(
            name='report_on_service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('report', models.TextField()),
                ('rollback_url', models.URLField(null=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.service_order')),
            ],
        ),
        migrations.CreateModel(
            name='report_on_inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('report', models.TextField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.inventory_orders')),
            ],
        ),
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revived', models.BooleanField(default=False)),
                ('msg', models.TextField()),
                ('subject', models.CharField(max_length=100, null=True)),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to='TradingCenter.customer')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='TradingCenter.customer')),
            ],
        ),
        migrations.CreateModel(
            name='inventory_relations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first', to='TradingCenter.inventory_managment')),
                ('second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second', to='TradingCenter.inventory_managment')),
            ],
        ),
        migrations.CreateModel(
            name='inventory_items_featurers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('ref_url', models.URLField(null=True)),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.inventory_managment')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='customers_account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.finantial_account'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='comment_on_software_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)])),
                ('comment', models.TextField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.software_orders')),
            ],
        ),
        migrations.CreateModel(
            name='comment_on_service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)])),
                ('comment', models.TextField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.service_order')),
            ],
        ),
        migrations.CreateModel(
            name='comment_on_inventory_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)])),
                ('comment', models.TextField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.inventory_orders')),
            ],
        ),
        migrations.AddField(
            model_name='check_out',
            name='cust',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.customer'),
        ),
        migrations.AddField(
            model_name='brand',
            name='brand_sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.sector'),
        ),
        migrations.AddField(
            model_name='brand',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TradingCenter.customer'),
        ),
    ]
