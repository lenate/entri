
## Assumption
The assumptions I made while solving this problem were what if there happens to be a conflict if the same interviewer is happened to be booked
on same time slot and that issue still persist in my application too.


## Bonus Point

1. I think as the interview slots are of 1 hour it would better to take from both the candidate and interview max two time slots like their available from
   9am-10pm and 1pm to 2pm like that. So on before hand itself we can give then somewhat the exact time for the interview as they suggested rather than
   providing them a time in between these slots .

2. If I had some more time how I would you improved my interview application project by trying to avoid the
   conflict if the same interviewer is happened to be booked on same time slot and also try automated the interview application.
   
   In my application I tried to use the logger.info(logging) statements intead of print as 
   Logging output is more flexible. It can be done at console or to a file or to some other output place and be referenced for future analysis
   and You can log to files, sockets, pretty much anything, all at the same time
   Secondly, I have incoporated the post_save functionality in models.
   
   
## Examples

add candidate or interviewer

- url : http://127.0.0.1:8000/interviewschedule/entri/candidate-or-interviewer/add/
- request payload(raw data) : {
    "name": "cyril",
    "designation": "Angular Developer",
    "email": "cyril@gmail.com",
    "is_interviewer": true
   
}

candidate and interviewer list API handled dynamically by passing query param user_type

- url : http://127.0.0.1:8000/interviewschedule/entri/user/listing/
- Query Parameter : user_type=candidate/interviewer
}


candidate and interviewer list API handled dynamically by passing query param user_type

- url : http://127.0.0.1:8000/interviewschedule/entri/user/listing/
- Query Parameter : user_type=candidate/interviewer



To list out entire candidate and interviewer

- url : http://127.0.0.1:8000/interviewschedule/entri/all-entri-user-profile/listing


To enter candidate/interviewer slot

- url : http://127.0.0.1:8000/interviewschedule/entri/interview/timeslot/entry/
- request payload(raw data) : {
    "start_time": "2021-08-12 10:00:19.358539",
    "end_time": "2021-08-12 13:00:00.00000",
    "is_allocated": false,
    "user":32
}


each candidate/interviewer available slot list

- url : http://127.0.0.1:8000/interviewschedule/entri/interview/timeslot/entry/list/


To edit candidate/interviewer slot or their details

- url : http://127.0.0.1:8000/interviewschedule/interview/time-slot/69025961-8e41-4101-b2c6-2035c5b26a94/edit/
- request payload(raw data) : {   "start_time": "2021-08-12T10:00:19.358539Z",
        "end_time": "2021-08-12T13:00:00Z",
        "user": {
            "id": 32,
            "user_id": "IN-032",
            "name": "ranish",
            "email": "ranish001@gmail.com",
            "designation": "Angular Developer",
            "is_interviewer": true
        }
}


each candidate/interviewer available slot deletion

- url : http://127.0.0.1:8000/interviewschedule/interview/time-slot/eb0697ee-f990-401d-83fa-0f714dddd318/delete/



HR adding the scheduled interview slot for interview 

- url : http://127.0.0.1:8000/interviewschedule/entri/scheduled/interview/slot/entry/
- request payload(raw data) : {
    "candidate":33,
    "interviewer":32,
    "scheduled_slots":[
            [
                "2021-08-11 11:00:19.358539",
                "2021-08-11 12:00:19.358539"
            ],
            [
                "2021-08-11 12:00:19.358539",
                "2021-08-11 13:00:19.358539"
            ]
        ]}
        
        
  
each candidate/interviewer available slot list

- url : http://127.0.0.1:8000/interviewschedule/entri/scheduled/interview/slot/listing/





