import logging
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models import Q  # for queries
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueValidator

from .models import InterviewSchedule, InterviewTimeslot, UserProfile

logger = logging.getLogger(__name__)



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id','user_id','name','email','designation','is_interviewer']


class InterviewerSerializer(serializers.ModelSerializer):
    user = SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        try:
            if obj.user:
                data = {
                    "id": obj.user.id,
                    "user_id": obj.user.user_id,
                    "name": obj.user.name,
                    "email": obj.user.email,
                    "designation": obj.user.designation,
                    "is_interviewer": obj.user.is_interviewer,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Exception occuring while getting analytics_effectiveness  %s",
                exception,
            )
            return None

    class Meta:
        model = InterviewTimeslot
        fields = "__all__"

class ScheduledInterviewerSerializer(serializers.ModelSerializer):
    candidate = SerializerMethodField(read_only=True)
    interviewers = SerializerMethodField(read_only=True)
    
    def get_candidate(self, obj):
        try:
            if obj.candidate:
                data = {
                    "id": obj.candidate.id,
                    "user_id": obj.candidate.user_id,
                    "name": obj.candidate.name,
                    "email": obj.candidate.email,
                    "designation": obj.candidate.designation,
                    "is_interviewer": obj.candidate.is_interviewer,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Exception occuring while getting analytics_effectiveness  %s",
                exception,
            )
            return None

    def get_interviewers(self, obj):
        try:
            if obj.interviewers:
                data = {
                    "id": obj.interviewers.id,
                    "user_id": obj.interviewers.user_id,
                    "name": obj.interviewers.name,
                    "email": obj.interviewers.email,
                    "designation": obj.interviewers.designation,
                    "is_interviewer": obj.interviewers.is_interviewer,
                }
                return data
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Exception occuring while getting analytics_effectiveness  %s",
                exception,
            )
            return None


    class Meta:
        model = InterviewSchedule
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    email = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in email:
            user = UserProfile.objects.filter(
                Q(email=email) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("UserProfile credentials are not correct.")
            user = UserProfile.objects.get(email=email)
        else:
            user = UserProfile.objects.filter(
                Q(email=email) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("UserProfile credentials are not correct.")
            user = UserProfile.objects.get(email=email)
        if user.if_logged:
            raise ValidationError("UserProfile already logged in.")
        user.if_logged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = UserProfile
        fields = (
            'email',
            'password',
            'token'

        )

        read_only_fields = (
            'token',
        )


class LogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        user = None
        try:
            user = UserProfile.objects.get(token=token)
            if not user.if_logged:
                raise ValidationError("UserProfile is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.if_logged = False
        user.token = ""
        user.save()
        data['status'] = "UserProfile is logged out."
        return data

    class Meta:
        model = UserProfile
        fields = (
            'token'
            
        )
