from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0003_alter_funcionario_options_alter_funcionario_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='nome',
            field=models.CharField(default='Funcionário', max_length=100),
        ),
    ] 