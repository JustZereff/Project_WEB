from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import File
from .forms import FileForm
from cloudinary.uploader import destroy

def index_files(request):
    category = request.GET.get('category', 'all')
    if category != 'all':
        files_list = File.objects.filter(category=category)
    else:
        files_list = File.objects.all()
    
    paginator = Paginator(files_list, 10)  # Показувати 10 файлів на сторінку
    page_number = request.GET.get('page')
    files = paginator.get_page(page_number)
    
    return render(request, 'working_with_files/index_files.html', {
        'files': files,
        'category': category,
        'categories': File.CATEGORY_CHOICES,
    })

def file_upload(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index_files')  # Перенаправлення на сторінку з файлами після завантаження
    else:
        form = FileForm()
    return render(request, 'working_with_files/upload_file.html', {'form': form})

def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk)
    destroy(file.file.name)  # Видалення файлу з Cloudinary
    file.delete()  # Видалення запису з бази даних
    return redirect('index_files')
