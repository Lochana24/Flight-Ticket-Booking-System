# Generated by Django 4.0.6 on 2022-08-18 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='deleted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ticket',
            name='email',
            field=models.EmailField(default='youremail@namespace.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
