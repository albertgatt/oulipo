'''
Created on 18 Sep 2015

@author: albertgatt
'''
from random import choice
from base.BaseClasses import *
import Lexicon.wordlists as schema
from Lexicon.utils import TimeHelper, ArticleHelper, VerbConjugator,OrthographyHelper, ExpressionChooser,\
    NPHelper
from jinja2 import Template, Environment, PackageLoader


class Story(object):
    def __init__(self, setting, development, conc=None):
        self.env = Environment(loader=PackageLoader('base', 'storygrammars'), lstrip_blocks=True, trim_blocks=True)
        self.setting = setting
        self.development = development
        self.conclusion = conc
        self.embedded = False

    def get_setting(self):
        return self.env.get_template("1.setting.txt").render(setting=self.setting,     
                           time=TimeHelper(), art=ArticleHelper(), vc=VerbConjugator(), orth=OrthographyHelper(),
                           exp=ExpressionChooser(), np=NPHelper()) 

    def get_development(self):
        return self.env.get_template("2.development.txt").render(setting=self.setting, development=self.development,     
                           time=TimeHelper(), art=ArticleHelper(), vc=VerbConjugator(), orth=OrthographyHelper(),
                           exp=ExpressionChooser(), np=NPHelper()) 
        
    def get_conclusion(self):
        return self.env.get_template("4.conclusion.txt").render(setting=self.setting, development=self.development,     
                           time=TimeHelper(), art=ArticleHelper(), vc=VerbConjugator(), orth=OrthographyHelper(),
                           exp=ExpressionChooser(), np=NPHelper()) 
        

class EmbeddedStory(Story):    
    def __init__(self, setting, development, flashback,embedded, conc=None):        
        super().__init__(setting, development, conc)
        self.flashback = flashback
        self.env = Environment(loader=PackageLoader('base', 'storygrammars'), lstrip_blocks=True, trim_blocks=True)
        self.substory = embedded
        self.embedded = True
        
    def get_switchback(self):
        return self.env.get_template("6.switchback.txt").render(setting=self.setting, development=self.development,   
                           time=TimeHelper(), art=ArticleHelper(), vc=VerbConjugator(), orth=OrthographyHelper(),
                           exp=ExpressionChooser(), np=NPHelper()) 
        
    def get_flashback(self):
        return self.env.get_template("5.flashback.txt").render(setting=self.setting, development=self.development,
                           flashback=self.flashback,     
                           time=TimeHelper(), art=ArticleHelper(), vc=VerbConjugator(), orth=OrthographyHelper(),
                           exp=ExpressionChooser(), np=NPHelper()) 
        
    def get_embedded_story(self):
        return self.substory.get_setting() + self.substory.get_development() + self.substory.get_conclusion()
        
    

class StoryMaker(object):

    def random_time(self):
        hr = choice(range(0,24))
        minute = choice(range(0,60))
        month = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        day = choice(range(1,20))
        time = datetime.datetime(2015, month, day, hr, minute)
        return time    


    def build_character(self, gender=None, girth=None, height=None, agerange=None):
        if girth is None:
            girth = choice(schema.girth_synsets)
        elif girth.startswith('fat'):
            girth = 'fat.a.01'
        elif girth.startswith('thin'):
            girth = 'thin.a.01'
        else:
            raise RuntimeError("Unknown value for girth: " + girth)
            
        if height is None:
            height = choice(schema.height_synsets)
        elif height.startswith('tall'):
            height = 'tall.a.01'
        elif height.startswith('short'):
            height = 'short.a.01'
        else:
            raise RuntimeError("Unknown value for height: " + height)

        age = None
        if agerange is None:
            age = choice(range(20, 60))
        elif agerange == 'young':
            age = choice(range(18,35))
        elif agerange == 'middle':
            age = choice(range(35, 50))
        elif agerange == 'old':
            age = choice(range(50,70))
        else:
            raise RuntimeError("Unknown value for agerange: " + agerange)
        
              
        if gender is None:    
            gender = choice(['male', 'female'])
        if gender == 'male':
            name = choice(schema.male_names)
        else:
            name = choice(schema.female_names)
        
        p =  Person(Roles.THEME, name, gender, age)
        
        p.add_attribute('girth', girth)
        p.add_attribute('height', height)
        return p

    def build_activity(self, someperson, sometime):
        verb = choice(schema.activities)
        location = Location(choice(schema.locations))
        event = Event(verb, False)
        event.time = sometime
        event.add_arg(someperson)
        event.add_arg(location)
        return event

    def build_event(self, someperson, verbs=schema.actions):
        verb = choice(verbs)
        event = Event(verb, False)
        event.add_arg(someperson)
        return event

    def build_comm_event(self, someperson):
        ev = self.build_event(someperson, verbs=schema.comm_verbs)
        o = choice(schema.comm_objects)
        e = Entity(Roles.UTTERANCE, o)
        ev.add_arg(e)
        return ev

    def make_time_expression(self, time):
        '''Makes a time expression out of a datetime for an event, returning the string'''   
        month = time.month
        hr = time.hour
        adjective = None
        monthname = schema.months[month-1]
        
        if month in range(1, 4) or month == 12:
            adjective = choice(schema.winter)
        elif month in range(4, 6):
            adjective = choice(schema.spring)
        elif month in range(6, 9):
            adjective = choice(schema.summer)
        else:
            adjective = choice(schema.autumn)
            
        period_index = list(filter(lambda x: hr >= schema.times[x] and hr < schema.times[x+1], range(0, len(schema.times)-2)))[0]
        period = schema.periods[period_index].substitute(ADJ=adjective)
        time_string = schema.time1.substitute(PERIOD = period, MONTH=monthname)
        return time_string
    
    def mirror_character(self, char):
        agerange = char.age
        gender = char.gender
        girth = char.get_attribute('girth')
        height = char.get_attribute('height')
        return self.build_character(gender, girth, height, 'young')

    def make_story(self, storytype, char1, char2):
        '''Build a story structure'''
        
        #1.First determine the time
        t = self.random_time()
                    
        #3. The setting and initial activity
        initial_activity = self.build_activity(char1, t)
        
        #4. The development
        devel = self.build_event(char2)
        
        #5. The flashback
        flash = self.build_comm_event(char2)
        
        #6. the substory
        story2 = None
        if storytype=='embedded':
            story2 = self.make_story('simple', self.mirror_character(char1), self.mirror_character(char2))
            return EmbeddedStory(setting=initial_activity, development=devel, flashback=flash, embedded=story2)
        else:           
            return Story(setting=initial_activity, development=devel)
        

        
        