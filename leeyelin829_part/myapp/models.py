from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """게시글 모델"""
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='작성자',
        related_name='posts'
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True,
        verbose_name='썸네일'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    likes = models.ManyToManyField(
        User, 
        related_name='liked_posts', 
        blank=True,
        verbose_name='좋아요'
    )
    views = models.IntegerField(default=0, verbose_name='조회수')  # 🆕 조회수 추가

    class Meta:
        ordering = ['-created_at']
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'

    def __str__(self):
        return self.title

    @property
    def preview(self):
        """본문 앞 15글자만 반환"""
        if len(self.content) > 15:
            return self.content[:15] + '...'
        return self.content

    def like_count(self):
        """좋아요 수 반환"""
        return self.likes.count()


class Comment(models.Model):
    """댓글 모델"""
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='게시글'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    content = models.TextField(verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    class Meta:
        ordering = ['created_at']
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'