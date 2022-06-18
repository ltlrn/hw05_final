from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import paging

POSTS_PER_PAGE = 10


def index(request):
    """Отображение главной страницы."""

    post_list = Post.objects.all()
    page_obj = paging(request, post_list, POSTS_PER_PAGE)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Отображение страниц сообществ."""

    group = get_object_or_404(Group, slug=slug)

    post_list = group.posts.all()
    page_obj = paging(request, post_list, POSTS_PER_PAGE)

    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Отображение страницы пользователя."""

    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paging(request, post_list, POSTS_PER_PAGE)

    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=author
    ).exists()

    context = {
        'author': author,
        'page_obj': page_obj,
        'posts': post_list,
        'following': following
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Отображение отдельной публикации."""

    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'form': form,
        'comments': comment
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Отображение страницы создания публикации."""

    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )

    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()

        return redirect('posts:profile', new_post.author.username)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Отображение страницы редактирования публикации."""

    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('posts:profile', post.author.username)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )

    if form.is_valid():
        edited_post = form.save(commit=False)
        edited_post.author = request.user
        edited_post.save(update_fields=['text', 'group', 'author', 'image'])

        return redirect('posts:post_detail', post_id)

    context = {
        'form': form,
        'post': post,
        'is_edit': True
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    """Отображение добавления комментария."""

    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Отображение публикаций подписок."""

    post_list = Post.objects.filter(
        author__following__user=request.user
    ).select_related(
        'author',
        'group',
    )

    page_object = paging(request, post_list, POSTS_PER_PAGE)
    context = {
        'page_obj': page_object
    }

    return render(
        request,
        'posts/follow.html',
        context
    )


@login_required
def profile_follow(request, username):
    """Подписка на профиль."""

    user = request.user
    author = get_object_or_404(User, username=username)

    if author != user:
        if not Follow.objects.filter(user=user, author=author).exists():
            Follow.objects.create(user=user, author=author)

    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """Отписка от профиля"""

    user = request.user
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=user, author=author).delete()

    return redirect('posts:profile', username)
