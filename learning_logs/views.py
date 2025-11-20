from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import datetime 

from .models import Topic, Entry, TaskCompletion
from .forms import TopicForm, EntryForm


def index(request):
    """The register page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def home(request):
    """The home page for Learning Log."""
    topics = Topic.objects.filter(owner=request.user).order_by('text')
    completions = TaskCompletion.objects.filter(user=request.user)
    completions_dict = {}
    for completion in completions:
        date_key = completion.date.strftime('%Y-%m-%d')
        if date_key not in completions_dict:
            completions_dict[date_key] = []
        completions_dict[date_key].append(completion.topic.id)
    context = {'topics': topics,'completions':json.dumps(completions_dict)}
    return render(request, 'learning_logs/home.html', context)

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required    
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required    
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
@require_POST
def toggle_task(request):
    data = json.loads(request.body)
    topic_id = data.get('topic_id')
    date_str = data.get('date')
    
    topic = Topic.objects.get(id=topic_id, owner=request.user)
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    completion = TaskCompletion.objects.filter(
        user=request.user,
        topic=topic,
        date=date
    ).first()
    
    if completion:
        completion.delete()
        completed = False
    else:
        TaskCompletion.objects.create(
            user=request.user,
            topic=topic,
            date=date
        )
        completed = True
    return JsonResponse({'success':True,'completed':completed})