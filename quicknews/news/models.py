from datetime import datetime
from typing import Any, Union
from typing_extensions import Self

from django.db import models
from django.db.models import Q, UniqueConstraint

from django.utils.functional import cached_property
from zoneinfo import ZoneInfo


class NewsItemTypes(models.IntegerChoices):
    Comment = 1
    Job = 2
    Poll = 3
    PollOption = 4
    Story = 5


class NewsItem(models.Model):
    # id field is automatically created
    hn_id = models.PositiveIntegerField(help_text="HackerNews ID", null=True)
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
        auto_now_add=True,
        help_text="Date item was fetched/stored on our platform",
    )
    dead = models.BooleanField(
        null=True, default=False, help_text="true if the item is dead."
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="kids",
        null=True,
        blank=True,
        help_text="The item's parent. For comments, either another comment or the relevant story. For pollopts, the relevant poll. \
                  Reverse relation: The ids of the item's comments, in ranked display order.",
    )

    text = models.TextField(
        null=True, blank=True, help_text="The comment, story or poll text. HTML"
    )
    url = models.URLField(null=True, blank=True, help_text="The URL of the story.")
    title = models.CharField(
        null=True,
        max_length=500,
        blank=True,
        help_text="The title of the story, poll or job.",
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
        help_text="Reverse relation: A list of related pollopts, in display order.",
        null=True,
        blank=True,
    )

    class TypesManager(models.Manager):
        def get_queryset(self):
            return NewsItem.objects.all()

        def stories(self):
            return self.get_queryset().filter(type=NewsItemTypes.Story)

        def comments(self):
            return self.get_queryset().filter(type=NewsItemTypes.Comment)

        def jobs(self):
            return self.get_queryset().filter(type=NewsItemTypes.Job)

        def polls(self):
            return self.get_queryset().filter(type=NewsItemTypes.Poll)

        def polloptions(self):
            return self.get_queryset().filter(type=NewsItemTypes.PollOption)

    objects = models.Manager()
    news_types_objects = TypesManager()

    class Meta:
        # Constraints
        __comment_constraint = models.CheckConstraint(
            check=(~Q(type=NewsItemTypes.Comment) | Q(text__isnull=False)),
            name="valid_comment_fields",
        )
        __job_constraint = models.CheckConstraint(
            check=(~Q(type=NewsItemTypes.Job) | (Q(title__isnull=False))),
            name="valid_job_fields",
        )

        __poll_constraint = models.CheckConstraint(
            check=((~Q(type=NewsItemTypes.Poll) | Q(descendants__isnull=False))),
            name="valid_poll_fields",
        )
        __polloption_constraint = models.CheckConstraint(
            check=((~Q(type=NewsItemTypes.PollOption) | Q(parent__isnull=False))),
            name="valid_polloption_fields",
        )
        __story_constraint = models.CheckConstraint(
            check=(~Q(type=NewsItemTypes.Story) | Q(title__isnull=False)),
            name="valid_story_fields",
        )

        verbose_name = "News Item"
        verbose_name_plural = "News Items"
        ordering = ["-hn_time_created"]
        constraints = [
            __comment_constraint,
            __job_constraint,
            __poll_constraint,
            __polloption_constraint,
            __story_constraint,
            UniqueConstraint(
                fields=["hn_id"], condition=Q(hn_id__isnull=False), name="unique_hn_id"
            ),
        ]

        indexes = [
            models.Index(fields=["hn_id"]),
            models.Index(fields=["hn_time_created"]),
        ]

    def __str__(self) -> str:
        type_label = NewsItemTypes(self.type).name
        return f"{type_label}: {self.by} {self.title}"

    @property
    def is_story(self):
        return self.type == NewsItemTypes.Story

    @property
    def is_comment(self):
        return self.type == NewsItemTypes.Comment

    @property
    def is_poll(self):
        return self.type == NewsItemTypes.Poll

    @property
    def is_polloption(self):
        return self.type == NewsItemTypes.PollOption

    @property
    def type_label(self):
        return NewsItemTypes(self.type).name

    @classmethod
    def _to_news_item(cls, item_data: dict) -> Self:
        HN_TO_NEWS_ITEM_TYPES = {
            "story": NewsItemTypes.Story,
            "comment": NewsItemTypes.Comment,
            "job": NewsItemTypes.Job,
            "poll": NewsItemTypes.Poll,
            "pollopt": NewsItemTypes.PollOption,
        }
        item_type = HN_TO_NEWS_ITEM_TYPES[item_data["type"]]

        if hn_time_created := item_data.get("time"):
            hn_time_created = datetime.fromtimestamp(
                item_data["time"], tz=ZoneInfo("UTC")
            )
        else:
            hn_time_created = None

        news_item = NewsItem(
            hn_id=item_data["id"],
            deleted=item_data.get("deleted", False),
            type=item_type,
            by=item_data.get("by", ""),
            hn_time_created=hn_time_created,
            dead=item_data.get("dead"),
            text=item_data.get("text"),
            url=item_data.get("url"),
            title=item_data.get("title"),
            descendants=item_data.get("descendants"),
            score=item_data.get("score"),
        )
        return news_item
