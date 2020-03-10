from django import forms
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,

)
from .models import Post,  Comment
from django.contrib.auth.models import User



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),


        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)



class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':2, 'cols':15}),

)

    # the new bit we're adding
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label="Your name:"
        self.fields['contact_email'].label ="Your email:"
        self.fields['content'].label ="What do you want to say?"
