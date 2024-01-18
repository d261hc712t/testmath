import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

class CircularProgressBar(Slider):
   def __init__(self, **kwargs):
       super(CircularProgressBar, self).__init__(**kwargs)
       self.min = 0
       self.max = 100
       self.value = 0

   def on_value(self, instance, value):
       if value >= 100:
           Clock.schedule_once(lambda dt: self.parent.manager.current == 'calculator')

class Calculator(Screen):
   def __init__(self, **kwargs):
       super(Calculator, self).__init__(**kwargs)
       self.operators = ["/", "*", "+", "-"]
       self.last_was_operator = None
       self.last_button = None

       main_layout = BoxLayout(orientation="vertical")
       self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=55)
       main_layout.add_widget(self.solution)

       buttons = [["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], [".", "0", "C", "+"]]
       for row in buttons:
           h_layout = BoxLayout()
           for label in row:
               button = Button(text=label, pos_hint={"center_x": 0.5, "center_y": 0.5})
               button.bind(on_press=self.on_button_press)
               h_layout.add_widget(button)
           main_layout.add_widget(h_layout)

       equals_button = Button(text="=", pos_hint={"center_x": 0.5, "center_y": 0.5})
       equals_button.bind(on_press=self.on_solution)
       main_layout.add_widget(equals_button)

       self.add_widget(main_layout)

   def on_button_press(self, instance):
       current = self.solution.text
       if instance.text == "C":
           self.solution.text = ""
       elif instance.text in self.operators:
           if self.last_button in self.operators:
               self.solution.text = current[:-1] + instance.text
           else:
               self.solution.text += instance.text
       else:
           self.solution.text += instance.text
       self.last_button = instance.text

   def on_solution(self, instance):
       current = self.solution.text
       if self.last_button in self.operators:
           result = eval(current)
           self.solution.text = str(result)
       else:
           self.solution.text += "=" + str(eval(current))
       self.last_button = "="

class MainApp(App):
   def build(self):
       sm = ScreenManager()
       sm.add_widget(CircularProgressBar(name='progress'))
       sm.add_widget(Calculator(name='calculator'))
       return sm

if __name__ == '__main__':
   MainApp().run()
