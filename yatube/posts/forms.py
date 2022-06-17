from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма создания новой публикации."""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

        help_texts = {
            'text': 'Текст публикации',
            'group': 'Группа публикации',
        }

        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Введите текст публикации',
                    'class': 'form-control',
                }
            ),
            'group': forms.Select(
                attrs={'class': 'form-control'}
            )
        }


class CommentForm(forms.ModelForm):
    """Форма создания нового комментария."""

    class Meta:
        model = Comment
        fields = ('text',)

        help_texts = {
            'text': 'Добавить комментарий: ',
        }

        widgets = {
            'text': forms.Textarea(
                attrs={
                    'placeholder': 'Введите текст комментария',
                    'class': 'form-control',
                }
            ),
        }
