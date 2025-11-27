from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요', 'rows': 10}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'thumbnail': '썸네일 이미지',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '댓글을 입력하세요', 'rows': 3}),
        }
        labels = {
            'content': '댓글',
        }