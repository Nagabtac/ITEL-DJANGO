from django.shortcuts import render

# Create your views here.
def index(request):
    user= {
        "name": "Darwin",
        "age": "19",
        "course": "BSIT-II",
        "motto": "no matter what happen remember to feel WEIIII"
    }
    
    return render(request, 'index.html', {'user': user})
