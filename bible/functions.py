from .models import Profile



"""
CONTINUE READIND
If user exists on Profile model
update continue_reading_url with current path
else create new record and set continue_reading_url
count checks if record exists
save() updates existing record
"""
def continue_reading(request):
    user = request.user.id

    if user:
        if Profile.objects.filter(user=user).count():
            p = Profile.objects.get(user=user) # select the record
            p.continue_reading_url = request.path
            p.save()
        else:
            p = Profile()
            p.user_id = user
            p.continue_reading_url = request.path
            p.save()
