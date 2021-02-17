from django.shortcuts import redirect

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *

# Create your views here.
class ClasseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows classes to be viewed or modified
    """
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'abbrev']
    search_fields = ['name', 'abbrev']

class SubjectViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows subjects to be viewed or modified
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['name', 'description']
    search_fields = ['name', 'description']

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or modified
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['email', 'username', 'first_name', 'last_name', 'date_joined', 'telephone', 'type']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'date_joined', 'telephone', 'type', 'favoris']

    def create(self, request, *args, **kwargs):

        user = Users.objects.create(
            email = request.data["email"],
            username = request.data["username"],
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            telephone = request.data["telephone"],
            type = request.data["type"],
            favoris = request.data["favoris"],
        )
        user.set_password(request.data["password"])
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows courses to be viewed or modified
    """    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['title', 'keywords', 'upload_date', 'update_date', 'validated', 'subject', 'level', 'author']
    search_fields = ['title', 'keywords', 'upload_date', 'update_date', 'validated', 'subject__name', 'subject__description', 'level__name', 'level__abbrev', 'author__first_name', 'author__last_name']


class ExamViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows exams to be viewed or modified
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'course__id', 'course__title', 'course__keywords']


class CommentViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows comments to be viewed or modified
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name', 'comment', 'date', 'course__title']

class InscriptionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to subscribe to a course
    """
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


@api_view(['GET'])
def getFreeCourses(request):
    """
        API endpoint to allow users get 5 free courses
    """
    courses = Course.objects.all()
    courses = courses[: 5]

    serializer_context = {
        'request': request,
    }

    serializer = CourseSerializer(courses, many=True, context=serializer_context)
    result = {
        "status" : "SUCCESS",
        "result" : serializer.data
    }
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCommentCourse(request, pk):
    """
        API endpoint to get comments of a Course
    """
    course = Course.objects.get(id = pk)
    comments = Comments.objects.filter(course = course)

    serializer_context = {
        'request': request,
    }

    serializer = CommentSerializer(comments, many=True, context=serializer_context)
    result = {
        "status" : "SUCCESS",
        "result" : serializer.data
    }
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getExamCourse(request, pk):
    """
        API endpoint to get exams of a Course
    """
    course = Course.objects.get(id = pk)
    exams = Exam.objects.filter(course = course)

    serializer_context = {
        'request': request,
    }

    serializer = ExamSerializer(exams, many=True, context=serializer_context)
    result = {
        "status" : "SUCCESS",
        "result" : serializer.data
    }
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCourses(request):
    """
        API endpoint to all validated courses of the platform
    """
    course = Course.objects.filter(validated = True)

    serializer_context = {
        'request': request,
    }

    serializer = CourseSerializer(course, many=True, context=serializer_context)
    serialize_course = serializer.data

    for course in serialize_course:
        
        if course["author"]:
            author = course["author"]
            id = author[author.find('user')+4: ]
            id = int(id.replace("/", ""))

            author = Users.objects.get(id = id)
            serializer_author = UserSerializer(author)

            course["author"] = serializer_author.data

        if course["level"]:
            level = course["level"]
            id = level[level.find('classe')+6: ]
            id = int(id.replace("/", ""))

            level = Classe.objects.get(id = id)
            serializer_level = ClasseSerializer(level)

            course["level"] = serializer_level.data
        
        if course["subject"]:
            subject = course["subject"]
            id = subject[subject.find('subject')+7: ]
            id = int(id.replace("/", ""))

            subject = Subject.objects.get(id = id)
            serializer_subject = SubjectSerializer(subject)

            course["subject"] = serializer_subject.data
        
    result = {
        "status" : "SUCCESS",
        "count": len(serialize_course),
        "result" : serialize_course
    }
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCourse(request, pk):
    """
        API endpoint to a particular course of the platform
    """
    course = None
    try:
        course = Course.objects.get(id = pk, validated = True)
    except:
        result = {
            "status": "FAILURE",
            "message": "No corresponding course"
        }
        return Response(result, status=status.HTTP_200_OK)

    serializer_context = {
        'request': request,
    }

    serializer = CourseSerializer(course, context=serializer_context)
    serialize_course = serializer.data
        
    if serialize_course["author"]:
        author = serialize_course["author"]
        id = author[author.find('user')+4: ]
        id = int(id.replace("/", ""))

        author = Users.objects.get(id = id)
        serializer_author = UserSerializer(author)

        serialize_course["author"] = serializer_author.data

    if serialize_course["level"]:
        level = serialize_course["level"]
        id = level[level.find('classe')+6: ]
        id = int(id.replace("/", ""))

        level = Classe.objects.get(id = id)
        serializer_level = ClasseSerializer(level)

        serialize_course["level"] = serializer_level.data
    
    if serialize_course["subject"]:
        subject = serialize_course["subject"]
        id = subject[subject.find('subject')+7: ]
        id = int(id.replace("/", ""))

        subject = Subject.objects.get(id = id)
        serializer_subject = SubjectSerializer(subject)

        serialize_course["subject"] = serializer_subject.data
        
    result = {
        "status" : "SUCCESS",
        "result" : serialize_course
    }
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def errorPage(request):
    
    result = {
        "code": "HTTP_404_NOT_FOUND",
        "status": "Page not found",
        "message": "Vérifiez votre URL"
    }

    return Response(result, status=status.HTTP_404_NOT_FOUND)


def root(request):
    return redirect('/api')