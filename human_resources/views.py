from django.shortcuts import render
from .models import HumanResource
# Create your views here.
def human_resources_home(request):
    human_resources=HumanResource.objects.all()
    context={
        'human_resources': human_resources
    }
    return render(request, "human_resources/human_resources_home.html", context)