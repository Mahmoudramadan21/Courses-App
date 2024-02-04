from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@api_view(['GET'])  # user
@permission_classes([IsAuthenticated])
def getCourses(request):
    try:
        query = request.query_params.get('q')
        if query is None:
            query = ''

        courses = Course.objects.filter(
            title__icontains=query).order_by('-created_at')

        page = request.query_params.get('page')
        paginator = Paginator(courses, 4)

        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        serializer = CourseSerializer(courses, many=True)
        return Response({'courses': serializer.data,
                         'page': page, 'pages': paginator.num_pages})

    except:
        return Response('Unexpected error')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCourse(request, pk):
    try:
        user = request.user
        course = get_object_or_404(Course, pk=pk)

        # Assuming the field name is numOfViews, update the following line
        View.objects.create(_user_id=user, _course_id=course)

        course.watches += 1
        course.save()

        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)

    except:
        return Response('Unexpected error')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getCourseSubscribers(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        subscribers = course.user_id.all()  # احصل على جميع المشتركين في الدورة
        serializer = UserSerializer(subscribers, many=True)
        return Response(serializer.data)
    except:
        return Response('Unexpected error')


@api_view(['POST']) #Admin
@permission_classes([IsAdminUser])
def createCourse(request):
    try:
        data = request.data
        user = request.user

        course = Course.objects.create(
            user = user,
            title = data['title'],
            description = data['description'],
            image = request.FILES.get('image'),
        )

        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)

    except:
        return Response('Unexpected error')

# @api_view(['POST']) #Admin
# @permission_classes([IsAdminUser])
# def uploadImage(request):
#     data = request.data

#     lecture = data['course_id']
#     lecture = Lecture.objects.get(pk=course_id)

#     lecture.video = request.FILES.get('image')
#     lecture.save()

#     return Response('Image was uploaded')

@api_view(['PUT']) #Admin
@permission_classes([IsAdminUser])
def updateCourse(request, pk):
    try:
        data = request.data
        course = get_object_or_404(Course, pk=pk)

        course.title = data['title']
        course.description = data['description']
        course.image = request.FILES.get('image')

        course.save()
        serializer = CourseSerializer(course, many=False)
        return Response(serializer.data)
    except:
        return Response('Unexpected error')

@api_view(['DELETE']) #Admin
@permission_classes([IsAdminUser])
def deleteCourse(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response({'detail': 'Course deleted successfully'})
    except:
        return Response('Unexpected error')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likeCourse(request, course_id):
    try:
        user = request.user
        course = get_object_or_404(Course, pk=course_id)

        # التحقق مما إذا كان المستخدم قد قام بالفعل بالإعجاب بالدورة
        like_exists = Like.objects.filter(user_id=user, course_id=course).exists()

        if like_exists:
            return Response({'detail': 'You already liked this course'}, status=400)

        # إضافة إعجاب جديد
        like = Like.objects.create(user_id=user, course_id=course)

        # تحديث numOfLikes في الدورة
        course.numOfLikes += 1
        course.save()

        return Response({'detail': 'Course liked successfully'})
    except:
        return Response('Unexpected error')

####################################################################

@api_view(['POST']) #Admin
@permission_classes([IsAdminUser])
def createLecture(request, course_id):
    try:
        data = request.data
        course = get_object_or_404(Course, pk=course_id)

        lecture = Lecture.objects.create(
            course_id = course,
            title = data['title'],
            notes = data['notes'],
            video = request.FILES.get('video'),
        )

        serializer = LectureSerializer(lecture, many=False)
        return Response(serializer.data)
    except:
        return Response('Unexpected error')


# @api_view(['POST']) #Admin
# @permission_classes([IsAdminUser])
# def uploadVideo(request):
#     data = request.data

#     lecture = data['lecture_id']
#     lecture = Lecture.objects.get(pk=lecture_id)

#     lecture.video = request.FILES.get('video')
#     lecture.save()

#     return Response('Video was uploaded')

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateLecture(request, course_id, lecture_id):
    try:
        data = request.data
        lecture = get_object_or_404(Lecture, pk=lecture_id)

        lecture.title = data['title']
        lecture.notes = data['notes']
        lecture.video = request.FILES.get('video')

        lecture.save()
        serializer = LectureSerializer(lecture, many=False)
        return Response(serializer.data)
    except:
        return Response('Unexpected error')

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteLecture(request, course_id, lecture_id):
    try:
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        lecture.delete()
        return Response({'detail': 'Lecture deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response('Unexpected error')

#####################################################################

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create(
            first_name=data['first-name'],
            last_name=data['last-name'],
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email or username already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        return Response('Unexpected error')



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)

        data = request.data
        user.first_name = data['first-name']
        user.last_name = data['last-name']
        user.username = data['username']
        user.email = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

        return Response(serializer.data)

    except:
        return Response('Unexpected error')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    except:
        return Response('Unexpected error')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    try:
        user = User.objects.get(id=pk)

        data = request.data

        user.first_name = data['first-name']
        user.last_name = data['last-name']
        user.username = data['username']
        user.email = data['email']
        user.is_staff = data['isAdmin']

        user.save()

        serializer = UserSerializer(user, many=False)

        return Response(serializer.data)
    except:
        return Response('Unexpected error')


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    try:
        userForDeletion = User.objects.get(id=pk)
        userForDeletion.delete()
        return Response('User was deleted')

    except:
        return Response('Unexpected error')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyCourses(request):
    try:
        user = request.user
        courses = Course.objects.filter(user_id=user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    except:
        return Response('Unexpected error')
