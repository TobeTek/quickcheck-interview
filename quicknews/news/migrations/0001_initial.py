# Generated by Django 4.1.3 on 2022-11-02 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewsItemModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "hn_id",
                    models.CharField(
                        help_text="HackerNews ID", max_length=10, unique=True
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(
                        default=False, help_text="True if the item is deleted"
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Comment"),
                            (2, "Job"),
                            (3, "Poll"),
                            (4, "Polloption"),
                            (5, "Story"),
                        ],
                        help_text="The type of item. Determines if instance is a `job`, `story`, `comment`, `poll`, or `pollopt`",
                    ),
                ),
                (
                    "by",
                    models.CharField(
                        help_text="Username of the item's author", max_length=200
                    ),
                ),
                (
                    "hn_time_created",
                    models.DateTimeField(
                        help_text="Date item was created on HackerNews"
                    ),
                ),
                (
                    "pulled_at",
                    models.DateTimeField(
                        help_text="Date item was fetched/stored on our platform"
                    ),
                ),
                (
                    "dead",
                    models.BooleanField(
                        default=False, help_text="true if the item is dead."
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, help_text="The comment, story or poll text. HTML"
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, help_text="The URL of the story.", null=True
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="The title of the story, poll or job.",
                        max_length=500,
                    ),
                ),
                (
                    "descendants",
                    models.PositiveIntegerField(
                        help_text="In the case of stories or polls, the total comment count.",
                        null=True,
                    ),
                ),
                (
                    "score",
                    models.PositiveIntegerField(
                        help_text="The story's score, or the votes for a pollopt.",
                        null=True,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        help_text="The item's parent. For comments, either another comment or the relevant story. For pollopts, the relevant poll.                   Reverse relation: The ids of the item's comments, in ranked display order.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kids",
                        to="news.newsitemmodel",
                        to_field="hn_id",
                    ),
                ),
                (
                    "parent_poll",
                    models.ForeignKey(
                        blank=True,
                        help_text="Reverse relation: A list of related pollopts, in display order.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parts",
                        to="news.newsitemmodel",
                        to_field="hn_id",
                    ),
                ),
            ],
            options={
                "verbose_name": "News Item",
                "verbose_name_plural": "News Items",
                "ordering": ["-hn_time_created"],
            },
        ),
        migrations.AddIndex(
            model_name="newsitemmodel",
            index=models.Index(fields=["hn_id"], name="news_newsit_hn_id_1972e0_idx"),
        ),
        migrations.AddIndex(
            model_name="newsitemmodel",
            index=models.Index(
                fields=["hn_time_created"], name="news_newsit_hn_time_a5adfb_idx"
            ),
        ),
        migrations.AddConstraint(
            model_name="newsitemmodel",
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
            model_name="newsitemmodel",
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
            model_name="newsitemmodel",
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
            model_name="newsitemmodel",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 4), _negated=True),
                    models.Q(("score__isnull", False), ("parent__isnull", False)),
                    _connector="OR",
                ),
                name="valid_polloption_fields",
            ),
        ),
        migrations.AddConstraint(
            model_name="newsitemmodel",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("type", 5), _negated=True),
                    models.Q(
                        ("score__isnull", False),
                        ("descendants__isnull", False),
                        ("text__isnull", False),
                        ("title__isnull", False),
                    ),
                    _connector="OR",
                ),
                name="valid_story_fields",
            ),
        ),
    ]