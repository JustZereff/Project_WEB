from django.shortcuts import render

def index_files(request):
    return render(request, 'working_with_files/index_files.html')