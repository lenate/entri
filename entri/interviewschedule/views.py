import logging
from datetime import datetime, timedelta

# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .functions import gen_object_id
from .models import *
from .models import UserProfile
from .serializers import *

logger = logging.getLogger('main')

# Create your views here.


class Login(generics.GenericAPIView):
    # get method handler
    queryset = UserProfile.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = LoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = LogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class CandidateandInterviewerAvailabilityAddEntryView(CreateAPIView):

    """
    candidate and interviewer availability add entry view
    if is_interviewer is true then interviewer is added else candidate is added

    """
    
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                if self.request.data.get('is_interviewer') is True:
                    serializer.save(object_id=gen_object_id(UserProfile),is_interviewer=True)
                    message="Interviewer added successfully"
                else:
                    serializer.save(object_id=gen_object_id(UserProfile),is_interviewer=False)
                    message="Candidate added successfully"

                
                data["status"] = "success"
                data["message"] = message
                data["code"] = 201
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "Failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "Failed"
            data["message"] = "something went wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class UserListView(ListAPIView):

    """
    candidate and interviewer list view handled dynamically by pass query param user_type

    """

    serializer_class = InterviewerSerializer

    def get_queryset(self, *args, **kwargs):
        user_type=self.request.GET.get("user_type")
        if user_type=="candidate":
            queryset_list=InterviewTimeslot.objects.filter(user__is_interviewer=False).all()
        else:
            queryset_list=InterviewTimeslot.objects.filter(user__is_interviewer=True).all()
       
        return queryset_list


class AllEntriUserProfileListView(ListAPIView):

    """
    all candidates and interviewer list view

    """

    serializer_class = UserProfileSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list=UserProfile.objects.order_by("-id")
        return queryset_list




class InterviewSlotEntryAddView(CreateAPIView):

    """
    candidate/interviewer availability add time entry view

    """
    queryset =  UserProfile.objects.order_by("id").all()

    serializer_class = InterviewerSerializer


    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():

                user_obj=UserProfile.objects.get(id=self.request.data.get('user'))
                obj=serializer.save(object_id=gen_object_id(InterviewTimeslot),user=user_obj)
               
                try:
                    date_format='%Y-%m-%d %H:%M:%S.%f'
                    start_date = datetime.strptime(self.request.data.get('start_time'),date_format)
                    end_date = datetime.strptime(self.request.data.get('end_time'),date_format)
                    if start_date.date()==end_date.date():
                        start_date_hour = start_date.hour
                        end_date_hour = end_date.hour
                        s_date=start_date
                        slot_list=[]
                        while end_date_hour>=start_date_hour:
                            s_date+= timedelta(hours=1)
                            res=start_date.strftime('%Y-%m-%d %H:%M:%S.%f'),s_date.strftime('%Y-%m-%d %H:%M:%S.%f')
                            slot_list.append(res)
                            start_date=s_date
                            start_date_hour+=1
                        obj.available_slots=slot_list
                        obj.save()
                    else:
                        pass
                except Exception as e:
                    pass
                
                data["status"] = "success"
                data["message"] = "Interview available slots added successfully"
                data["code"] = 201
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "Failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "Failed"
            data["message"] = "something went wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class InterviewSlotEntryListView(ListAPIView):

    """
    all interview list view for both candidate and interviewer

    """

    serializer_class = InterviewerSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list=InterviewTimeslot.objects.order_by("-id")
        return queryset_list


class InterviewSlotEntryDeleteView(DestroyAPIView):
    """
    Interview slot Delete API View
    """
    queryset =  InterviewTimeslot.objects.order_by("id").all()
    serializer_class = InterviewerSerializer

    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            object_id = self.kwargs.get("object_id")
            InterviewTimeslot.objects.get(object_id=object_id).delete()

            data["status"] = True
            data["message"] = "Record Deleted Successfully" 
            data["code"] = 200

        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data["message"] = "something went wrong"
            data["status"] = "Failed"
            data["code"] = 500
        return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)



class InterviewSlotEntryEditView(RetrieveUpdateAPIView):

    """
    Interview slot and candidate/interviewer details edit api

    """

    serializer_class = InterviewerSerializer
    queryset = InterviewTimeslot.objects.order_by("id").all()
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                serializer.save()
                if self.request.data.get("user"):
                    user_data=self.request.data.get("user")
                    user_id=user_data.get("id")
                    UserProfile.objects.filter(id=user_id).update(email=user_data.get("email"),
                    designation=user_data['designation'],
                    name=user_data['name'],)
                data["message"] = "Record Updated successfully"
                data["status"] = "success"
                data['code'] = 200
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "Failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class ScheduledInterviewSlotEntryAddView(CreateAPIView):

    """
    scheduled interview entry view

    """
    queryset =  InterviewSchedule.objects.order_by("id").all()
    serializer_class = ScheduledInterviewerSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():

                candidate_obj=UserProfile.objects.get(id=self.request.data.get('candidate'))
                interviewer_obj=UserProfile.objects.get(id=self.request.data.get('interviewer'))

                # candidate_already_booked=InterviewTimeslot.objects.get(user=candidate_obj)
                # interview_already_booked=InterviewTimeslot.objects.get(user=interviewer_obj)

                # if candidate_already_booked.is_allocated is True and interview_already_booked.is_allocated is True:
                #     data["message"] = "Candidate and Interviewer schedules are already booked"
                #     data["status"] = "Failed"
                #     data["code"] = 400
                #     return data
               
                serializer.save(object_id=gen_object_id(InterviewSchedule),
                candidate=candidate_obj,
                interviewers=interviewer_obj,
                scheduled_slots=self.request.data.get('scheduled_slots')
                )
                InterviewTimeslot.objects.filter(Q(user=interviewer_obj) | Q(user=candidate_obj)).update(is_allocated=True)
               
                data["status"] = "success"
                data["message"] = "Interview Scheduled Successfully"
                data["code"] = 201
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "Failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "Failed"
            data["message"] = "something went wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class ScheduledInterviewSlotEntryListView(ListAPIView):

    """
    scheduled interview list view

    """

    serializer_class = ScheduledInterviewerSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list=InterviewSchedule.objects.order_by("-id")
        return queryset_list
