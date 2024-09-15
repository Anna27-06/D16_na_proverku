from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, UserResponseView, UserResponseList, UserresponseDelete, \
    response_status_update

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('userresponses/', UserResponseList.as_view(), name='userresponses'),
    path('<int:pk>/userresponse/', UserResponseView.as_view(), name='userresponse'),
    path('<int:pk>/userresponse/delete/', UserresponseDelete.as_view(), name='userresponse_delete'),
    path('<int:pk>/userresponse/accept/', response_status_update, name='userresponse_accept'),

]

