from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import datetime 
from datetime import date

from .models import Topic, Entry, TaskCompletion
from .forms import TopicForm, EntryForm
from .stats import day_completion, month_completion


def index(request):
    """The register page for account_homepage."""
    return render(request, 'account_homepage/index.html')

@login_required
def home(request):
    user = request.user
    """The home page for account_homepage."""
    topics = Topic.objects.filter(owner=user).order_by('text')

    today = date.today()
    year = today.year
    month = today.month

    habits = {}

    from calendar import monthrange
    days_in_month = monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        key = d.strftime("%Y-%m-%d")
        habits[key] = [t.id for t in topics]

    completions = TaskCompletion.objects.filter(user=user)
    completed = {}
    for completion in completions:
        date_key = completion.date.strftime('%Y-%m-%d')
        if date_key not in completed:
            completed[date_key] = []
        completed[date_key].append(completion.topic.id)


    today_str = today.strftime("%Y-%m-%d")
    month_str = today.strftime("%Y-%m")

    day_stats = day_completion(today_str, habits, completed)
    month_stats = month_completion(month_str, habits, completed)

    context = {
        'topics': topics,
        'completions': json.dumps(completed), 
        'day_stats': day_stats,
        'month_stats': month_stats,
    }
    return render(request, 'account_homepage/home.html', context)

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'account_homepage/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'account_homepage/topic.html', context)

@login_required    
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user

            # These names MUST match the model field names above
            new_topic.monday = True if request.POST.get('monday') else False
            new_topic.tuesday = True if request.POST.get('tuesday') else False
            new_topic.wednesday = True if request.POST.get('wednesday') else False
            new_topic.thursday = True if request.POST.get('thursday') else False
            new_topic.friday = True if request.POST.get('friday') else False
            new_topic.saturday = True if request.POST.get('saturday') else False
            new_topic.sunday = True if request.POST.get('sunday') else False

            new_topic.save()
            return redirect('account_homepage:topics')

    context = {'form': form}
    return render(request, 'account_homepage/new_topic.html', context)


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
            return redirect('account_homepage:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'account_homepage/new_entry.html', context)

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
            return redirect('account_homepage:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'account_homepage/edit_entry.html', context)

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