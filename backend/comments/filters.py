"""
Query Params filters for comments.
"""

from rest_framework import filters
from rest_framework.exceptions import ValidationError


class CommentsByTopicIdFilter(filters.SearchFilter):
    # Shows up in drf docs.
    search_param = 'topic_id'
    search_title = 'topic_id'
    search_description = '[REQUIRED] get all comments from the Team by topic_id query params.'

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        # Make query_params mandatory for (view.action == list) only.
        if not search_terms and view.action == 'list':
            # return queryset.none()
            raise ValidationError(
                '%s paramter is required!' % self.search_param
            )

        return super().filter_queryset(request, queryset, view)