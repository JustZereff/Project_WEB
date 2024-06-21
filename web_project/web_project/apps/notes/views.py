from django.shortcuts import render

def index_notes(request):
    return render(request, 'notes/all_notes.html')