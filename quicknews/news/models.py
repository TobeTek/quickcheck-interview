from django.db import models
from django.db.models import Q


class NewsItemTypes(models.IntegerChoices):
    Comment = 1
    Job = 2
    Poll = 3
    PollOption = 4
    Story = 5


class NewsItemModel(models.Model):
    # id field is automatically created
    hn_id = models.CharField(max_length=10, help_text="HackerNews ID", unique=True)
    deleted = models.BooleanField(
        default=False, help_text="True if the item is deleted"
    )
    type = models.PositiveSmallIntegerField(
        choices=NewsItemTypes.choices,
        help_text="The type of item. Determines if instance is a `job`, `story`, `comment`, `poll`, or `pollopt`",
    )
    by = models.CharField(max_length=200, help_text="Username of the item's author")
    hn_time_created = models.DateTimeField(
        help_text="Date item was created on HackerNews"
    )
    pulled_at = models.DateTimeField(
        help_text="Date item was fetched/stored on our platform"
    )
    dead = models.BooleanField(default=False, help_text="true if the item is dead.")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="kids",
        null=True,
        blank=True,
        help_text="The item's parent. For comments, either another comment or the relevant story. For pollopts, the relevant poll. \
                  Reverse relation: The ids of the item's comments, in ranked display order.",
        to_field="hn_id",
    )

    text = models.TextField(
        blank=True, help_text="The comment, story or poll text. HTML"
    )
    url = models.URLField(null=True, blank=True, help_text="The URL of the story.")
    title = models.CharField(
        max_length=500, blank=True, help_text="The title of the story, poll or job."
    )

    descendants = models.PositiveIntegerField(
        null=True, help_text="In the case of stories or polls, the total comment count."
    )
    score = models.PositiveIntegerField(
        null=True, help_text="The story's score, or the votes for a pollopt."
    )

    parent_poll = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="parts",
        to_field="hn_id",
        help_text="Reverse relation: A list of related pollopts, in display order.",
        null=True,
        blank=True,
    )

    class Meta:
        # Constraints
        comment_constraint = models.CheckConstraint(
            check=~Q(type=NewsItemTypes.Comment)
            | (Q(parent__isnull=False) & Q(text__isnull=False)),
            name="valid_comment_fields",
        )
        job_constraint = models.CheckConstraint(
            check=~Q(type=NewsItemTypes.Job)
            | (Q(text__isnull=False) & Q(url__isnull=False) & Q(title__isnull=False)),
            name="valid_job_fields",
        )

        poll_constraint = models.CheckConstraint(
            check=~Q(type=NewsItemTypes.Poll)
            | (
                Q(score__isnull=False)
                & Q(descendants__isnull=False)
                & Q(text__isnull=False)
                & Q(title__isnull=False)
            ),
            name="valid_poll_fields",
        )
        polloption_constraint = models.CheckConstraint(
            check=~Q(type=NewsItemTypes.PollOption)
            | (Q(score__isnull=False) & Q(parent__isnull=False)),
            name="valid_polloption_fields",
        )
        story_constraint = models.CheckConstraint(
            check=~Q(type=NewsItemTypes.Story)
            | (
                Q(score__isnull=False)
                & Q(descendants__isnull=False)
                & Q(text__isnull=False)
                & Q(title__isnull=False)
            ),
            name="valid_story_fields",
        )

        verbose_name = "News Item"
        verbose_name_plural = "News Items"
        ordering = ["-hn_time_created"]
        constraints = [
            comment_constraint,
            job_constraint,
            poll_constraint,
            polloption_constraint,
            story_constraint,
        ]
        indexes = [
            models.Index(fields=["hn_id"]),
            models.Index(fields=["hn_time_created"]),
        ]
