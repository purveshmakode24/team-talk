"""
Query Params filters for teams.
"""

from rest_framework import filters


class TeamOwnerFilter(filters.SearchFilter):
    # Shows up in drf docs.
    search_param = 'user_id'
    search_title = 'user_id'
    search_description = '[OPTIONAL] get all teams by user_id(owner) query params.\
        membership_status will be of authenticated user only.'

