"""
Query Params filters for teams.
"""

from rest_framework import filters
from rest_framework.exceptions import ValidationError


class TopicsByTeamIdFilter(filters.SearchFilter):
    # Shows up in drf docs.
    search_param = 'team_id'
    search_title = 'team_id'
    search_description = '[REQUIRED] get all Topics from the Team by team_id query params.'

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        # Make query_params mandatory for (view.action == list) only.
        if not search_terms and view.action == 'list':
            # return queryset.none()
            raise ValidationError(
                '%s parameter is required!' % self.search_param
            )

        return super().filter_queryset(request, queryset, view)
