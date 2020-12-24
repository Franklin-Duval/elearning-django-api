from django.shortcuts import redirect

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
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

class SubjectViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows subjects to be viewed or modified
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or modified
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows courses to be viewed or modified
    """
    """ authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] """
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ExamViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows exams to be viewed or modified
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows comments to be viewed or modified
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

class InscriptionViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to subscribe to a course
    """
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


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