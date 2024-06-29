from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from index.models import File
from .forms import FileForm
from cloudinary.uploader import destroy
from django.contrib.auth.decorators import login_required

@login_required
def index_files(request):
    category = request.GET.get('category', 'all')
    sort_order = request.GET.get('sort_order', 'desc')

    files_list = File.objects.filter(user=request.user)
    if category != 'all':
        files_list = files_list.filter(category=category)
    
    if sort_order in ['asc', 'desc']:
        order = 'uploaded_at' if sort_order == 'asc' else '-uploaded_at'
        files_list = files_list.order_by(order)
    
    paginator = Paginator(files_list, 10)
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)
    
    return render(request, 'working_with_files/index_files.html', {
        'files': files,
        'category': category,
        'sort_order': sort_order,
        'categories': File.CATEGORY_CHOICES,
    })

@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('index_files')
    else:
        form = FileForm(user=request.user)
    return render(request, 'working_with_files/upload_file.html', {'form': form})

@login_required
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk, user=request.user)
    
    if request.method == 'POST':
        try:
            # Видалити файл з Cloudinary
            file_url = file.file.url
            public_id = '/'.join(file.file.name.split('/')[-2:])
            public_id = public_id.replace('.' + file_url.split('.')[-1], '')
            destroy(public_id)
           
            # Видалити файл з бази даних
            file.delete()
        except Exception as e:
            print(f"Error deleting file {file.name}: {str(e)}")

        return HttpResponseRedirect(reverse('index_files'))

    return render(request, 'working_with_files/confirm_delete.html', {'file': file})
