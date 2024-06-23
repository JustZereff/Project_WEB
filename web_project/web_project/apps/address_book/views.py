from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import ContactForm
from index.models import Contact

@login_required
def index_address_book(request):
    contacts = Contact.objects.filter(user=request.user).order_by('id')  # Добавлено упорядочение
    paginator = Paginator(contacts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = ContactForm()
    return render(request, 'address_book/index.html', {'form': form, 'page_obj': page_obj})

@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('address_book:contact_list')
    else:
        form = ContactForm()
    return render(request, 'address_book/create_contact.html', {'form': form})

@login_required
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('address_book:contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'address_book/edit_contact.html', {'form': form, 'contact': contact})

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user).order_by('id')  # Добавлено упорядочение
    paginator = Paginator(contacts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'address_book/all_contacts.html', {'page_obj': page_obj})

@login_required
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id, user=request.user)
    data = {
        'id': contact.id,
        'name': contact.name,
        'email': contact.email,
        'phone': contact.phone,
        'address': contact.address,
        'birth_date': contact.birth_date.strftime('%Y-%m-%d') if contact.birth_date else None,
    }
    return JsonResponse(data)
