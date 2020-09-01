# '''
# Created on 16 Sep 2015
#
# @author: albertgatt
# '''
# from tkinter import *
# from tkinter import ttk
# from base.Generator import StoryMaker
# import re
#
# #------------------------------- subjects = ['John', 'Pete', 'Alyssa', 'Daphna']
# #----------------------------------------- objects = ['shop', 'bar', 'boutique']
# #------------------------------------------------------ verbs = ['open', 'walk']
# #-------------------------------- locations = ['Valletta', 'Sliema', 'New York']
# #------------------------------------------------------------------------------
# #---------------- s = Entity(Roles.AGENT, random.choice(subjects), common=False)
# #----------------------------------------------- e = Event(random.choice(verbs))
# #---------------- o = Entity(Roles.PATIENT, random.choice(objects), common=True)
# #---------------------------------- l = Location(random.choice(locations), "in")
# #------------------------------------------------ schema = EventSchema(e,s,o, l)
#
# class StoryApp(ttk.Frame):
#
#     def __init__(self, master=None):
#         super().__init__(master, padding="3 3 12 12")
#         self.grid(column=0, row=0, sticky=(N,W,E,S))
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(0, weight=1)
#         #heading = StringVar()
#         #self.pack()
#         #self.create_widgets()
#
#     def create_widgets(self):
#
#         self.generate = Button(self)
#         self.generate["text"] = "Generate story"
#         self.generate["command"] = self.generate_story
#         self.generate.pack(side="top")
#         self.quit = Button(self, text="Quit", fg="red", command=root.destroy)
#         self.quit.pack(side="bottom")
#
#
#     def generate_story(self):
#         sm = StoryMaker()
#         char1 = sm.build_character(gender='male', girth='fat', height='tall', agerange='old')
#         char2 = sm.build_character(gender='female', girth='thin', height='short', agerange='young')
#         story = sm.make_story('embedded-story.txt', char1, char2, subtemplate='basic-story.txt')
#         story = re.sub("[\s\n]+"," ", story)
#         print(story)
#
# if __name__ == '__main__':
#     sm = StoryMaker()
#     char1 = sm.build_character(gender='male', girth='fat', height='tall', agerange='old')
#     char2 = sm.build_character(gender='female', girth='thin', height='short', agerange='young')
#     story = sm.make_story('embedded-story.txt', char1, char2, subtemplate='basic-story.txt')
#     story = re.sub("[\s\n]+"," ", story)
#     print(story)
#     #root = Tk()
#     #root.title("Oulipo: Story Generator")
#     #app = StoryApp(master=root)
#     #app.mainloop()
#