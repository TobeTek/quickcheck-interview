# Generated by Django 4.0.6 on 2022-11-03 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0003_alter_newsitem_dead"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsitem",
            name="text",
            field=models.TextField(
                blank=True, help_text="The comment, story or poll text. HTML", null=True
            ),
        ),
        migrations.AlterField(
            model_name="newsitem",
            name="title",
            field=models.CharField(
                blank=True,
                help_text="The title of the story, poll or job.",
                max_length=500,
                null=True,
            ),
        ),
    ]
