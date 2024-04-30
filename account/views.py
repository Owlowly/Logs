from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from actions.models import Action
from actions.utils import create_action
from learning_logs.models import Topic, Entry
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, MessageForm
from .models import Profile, Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.db.models import Q, F
from django.db.models import Subquery, OuterRef, Count



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'Account created successfully')
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:profile')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        return HttpResponse("You don't have permission for deleting")
    if request.method == 'POST':
        user.delete()
        return redirect('learning_logs:index')
    else:
        return render(request, 'account/confirm_delete_user.html', {'user': user})


@login_required
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    context = {
        'profile': profile,
    }
    return render(request, 'account/profile.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile_edit.html',
                  {'user_form': user_form, 'profile_form': profile_form,})


def all_users(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    paginator = Paginator(profiles, 4)
    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)
    return render(request, 'account/all_users.html', {'users': users, 'profiles': profiles})


def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    topics = Topic.objects.filter(owner=profile_user)
    entries = Entry.objects.filter(topic__in=topics)

    context = {
        'profile_user': profile_user,
        'topics': topics,
        'entries': entries,
        'topic': None,
    }
    return render(request, 'account/view_profile.html', context)


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            profile = Profile.objects.get(user_id=user_id)
            if action == 'follow':
                profile.user_follow.add(request.user)
                create_action(request.user, 'is following', profile)
            else:
                profile.user_follow.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


def most_followed_users(request):
    most_followed_users = Profile.objects.order_by('-total_followers')[:5]
    return render(request, 'account/most_followed_users.html',
                  {'most_followed_users': most_followed_users})


@login_required
def followed_users(request):
    profile = request.user.profile
    followed_users = Profile.objects.filter(user_follow=request.user)
    return render(request, 'account/followed_users.html',
                  {'profile': profile, 'followed_users': followed_users})

@login_required
def activity_feed(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = Profile.objects.filter(user_follow=request.user).values_list('user__id')
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/activity_feed.html', {'actions': actions})


@login_required
def all_messages(request):
    user = request.user
    latest_timestamps = Message.objects.filter(
        recipient=user,
        sender=OuterRef('sender')
    ).order_by('-timestamp').values('timestamp')[:1]
    messages = Message.objects.filter(
        recipient=user
    ).annotate(
        latest_timestamp=Subquery(latest_timestamps)
    ).filter(
        timestamp=F('latest_timestamp')
    ).annotate(
        unread_count=Count('id', filter=Q(read=False))
    )
    unread_count = Message.objects.filter(recipient=user, read=False).count()
    return render(request, 'account/all_messages.html',
                  {'messages': messages, 'unread_count': unread_count})


# not used in this project
@login_required
def all_messages_works(request):
    user = request.user
    messages = Message.objects.filter(recipient=user).order_by('sender', '-timestamp').distinct('sender')
    return render(request, 'account/all_messages.html', {'messages': messages})


@login_required
def user_messages(request, username):
    user = request.user
    profile_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=user, recipient=profile_user) | Q(sender=profile_user, recipient=user))
    ).order_by('-timestamp')
    # Mark messages as read
    for message in messages:
        if message.recipient == user and not message.read:
            message.read = True
            message.save()
    return render(request, 'account/user_messages.html', {'profile_user': profile_user, 'messages': messages})


@login_required
def send_messages(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = profile_user.user
            new_message.read = False
            new_message.save()
            return redirect('account:user_messages', username=username)
        else:
            messages.error(request, 'Error sending message. Please check the form.')
    else:
        form = MessageForm()
    context = {'form': form, 'profile_user': profile_user}
    return render(request, 'account/send_messages.html', context)


@login_required
def user_messages_delete(request, username):
    user = request.user
    profile_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(Q(sender=user, recipient=profile_user) | Q(sender=profile_user, recipient=user))
    if not messages.exists():
        return HttpResponseForbidden("You don't have permission to delete messages.")
    if request.method == 'POST':
        messages.delete()
        return redirect('account:all_messages')
    else:
        context = {'user': user, 'profile_user': profile_user, 'messages': messages}
        return render(request, 'account/confirm_delete_messages.html', context)


@login_required
def send_messages_works(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = profile_user.user
            new_message.save()
            return redirect('account:all_messages')
        else:
            form = MessageForm()
    else:
        form = MessageForm()
    context = {'form': form, 'profile_user': profile_user}
    return render(request, 'account/send_messages.html', context)

