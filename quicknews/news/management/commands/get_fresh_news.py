import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from news import services


class Command(BaseCommand):
    help = "Fetch new commands from HackerNews API"

    def add_arguments(self, parser):
        parser.add_argument(
            "-ri",
            "--refresh-interval",
            type=int,
            help="Interval (in minutes) to fetch news",
            default=5,
        )

        parser.add_argument(
            "-nr",
            "--no-records",
            type=int,
            help="No. records to fetch per API request.",
            default=100,
        )

    def handle(self, *args, **options):
        self.stdout.write("Scheduling refresh job")
        settings.SCHEDULER.add_job(
            services.HackerNewsData.get_newstories,
            "interval",
            minutes=options["refresh_interval"],
            max_instances=1,
            args=(options["no_records"],),
            replace_existing=False,
        )
        self.stdout.write(self.style.SUCCESS("Fetching news from HackerNews API"))
        while True:
            self.stdout.write(f"Job List: \n{settings.SCHEDULER.print_jobs()}")
            settings.SCHEDULER
            try:
                pass
            except KeyboardInterrupt:
                self.stdout.write("Shutting down")
