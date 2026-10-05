from django import forms
from .models import Post, Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        # unlike forms, for modelforms widgets are declared in widget dictionary inside Meta class
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }