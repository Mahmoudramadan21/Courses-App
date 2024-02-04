from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.getCourses, name='courses'), #Authenticated
    path('course/<int:pk>/', views.getCourse, name='course'), #Authenticated
    path('course/<int:pk>/subscribers/', views.getCourseSubscribers,
            name='course-subsribers'), #Admin

    path('course/create/', views.createCourse, name='create-course'), #Admin
    path('course/<int:pk>/update/', views.updateCourse, name='edit-course'), #Admin
    path('course/<int:pk>/delete/', views.deleteCourse, name='delete-course'), #Admin
    path('course/<int:course_id>/like/', views.likeCourse, name='like-course'),


    path('course/<int:course_id>/createlecture/', views.createLecture,
            name='create-lecture'), #Admin
    path('course/<int:course_id>/lecture/<int:lecture_id>/update/',
        views.updateLecture, name='update-lecture'), #Admin
    path('course/<int:course_id>/lecture/<int:lecture_id>/delete/',
        views.deleteLecture, name='delete-lecture'), #Admin

    # path('course/image/upload/', views.uploadImage, name='upload-Image'), #Admin
    # path('lecture/video/upload/', views.uploadVideo, name='upload-video'), #Admin

    path('users/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'), #Authenticated

    path('users/register/', views.registerUser, name='register'), #Authenticated

    path('users/profile/', views.getUserProfile, name="user-profile"), #Authenticated
    path('users/profile/update/', views.updateUserProfile,
        name="user-profile-update"), #Authenticated
    path('users/profile/mycourses/', views.getMyCourses,
        name="user-courses"), #Authenticated

    path('users/', views.getUsers, name="users"), #Admin
    path('users/<int:pk>/update/', views.updateUser, name='user-update'), #Admin
    path('users/<int:pk>/delete/', views.deleteUser, name='user-delete'), #Admin
]