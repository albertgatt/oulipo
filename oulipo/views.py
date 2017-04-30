from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from base.Generator import StoryMaker
import re
# Create your views here.
# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'oulipo/index.html'
    
class AboutView(generic.TemplateView):
    template_name = 'oulipo/about.html'
    
def _check_or_none(d, k):
    if k in d:
        return d[k]
    return None
        
def generate_story(request):
    sm = StoryMaker()    
    char1 = sm.build_character(gender=_check_or_none(request.POST, 'gender1'), girth=_check_or_none(request.POST,'girth1'), height=_check_or_none(request.POST, 'height1'), agerange=_check_or_none(request.POST, 'age1'))
    char2 = sm.build_character(gender=_check_or_none(request.POST, 'gender2'), girth=_check_or_none(request.POST,'girth2'), height=_check_or_none(request.POST, 'height2'), agerange=_check_or_none(request.POST, 'age2'))
    
    sub_temp = None
    main_temp = 'basic-story.txt'
    
    if 'subtemplate' in request.POST and request.POST['subtemplate']=='yes':
        story = sm.make_story('embedded', char1, char2)
    else:
        story = sm.make_story('simple', char1, char2)
    
    
    context = {'story': story}
    return render(request, 'oulipo/generate.html', context)