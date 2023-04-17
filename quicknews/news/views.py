from django.shortcuts import render

from django.db.models import Q
from django.views.generic import CreateView, DeleteView, ListView, DetailView
from django.views import View
from django.views.generic.list import MultipleObjectMixin
from django.http import Http404
from django.core.cache import cache
from django.core.paginator import InvalidPage
from news.models import NewsItem


class NewsItemListView(ListView):
    model = NewsItem
    queryset = NewsItem.objects.filter(parent__isnull=True).all()
    paginate_by = 12
    template_name = "news/news_item_list.html"


class StoryListView(NewsItemListView):
    queryset = NewsItem.news_types_objects.stories().filter(parent__isnull=True).all()


class CommentListView(NewsItemListView):
    queryset = NewsItem.news_types_objects.comments().filter(parent__isnull=True).all()


class JobListView(NewsItemListView):
    queryset = NewsItem.news_types_objects.jobs().filter(parent__isnull=True).all()


class PollListView(NewsItemListView):
    queryset = NewsItem.news_types_objects.polls().filter(parent__isnull=True).all()


class PollOptionsListView(NewsItemListView):
    queryset = (
        NewsItem.news_types_objects.polloptions().filter(parent__isnull=True).all()
    )


class NewsItemDetailView(DetailView):
    model = NewsItem
    template_name = "news/news_item_detail.html"


class SearchNewsItemView(MultipleObjectMixin, View):
    model = NewsItem
    template_name = "news/news_item_list.html"
    queryset = NewsItem.objects.all()
    paginate_by = 12
    page_kwarg = "page"
    search_kwarg = "q"

    def get(self, request):
        query = request.GET.get(self.search_kwarg, "")
        if not query:
            page_obj = []
        else:
            queryset = NewsItem.objects.filter(
                Q(text__icontains=query) | Q(title__icontains=query)
            ).all()
            page_obj = self.paginate_queryset(
                queryset=queryset, page_size=self.paginate_by, search_query=query
            )
            self.object_list = page_obj

        context = {"page_obj": page_obj}

        return render(
            request=request,
            template_name=self.template_name,
            context=context,
        )

    def paginate_queryset(self, queryset, page_size, search_query):

        """Paginate the queryset"""
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )

        page_kwarg = self.page_kwarg

        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

        try:
            page_number = int(page)

        except ValueError:
            if page == "last":
                page_number = paginator.num_pages

            else:
                raise Http404("Page is not 'last', nor can it be converted to an int.")
        try:
            page = paginator.page(page_number)
            return page

        except InvalidPage as e:
            raise Http404(
                "Invalid page (%(page_number)s): %(message)s"
                % {"page_number": page_number, "message": str(e)}
            )
