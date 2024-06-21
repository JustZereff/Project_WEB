from django.shortcuts import render

def index_address_book(request):
    return render(request, 'address_book/all_contacts.html')