from django import forms
from .models import Blog

class CreateBlogForm(forms.ModelForm):
    is_draft        = forms.BooleanField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Blog
        fields = ["title", "body", "image","is_draft"]

    def clean_is_draft(self):
        if 'publish' in self.data:
            is_draft = self.cleaned_data['is_draft']
            is_draft = False
            return is_draft
        
        elif 'save_draft' in self.data:
            is_draft = self.cleaned_data['is_draft']
            is_draft = True
            return is_draft


# Update Blog post form
class UpdateBlogForm(forms.ModelForm):
    is_draft        = forms.BooleanField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Blog
        fields = ["title", "body", "image","is_draft"]

    def clean_is_draft(self):
        if 'publish' in self.data:
            is_draft = self.cleaned_data['is_draft']
            is_draft = False
            return is_draft
        
        elif 'save_draft' in self.data:
            is_draft = self.cleaned_data['is_draft']
            is_draft = True
            return is_draft
    
    def save(self, commit=True):
        blog            = self.instance
        blog.title      = self.cleaned_data['title']
        blog.body       = self.cleaned_data['body']

        if self.cleaned_data['image']:
            blog.image = self.cleaned_data['image']
        
        if commit:
            blog.save()
        
        return blog
