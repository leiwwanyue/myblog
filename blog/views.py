from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from myblog.settings import SEND_TEXT_APP_KEY
from .models import Post, CustomUser, Carousel, BlogCategory
from .forms import PostForm, LoginForm
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from .forms import UserProfileForm

def post_list(request):
    users = CustomUser.objects.all()  # 假设你有一个名为 User 的模型，用来存储用户信息
    posts = Post.objects.all()
    carousels = Carousel.objects.filter(active=True)
    categories = BlogCategory.objects.all()
    print(f'categories:', categories)
    return render(request, 'blog/post_list.html', {'categories': categories, 'posts': posts, 'user_list': users, 'carousels': carousels})


# 例如，在 views.py 文件中定义评论视图函数
from .models import Comment
def post_detail(request, article_id):
    article = Post.objects.get(id=article_id)
    if request.method == 'POST':
        author = request.POST.get('author')
        content = request.POST.get('content')
        Comment.objects.create(author=author, content=content, article_id=article_id)
        return redirect('blog/post_detail.html', article_id=article_id)
    return render(request, 'blog/post_detail.html', {'post': article})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.author_id = request.user.id
            print(f'post.author_id:', post.author_id)
            print(f'post.author:', post.author)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_superuser:
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_superuser:
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # 重定向到用户个人信息页面
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

def signup(request):
    print(f'signup')
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.set_password = form.cleaned_data['password1']
            user.email = form.cleaned_data['email']
            user.age = form.cleaned_data['age']
            user.gender = form.cleaned_data['gender']
            user.interests = form.cleaned_data['interests']
            user.is_superuser = False
            # 增加staff逻辑
            user.is_staff = form.cleaned_data['is_staff']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.date_of_birth = form.cleaned_data['date_of_birth']
            user.is_active = True
            user.avatar = form.cleaned_data['avatar'] if 'avatar' in form.cleaned_data else None  # 获取上传的头像文件
            print(f'user2:{user}')
            user.save()
            return redirect('login')  # 注册成功后重定向到登录页面
        else:
            print(f'form.errors:{form.errors}')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def is_admin(user):
    return user.is_superuser

def custom_logout(request):
    logout(request)
    return redirect('post_list')

def user_profile(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'profile.html', {'user': user})

from django.views import View
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(f'username:{username}, password:{password}')
            user = authenticate(request, username=username, password=password)
            print(f'user:{user}')
            if user is not None:
                login(request, user)
                return redirect('post_list')  # 否则重定向到文章列表页面
            else:
                # 登录失败，显示错误消息
                form.add_error(None, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})


from django.shortcuts import render
def about(request):
    return render(request, 'about.html')


from .forms import BlogSearchForm
def search(request):
    form = BlogSearchForm(request.GET)
    print(f'results:', form)
    results = []
    if form.is_valid():
        # 从 Elasticsearch 获取匹配的博客文章 ID
        sqs = form.search()
        matched_ids = [result.pk for result in sqs]

        # 从 MySQL 数据库中获取详细信息
        results = Post.objects.filter(id__in=matched_ids)
        print(f'results:', results)

    return render(request, 'search/search_results.html', {'form': form, 'results': results})

from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import PasswordResetRequestForm
from django.contrib.auth.forms import SetPasswordForm

class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, 'password_reset_request.html', {'form': form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                site = get_current_site(request)
                link = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                mail_subject = 'Reset your password'
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': site.domain,
                    'uid': uid,
                    'token': token,
                    'link': link,
                })
                print(f'message:', message)
                send_mail(mail_subject, message, 'carrie.lei@qq.com', [email])
                return redirect('password_reset_done')
            form.add_error(None, 'Invalid username')
        return render(request, 'password_reset_request.html', {'form': form})


class PasswordResetConfirmView(View):
    def get(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form, 'user': user})
        else:
            return HttpResponse('Token is invalid!')

    def post(self, request, uidb64=None, token=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return redirect('password_reset_complete')
        return render(request, 'password_reset_confirm.html', {'form': form})


import random
import redis
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

# 连接 Redis
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

# 生成验证码
def generate_verification_code(length=6):
    return ''.join(random.choices('0123456789', k=length))



@require_POST
def request_verification_code(request):

    data = json.loads(request.body.decode('utf-8'))
    phone_number = data.get('phone_number')

    if not phone_number:
        return JsonResponse({'success': False, 'message': '手机号不能为空'}, status=400)

    # 生成验证码
    code = generate_verification_code()
    print(f'code, {code}')
    redis_key = f"verification_code:{phone_number}"
    redis_client.set(redis_key, code, ex=600)  # 5分钟有效期

    # 这里调用第三方短信服务商API发送验证码
    send_verification_code(phone_number, code)

    return JsonResponse({'success': True, 'message': '验证码已发送'})



@require_POST
def login_with_verification_code(request):
    try:
        data = json.loads(request.body)
        country_code = data.get('country_code')
        phone_number = data.get('phone_number')
        verification_code = data.get('verification_code')
        print(f'country_code, {country_code}, phone_number, {phone_number}, verification_code, {verification_code}')

        if not phone_number or not verification_code:
            return JsonResponse({'success': False, 'message': '手机号和验证码不能为空'}, status=400)

        redis_key = f"verification_code:{phone_number}"
        stored_code = redis_client.get(redis_key)
        print(f'stored_code, {stored_code}')

        if stored_code and stored_code.decode('utf-8') == verification_code:
            redis_client.delete(redis_key)
            user, created = CustomUser.objects.get_or_create(username=phone_number)
            print(f'user, {user}')
            if created:
                user.set_password(phone_number)
                user.email = f'{phone_number}@qq.com'
                user.save()
            login(request, user)
            redirect_url = '/post_list'  # 修改为实际的 post_list 页面 URL
            return JsonResponse({'success': True, 'redirect_url': redirect_url})
        return JsonResponse({'success': False, 'message': '验证码错误'}, status=400)
    except Exception as e:
        print(f'Error: {e}')
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

import requests
from django.conf import settings
import urllib, sys
import ssl


def send_verification_code(phone_number, code):
    host = 'http://zwp.market.alicloudapi.com'
    path = '/sms/sendv2'
    method = 'GET'
    appcode = settings.SEND_TEXT_APP_CODE
    content = f"【智能云】您的验证码是{code}。如非本人操作，请忽略本短信"
    querys = f'mobile={phone_number}&content={content}'
    bodys = {}
    api_url = host + path + '?' + querys

    headers = {
        'Authorization': 'APPCODE ' + appcode,
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(api_url, headers=headers, verify=True)
        if response.status_code == 200:
            print('短信发送成功')
            return True
        else:
            print(f'短信发送失败，错误代码: {response.status_code}, {response.text}')
            return False
    except requests.RequestException as e:
        print(f'短信发送失败: {str(e)}')
        return False



