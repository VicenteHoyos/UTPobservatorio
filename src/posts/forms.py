from django import forms
from datetime import date
from .models import Post, Interes

class InteresForm(forms.ModelForm):
    class Meta:
        model = Interes
        
        fields ={
            "nombre",
            "descripcion",
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'imagen', "contenido", 'publish')
        widgets = {
            'publish': forms.SelectDateWidget(),
            }
         # widgets = {
        #      'categorias': forms.CheckboxSelectMultiple(),
        #  }

    def clean_publish(self):
        publish = self.cleaned_data.get("publish")
        if publish < date.today():
            raise forms.ValidationError("La fecha de publicación no puede ser menor a la fecha del sistema")
        else:
            return publish
       
   
    categorias = forms.ModelMultipleChoiceField(queryset=Interes.objects.all())

    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categorias'] = [t.pk for t in 
                kwargs['instance'].interes_set.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.categorias.clear()
            for interes in self.cleaned_data['categorias']:
                instance.categorias.add(interes)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        #if commit:
        instance.save()
        self.save_m2m()

        return instance

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'imagen', "contenido",'publish')    
        # widgets = {
        #      'categorias': forms.CheckboxSelectMultiple(),
        #  }
        widgets = {
            'publish': forms.SelectDateWidget(),
            }
    
    categorias = forms.ModelMultipleChoiceField(queryset=Interes.objects.all())

    def clean_publish(self):
        publish = self.cleaned_data.get("publish")
        if publish < date.today():
            raise forms.ValidationError("La fecha de publicación no puede ser menor a la fecha del sistema")
        else:
            return publish
            
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            # We get the 'initial' keyword argument or initialize it
            # as a dict if it didn't exist.
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categorias'] = [t.pk for t in 
                kwargs['instance'].categorias.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):
        # Get the unsaved Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            instance.categorias.clear()
            for interes in self.cleaned_data['categorias']:
                instance.categorias.add(interes)

        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        #if commit:
        instance.save()
        self.save_m2m()

        return instance


