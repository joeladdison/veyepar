# forms.py

from django import forms

from main.models import Episode, Location


class Who(forms.Form):
    locked_by = forms.CharField(max_length=32, required=True,
            label="Please enter your name")

class Location_Form(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ['active',]


class Episode_Form_Preshow(forms.ModelForm):
    authors = forms.CharField(max_length=255, required=False)
    emails = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        locations = kwargs.get('locations', Location.objects.all())
        if 'locations' in kwargs:
           del kwargs['locations']
        super(Episode_Form_Preshow, self).__init__(*args, **kwargs)
        self.fields['location']._set_choices([(l.id, l.name) for l in locations])

    class Meta:
        model = Episode
        fields = ('sequence',
                  'name', 'slug',
                  'show','location',
                  'start', 'duration',
                  'authors',
                  'emails',
                  'released',
                  'description',
                  'summary',
                  'tags',
                  'twitter_id',
                  'language',
                  )

class Episode_Form_small(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ('state', 'locked', 'locked_by', 'start', 'duration',
                  'name',
                  'emails',
                  'released',
                  'normalise', 'channelcopy',
                  'thumbnail', 'description', 'comment')

class Episode_Form_Mini(forms.ModelForm):
    emails = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Episode
        fields = ('name',
                  'emails',
                  'description',
                  'comment',
                  'start','end',
                  )
        widgets = {
        	'meails': forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }

class clrfForm(forms.Form):
    clid = forms.IntegerField(widget=forms.HiddenInput())
    trash = forms.BooleanField(label="Trash",required=False)
    apply = forms.BooleanField(label="Apply",required=False)
    split = forms.BooleanField(label="Split",required=False)
    sequence = forms.IntegerField(label="Sequence",required=False,
      widget=forms.TextInput(attrs={'size':'3','class':'suSpinButton'}))
    start = forms.CharField(max_length=12,label="Start",required=False,
      help_text = "offset from start in h:m:s or frames, blank for start",
      widget=forms.TextInput(attrs={'size':'9'}))
    end = forms.CharField(max_length=12,label="End",required=False,
      help_text = "offset from start in h:m:s or frames, blank for end",
      widget=forms.TextInput(attrs={'size':'9'}))
    rf_comment = forms.CharField(label="Raw_File comment",required=False,
      widget=forms.Textarea(attrs={'rows':'2','cols':'20'}))
    cl_comment = forms.CharField(label="Cut_List comment",required=False,
      widget=forms.Textarea(attrs={'rows':'2','cols':'20'}))

class Add_CutList_to_Ep(forms.Form):
    rf_filename = forms.CharField(max_length=132,required=False,
      help_text = "root is .../show/dv/location/, example: 2013-03-13/13:13:30.dv" )
    sequence = forms.IntegerField(label="Sequence",required=False,
      widget=forms.TextInput(attrs={'size':'3','class':'suSpinButton'}))
    getit = forms.BooleanField(label="get this", required=False,
            help_text="check and save to add this")

class AddImageToEp(forms.Form):
    image_id = forms.IntegerField(widget=forms.HiddenInput())
    episode_ids  = forms.CharField(max_length=35, required=False,)

class AddEpisodeToRaw(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ('name',
                'duration',
               # 'comment',
                )
    raw_id = forms.IntegerField(widget=forms.HiddenInput())


class MarkPicker(forms.Form):
    apply = forms.BooleanField(label="Apply",required=False)
    click = forms.CharField(max_length=19,label="Start",required=False,
      widget=forms.TextInput(attrs={'size':'15'}))


