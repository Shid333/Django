# Generated by Django 5.0 on 2023-12-23 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_instructor_manager_student_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
