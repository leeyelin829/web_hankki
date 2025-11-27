from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from .models import Post, Comment
from .forms import PostForm, CommentForm


def home(request):
    """홈 페이지"""
    return render(request, 'webapp/home.html')


def login_view(request):
    """로그인"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')

    return render(request, 'webapp/login.html')


def logout_view(request):
    """로그아웃"""
    logout(request)
    return redirect('home')


def signup_view(request):
    """회원가입"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        # 유효성 검사
        if password1 != password2:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'webapp/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return render(request, 'webapp/signup.html')

        # 사용자 생성
        try:
            user = User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            login(request, user)  # 가입 후 자동 로그인
            messages.success(request, f'{username}님, 환영합니다!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f'회원가입 중 오류가 발생했습니다: {str(e)}')

    return render(request, 'webapp/signup.html')


def post_list(request):
    """커뮤니티 게시글 목록"""
    # 정렬 방식 가져오기 (기본값: 시간순)
    sort = request.GET.get('sort', 'recent')

    if sort == 'popular':
        # 좋아요 많은 순
        posts = Post.objects.annotate(
            like_count_num=models.Count('likes')
        ).order_by('-like_count_num', '-created_at')
    else:
        # 최신순
        posts = Post.objects.all().order_by('-created_at')

    # 인기글 (좋아요 많은 상위 6개) - 3페이지 × 2개씩
    popular_posts = Post.objects.annotate(
        like_count_num=models.Count('likes')
    ).order_by('-like_count_num', '-created_at')[:6]

    context = {
        'posts': posts,
        'popular_posts': popular_posts,
        'current_sort': sort,
    }
    return render(request, 'webapp/post_list.html', context)

@login_required
def post_create(request):
    """게시글 작성"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '게시글이 작성되었습니다.')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()

    return render(request, 'webapp/post_create.html', {'form': form})


def post_detail(request, post_id):
    """게시글 상세보기 + 댓글"""
    post = get_object_or_404(Post, pk=post_id)

    # 🆕 조회수 증가 (매번 방문할 때마다)
    post.views += 1
    post.save()

    comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, '댓글이 작성되었습니다.')
                return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, '댓글을 작성하려면 로그인이 필요합니다.')
            return redirect('login')
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'webapp/post_detail.html', context)

@login_required
def post_like(request, post_id):
    """좋아요 토글"""
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', post_id=post.id)


@login_required
def mypage(request):
    """마이페이지"""
    user = request.user

    # 내가 쓴 글
    my_posts = Post.objects.filter(author=user).order_by('-created_at')[:5]

    # 내가 쓴 댓글
    my_comments = Comment.objects.filter(author=user).order_by('-created_at')[:5]

    # 좋아요한 글
    liked_posts = user.liked_posts.all().order_by('-created_at')[:5]

    context = {
        'user': user,
        'my_posts': my_posts,
        'my_comments': my_comments,
        'liked_posts': liked_posts,
        'total_posts': Post.objects.filter(author=user).count(),
        'total_comments': Comment.objects.filter(author=user).count(),
        'total_likes': user.liked_posts.count(),
    }
    return render(request, 'webapp/mypage.html', context)