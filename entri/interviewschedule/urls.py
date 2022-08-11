from django.urls import path
from .views import *

urlpatterns = [
    
    # candidate or interviewer add entry API's
    path('entri/candidate-or-interviewer/add/', CandidateandInterviewerAvailabilityAddEntryView.as_view(), name="candidate_or_interviewer_availability_add_entry"),

    #login api
    path('login/', Login.as_view(), name="login"),

    # all entri users list API's
    path('entri/all-entri-user-profile/listing/', AllEntriUserProfileListView.as_view(), name="entri_user_list"),

    # candidate and interviewer list API handled dynamically by pass query param user_type
    path('entri/user/listing/', UserListView.as_view(), name="entri_user_list"),

    # candidate/interviewer interview slot entry API
    path('entri/interview/timeslot/entry/', InterviewSlotEntryAddView.as_view(), name="interview_slot_entry_add"),


    # candidate/interviewer interview slot list API
    path('entri/interview/timeslot/entry/list/', InterviewSlotEntryListView.as_view(), name="interview_slot_entry_list"),

    # candidate/interviewer interview slot entry delete API
    path("interview/time-slot/<str:object_id>/delete/",InterviewSlotEntryDeleteView.as_view(),name="interview_slot_entry_delete"),

    # candidate/interviewer interview slot entry edit API
    path('interview/time-slot/<str:object_id>/edit/', InterviewSlotEntryEditView.as_view(), name="interview_availability_edit_entry"),


    # scheduled interview slot entry API
    path('entri/scheduled/interview/slot/entry/', ScheduledInterviewSlotEntryAddView.as_view(), name="scheduled_interview_slot_entry_add"),

    # scheduled interview list API's
    path('entri/scheduled/interview/slot/listing/', ScheduledInterviewSlotEntryListView.as_view(), name="entri_user_list"),
     
    path('logout/',Logout.as_view(), name="logout"),
]