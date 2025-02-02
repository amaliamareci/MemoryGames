# Generated by Django 5.1.5 on 2025-01-16 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_numbers_sequence'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumberSequenceGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Number Sequence', max_length=100)),
                ('description', models.TextField(default='Memorize and click numbers in sequence')),
                ('icon', models.CharField(default='🔢', max_length=50)),
                ('url_path', models.CharField(default='number-sequence', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('current_level', models.IntegerField(default=1)),
                ('card_count', models.IntegerField(default=4)),
                ('numbers_sequence', models.JSONField(default=list)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
