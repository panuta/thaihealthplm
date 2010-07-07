from django.shortcuts import redirect

def view_homepage(request):
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")