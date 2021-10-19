from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """The home page for Learning_log"""
    return render(request, 'learning_logs\index.html')

@login_required()
def topics(request):
    
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, r'learning_logs\topics.html', context)

@login_required()
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    if topic.owner != request.user:
        raise Http404
    context = {
        "topic":topic,
        "entries": entries
    }
    return render(request, r'learning_logs\topic.html', context)

@login_required()    
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
        
    return render(request, r"learning_logs\new_topic.html", {
        "form": form
    })
    
@login_required()    
def new_entry(request, topic_id):
    topic = Topic.objects.get(pk = topic_id)
    
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
        
    context = {'topic': topic, 'form': form}
    return render(request, r'learning_logs\new_entry.html', context)


@login_required()
def edit_entry(request, entry_id):
    entry = Entry.objects.get(pk = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        form = EntryForm(instance= entry)
        
    else:
        form = EntryForm(instance= entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("learning_logs:topic", args=[topic.id]))
    context = {
        "form": form,
        "entry": entry,
        "topic": topic
    }
    return render(request, r'learning_logs\edit_entry.html', context)

@login_required()
def delete_entry(request, entry_id):
    entry = Entry.objects.get(pk = entry_id)
    topic = entry.topic
    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))
    
    
@login_required()
def delete_topic(request, topic_id):
    topic = Topic.objects.get(pk = topic_id)
    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))
    

    
    


    
    
    
    
    