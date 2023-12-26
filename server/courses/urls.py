from django.urls import path

from . import views

urlpatterns = [
    path('sectors/', views.SectorsHomeView.as_view(), name='sectors_home'),
    path('detail/<uuid:course_uuid>/',
         views.CourseDetail.as_view(), name='course_detail'),
    path('sectors/<uuid:sector_uuid>/',
         views.SectorCourse.as_view(), name='sector_course'),
    path('search/<str:search_term>/',
         views.SearchCourse.as_view(), name='search_course'),
    path('course-study/<uuid:course_uuid>/',
         views.CourseStudy.as_view(), name='course_study'),
    path('add-comment/<uuid:course_uuid>/',
         views.AddComment.as_view(), name='add_comment'),
    path('cart/',
         views.GetCartDetail.as_view(), name='get_cart_detail'),
]
