from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from haystack.forms import SearchForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    age = forms.IntegerField(required=False, min_value=18)
    GENDER_CHOICES = (('M', 'Male'),('F', 'Female'),)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=False)
    INTEREST_CHOICES = (
        ('basketball', '篮球'),
        ('singing', '唱歌'),
        ('dancing', '跳舞'),
        ('traveling', '旅行'),
        ('reading', '读书'),
        ('public_speaking', '演讲'),
        ('binge_watching', '追剧'),
    )
    interests = forms.MultipleChoiceField(choices=INTEREST_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    avatar = forms.ImageField(required=False)  # 添加头像上传字段
    is_staff = forms.BooleanField(required=False, label='Is Staff')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2','first_name', 'last_name',   'date_of_birth', 'age', 'gender', 'interests', 'avatar', 'is_staff')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'interests', 'avatar')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'interests', 'avatar')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =  ('email', 'username', 'first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'interests', 'avatar')  # 需要更新的用户信息字段

class BlogSearchForm(SearchForm):
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        return super().search()

from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()  # 添加验证码字段

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Enter your email", max_length=254)

# 例如，在 forms.py 文件中定义评论表单
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

