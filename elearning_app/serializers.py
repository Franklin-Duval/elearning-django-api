from .models import *
from rest_framework import serializers

class ClasseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classe
        fields = [
            'id',
            'name',
            'abbrev',
            'number_courses',
        ]

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'number_courses',
            'description',
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'telephone',
            'type',
            'favoris',
        ]

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'detailImage',
            'video',
            'content',
            'rating',
            'keywords',
            'upload_date',
            'update_date',
            'validated',
            'subject',
            'level',
        ]

class ExamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'id',
            'course',
            'file',
            'correction',
        ]

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'id',
            'user',
            'course',
            'comment',
            'date',
        ]

class InscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inscription
        fields = [
            'id',
            'user',
            'course',
            'date'
        ]