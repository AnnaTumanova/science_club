from django import forms
from forum.entities import Thread, Post


class ThreadForm(forms.ModelForm):
    subject = forms.CharField(
        label="Subject",
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    content = forms.CharField(
        label="Content",
        strip=True,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Thread
        fields = ('subject', 'content')


class PostForm(forms.ModelForm):
    content = forms.CharField(
        label="Content",
        strip=True,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Post
        fields = ('content',)
