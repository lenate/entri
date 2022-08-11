from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

# Create your models here.


DESIGNATION = (
    ('Django Developer', 'Django Developer'),
    ('Angular Developer', 'Angular Developer'),
    ('QA Developer', 'QA Developer')
)


class UserProfile(models.Model):

    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    name = models.CharField(max_length=30)
    designation = models.CharField(max_length=50, choices=DESIGNATION, default='CharField')
    email = models.EmailField(unique=True)
    is_interviewer = models.BooleanField(default=False)
    user_id = models.CharField(max_length=30,blank=True,null=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    if_logged = models.BooleanField(default=False)
    password = models.CharField(max_length=50,null=True, blank=True)
    first_time_login = models.BooleanField(default=False)


    
    def __str__(self):
        return "{}".format(self.name) 

    class Meta:
        db_table = "userprofile_table"

@receiver(post_save, sender=UserProfile)
def user_created(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        if instance.is_interviewer:  
            user_id = 'IN-{0}'.format(str(instance_id).zfill(3))
        else:
            user_id = 'CD-{0}'.format(str(instance_id).zfill(3))
        instance.user_id = user_id
        instance.save()


class InterviewTimeslot(models.Model):

    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    user = models.ForeignKey(
       UserProfile, blank=True, null=True, on_delete=models.SET_NULL
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_allocated = models.BooleanField(default=False)
    available_slots = models.JSONField(default=dict,null=True,blank=True)

    
    def __str__(self):
        return " Interview availability from {0} to {1} to {2}".format(self.start_time, self.end_time, self.user)

    class Meta:
        db_table = "interviewtimeslot_table"


class InterviewSchedule(models.Model):

    object_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    candidate = models.ForeignKey(
       UserProfile, blank=True, null=True, on_delete=models.SET_NULL
    )
    scheduled_slots = models.JSONField(default=dict,null=True,blank=True)
    interview_id = models.CharField(max_length=30,blank=True,null=True)
    interviewers = models.ForeignKey(
       UserProfile, blank=True, null=True, on_delete=models.SET_NULL,related_name="interviewers"
    )

    
    def __str__(self):
        return "{0} is the interviewer for the candidate {1}".format(self.interviewers, self.candidate)

    class Meta:
        db_table = "interviewschedule_table"

@receiver(post_save, sender=InterviewSchedule)
def interview_created(sender, instance, created, **kwargs):
    if created:
        instance_id = instance.id
        interview_id = 'ID-{0}'.format(str(instance_id).zfill(3))
        instance.interview_id = interview_id
        instance.save()


# class AuditFields(models.Model):

#     name = models.CharField(max_length=30)
#     designation = models.CharField(max_length=50, choices=DESIGNATION, default='CharField')
#     email = models.EmailField(unique=True)
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)
#     entry_date = models.DateField(blank=True, null=True)
    
#     class Meta:
#         abstract = True

# class Timeslot(models.Model):

#     object_id = models.UUIDField(
#         unique=True,
#         editable=False,
#         default=uuid.uuid4,
#         verbose_name='Public identifier',
#     )
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)
#     entry_date = models.DateField(blank=True, null=True)
   

    
#     def __str__(self):
#         return "{}".format(self.interviewer_id) 
    
#     class Meta:
#         db_table = "timeslot_table"

        


# @receiver(post_save, sender=Candidate)
# def candidate_created(sender, instance, created, **kwargs):
#     if created:
#         instance_id = instance.id
#         candidate_id = 'CD-{0}'.format(str(instance_id).zfill(3))
#         instance.candidate_id = candidate_id
#         instance.save()



# class Interviewer(AuditFields):

#     object_id = models.UUIDField(
#         unique=True,
#         editable=False,
#         default=uuid.uuid4,
#         verbose_name='Public identifier',
#     )
#     interviewer_id = models.CharField(max_length=30, blank=True, null=True)
#     # time_slot = models.ManyToManyField(
#     #     Timeslot, blank=True,related_name="%(app_label)s_%(class)s_time_slot")

    
#     def __str__(self):
#         return "{}".format(self.interviewer_id) 
    
#     class Meta:
#         db_table = "interviewer_table"

# @receiver(post_save, sender=Interviewer)
# def interviewer_created(sender, instance, created, **kwargs):
#     if created:
#         instance_id = instance.id
#         interviewer_id = 'IN-{0}'.format(str(instance_id).zfill(3))
#         instance.interviewer_id = interviewer_id
#         instance.save()





