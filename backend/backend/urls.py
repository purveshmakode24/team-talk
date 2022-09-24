"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views as user_views
from teams import views as team_views
from team_memberships import views as team_membership_views
from topics import views as topic_views
from comments import views as comment_views

router = DefaultRouter()

router.register('auth/register', user_views.UserCreateViewSet,
                basename='user_create_viewset')
router.register('me', user_views.ProfileViewSet,
                basename='profile_viewset')
router.register('users', user_views.UserListUpdateDestroyViewSet,
                basename='user_list__update_destroy_viewset')
router.register('teams', team_views.TeamViewSet,
                basename='team_viewset')
router.register('memberships', team_membership_views.TeamMembershipViewSet,
                basename='team_membership_viewset')
router.register('topics', topic_views.TopicViewSet,
                basename='topic_viewset')
router.register('comments', comment_views.CommentViewSet,
                basename='comment_viewset')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', user_views.CreateTokenView.as_view(), name='token'),
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('docs2/', include_docs_urls(title='My API Title'))
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
