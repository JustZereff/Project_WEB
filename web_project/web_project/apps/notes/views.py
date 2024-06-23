from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from index.models import Tag, Note, CustomUser
from .forms import NoteForm, TagForm


@login_required
def index_notes(request, page=1):
    notes = Note.objects.filter(user=request.user).all()
    paginator = Paginator(notes, 5)
    notes_on_page = paginator.page(page)
    return render(request, 'notes/all_notes.html', context={'notes_on_page': notes_on_page})


@login_required
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes/all_notes.html')
    else:
        form = TagForm()
    return render(request, 'notes/create_tag.html', {'form': form})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.tags = note.add_tags(form.tags)
            note.save()
            return redirect(to='index_notes')
        else:
            return render(request, 'notes/create_note', {'form': form})

    return render(request, 'notes/create_note', {'form': NoteForm()})

@login_required
def edit_note(request, note_id: int):
    note = get_object_or_404(Note, pk=note_id)
    
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            # Оновлення тегів
            note.tags.set(form.cleaned_data['tags'])
            note.save()
            return redirect(to='index_notes')
    else:
        form = NoteForm(instance=note)
    
    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('notes/all_notes.html')
    return render(request, 'notes/delete_note.html', {'note': note})

@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/view_note.html', {'note': note})

@login_required
def sort_notes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    notes = Note.objects.filter(user=request.user, tags=tag).all()
    paginator = Paginator(notes, 5)
    notes_on_page = paginator.page(1)
    return render(request, 'notes/all_notes.html', context={'notes_on_page': notes_on_page})

@login_required
def sort_notes_by_date(request):
    notes = Note.objects.order_by('created_at').all()
    paginator = Paginator(notes, 5)
    notes_on_page = paginator.page(1)
    return render(request, 'notes/all_notes.html', context={'notes_on_page': notes_on_page})