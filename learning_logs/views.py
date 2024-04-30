from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm, EmailPostForm, SearchForm, ContactForm
from django.http import Http404, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action


def index(request):
    if request.user.is_authenticated:       
        return redirect('learning_logs:topics')
    else:       
        return render(request, 'learning_logs/index.html')


def api_page(request):
    return render(request, 'learning_logs/api.html')


def privacy_policy(request):
    return render(request, 'learning_logs/privacy_policy.html')


def all_topics(request, tag_slug=None):
    topics = Topic.objects.all().order_by('-date_added')
    tag = None
    paginator = Paginator(topics, 20)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            topics = topics.filter(tags__in=[tag])
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'learning_logs/all_topics.html', {'topics': topics, 'tag': tag})


def topics(request, tag_slug=None):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    tag = None
    paginator = Paginator(topics, 5)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            topics = topics.filter(tags__in=[tag])
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'learning_logs/topics.html', {'topics': topics, 'tag': tag})


def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = get_object_or_404(Topic, id=topic_id)
    topic.total_views += 1
    topic.save()
    # increment topic ranking by 1
    #r.zincrby('topic_ranking', 1, topic_id)
    entries = Entry.objects.filter(topic=topic)

    # List of similar posts
    topic_tags_ids = topic.tags.values_list('id', flat=True)
    similar_topics = Topic.objects.filter(tags__in=topic_tags_ids).exclude(id=topic.id)
    similar_topics = similar_topics.annotate(same_tags=Count('tags')).order_by('-same_tags')[:5]
    context = {'topic': topic, 'entries': entries, 'similar_topics': similar_topics, }
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':        
        form = TopicForm()
    else:        
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            create_action(request.user, 'created new subject', new_topic)        
            tags = form.cleaned_data['tags']
            for tag in tags:
                Tag.objects.get_or_create(name=tag)
                new_topic.tags.add(tag)
            return redirect('learning_logs:topics')    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise 404
    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    return render(request, 'learning_logs/edit_topic.html', {'form': form, 'topic': topic})


@login_required
def delete_topic(request, topic_id):    
    topic = get_object_or_404(Topic, id=topic_id)    
    if topic.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this topic.")
    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')
    else:
        context = {'topic': topic}
        return render(request, 'learning_logs/confirm_delete_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.user = request.user
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)        
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if entry.user != request.user:
        raise Http404
    if request.method != 'POST':        
        form = EntryForm(instance=entry)
    else:        
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'form': form, 'entry': entry, 'topic': topic}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):    
    entry = get_object_or_404(Entry, id=entry_id)    
    if entry.user != request.user:
        return HttpResponseForbidden("You do not have permission to delete this topic.")
    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topics')
    else:
        context = {'entry': entry}
        return render(request, 'learning_logs/confirm_delete_entry.html', context)


@login_required
def share_post(request, topic_id):    
    topic = get_object_or_404(Topic, id=topic_id)
    user_name = request.user.username
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(topic.get_absolute_url())
            subject = f"This is testing email message! {user_name} recommends this post: {topic.text}"
            message = f"This is testing email! User {user_name}, recommends : {topic.text} at {post_url}"
            send_mail(subject, message, 'djangochronics@gmail.com', [cd['to']])            
            return render(request, 'learning_logs/email_sent.html', {'topic': topic, 'form': form})
    else:
        form = EmailPostForm()
    return render(request, 'learning_logs/share_post.html', {'topic': topic, 'form': form})


def topic_search(request):
    form = SearchForm()
    search = None
    results = []

    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            search_vector = SearchVector('text', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(search)
            results = Topic.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)
                                             ).filter(rank__gte=0.3).order_by('-rank')

    paginator = Paginator(results, 10)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'learning_logs/search.html',
                  {'form': form, 'search': search, 'results': results})


@login_required
@require_POST
def topic_like(request):
    topic_id = request.POST.get('id')
    action = request.POST.get('action')
    if topic_id and action:
        try:
            topic = Topic.objects.get(id=topic_id)
            if action == 'like':
                topic.users_like.add(request.user)
                create_action(request.user, 'likes', topic)
            else:
                topic.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Topic.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def liked_topics(request):
    profile = request.user.profile
    liked_topics = Topic.objects.filter(users_like=request.user).select_related('owner')
    return render(request, 'learning_logs/liked_topics.html',
                  {'profile': profile, 'liked_topics': liked_topics})


def most_liked_topics(request):
    most_liked_topics = Topic.objects.annotate(like_count=Count('total_likes')).order_by('-like_count')
    return render(request, 'learning_logs/most_liked_topics.html',
                  {'most_liked_topics': most_liked_topics})


def most_viewed(request):
    most_viewed = Topic.objects.annotate(views_count=Count('total_views')).order_by('-total_views')[:5]
    return render(request, 'learning_logs/most_viewed.html', {'most_viewed': most_viewed})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = f"Sender's Email: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
            from_email = form.cleaned_data['email']
            recipient_list = ['djangochronics@gmail.com']
            send_mail(subject, message, from_email, recipient_list)
            return render(request, 'learning_logs/contact_success.html')
    else:
        form = ContactForm()
    return render(request, 'learning_logs/contact.html', {'form': form})


def success_view(request):
    return render(request, 'learning_logs/contact_success.html')