# Generated by Django 4.0.6 on 2022-11-03 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0005_remove_newsitem_valid_comment_fields_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="newsitem",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 1), _negated=True),
                    models.Q(("parent__isnull", False), ("text__isnull", False)),
                    _connector="OR",
                ),
                name="valid_comment_fields",
            ),
        ),
        migrations.AddConstraint(
            model_name="newsitem",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 2), _negated=True),
                    models.Q(
                        ("text__isnull", False),
                        ("url__isnull", False),
                        ("title__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="valid_job_fields",
            ),
        ),
        migrations.AddConstraint(
            model_name="newsitem",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 3), _negated=True),
                    models.Q(
                        ("score__isnull", False),
                        ("descendants__isnull", False),
                        ("text__isnull", False),
                        ("title__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="valid_poll_fields",
            ),
        ),
        migrations.AddConstraint(
            model_name="newsitem",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 4), _negated=True),
                    models.Q(("score__isnull", False), ("parent__isnull", False)),
                    _connector="OR",
                ),
                name="valid_polloption_fields",
            ),
        ),
    ]