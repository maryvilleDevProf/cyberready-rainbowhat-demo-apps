#!/usr/bin/env python3

from random import *
import rainbowhat
from time import *
import colorsys

# Twinkle, Twinkle little star
# https://www.midikits.net/midi_analyser/midi_note_numbers_for_octaves.htm
notes = [
    72, 72, 79, 79, 81, 81, 79,
    77, 77, 76, 76, 74, 74, 72
]
times = [
    500, 500, 500, 500, 500, 500, 1000,
    500, 500, 500, 500, 500, 500, 1000
]


class DemoState:
    def __init__(self):
        self.scroll_message_flag = False
        self.play_tune_flag = False
        self.light_show_flag = False
    
    def scroll_message( self ):
        self.stopAll()
        self.scroll_message_flag = True
    
    def play_tune( self ):
        self.stopAll()
        self.play_tune_flag = True
    
    def do_light_show( self ):
        self.stopAll()
        self.light_show_flag = True
        
    def stopAll( self ):
        self.scroll_message_flag = False
        self.play_tune_flag = False
        self.light_show_flag = False

state = DemoState()

def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()

@rainbowhat.touch.A.press()
def start_scrolling_message(channel):
    state.scroll_message()
    rainbowhat.lights.rgb(1,0,0)
    
@rainbowhat.touch.B.press()
def start_light_show(channel):
    state.do_light_show()
    rainbowhat.lights.rgb(0,1,0)
    
@rainbowhat.touch.C.press()
def start_play_tune(channel):
    state.play_tune()
    rainbowhat.lights.rgb(0,0,1)

def main():  
    scroll_message = "   RITENOUR CYBER    "
    scroll_index = 0
    is_scrolling = False
    
    note_index = 0
    last_time = 0
    current_time = 0

    while True:
        # Control block for scrolling message
        if state.scroll_message_flag:
            if is_scrolling:
                display_message( scroll_message[scroll_index: scroll_index + 4])
                scroll_index = (scroll_index + 1) % len( scroll_message )
            else:
                display_message( scroll_message[0:4] )
                scroll_index += 1
                is_scrolling = True
            
            sleep(.2)
            
        else:
            scroll_index = 0
            is_scrolling = False
            display_message('    ')
        
        # Control block for the random light show
        if state.light_show_flag:
            led = randrange(0, 7)
            hue = randrange(0, 361)
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)]
            rainbowhat.rainbow.set_pixel( led, r, g, b )
            #rainbowhat.rainbow.set_all( r, g, b)
            rainbowhat.rainbow.show()
            sleep(.1)
        else:
            rainbowhat.rainbow.set_all( 0, 0, 0)
            rainbowhat.rainbow.show()
        
        # Control block for playing the tune
        if state.play_tune_flag:
            if time() > last_time + current_time:
                current_note = notes[note_index]
                current_time = times[note_index] / 1000.0
                current_time += 0.1
                note_index += 1
                note_index %= len(notes)
                last_time = time()
                if current_note == 128 or current_time == 0:
                    pass
                    #rainbowhat.buzzer.stop()
                    #print("Note Off")
                else:
                    rainbowhat.buzzer.midi_note(current_note, current_time*0.9)
                    #print("Playing Note: {}".format(current_note))
        else:
            rainbowhat.buzzer.stop()
            note_index = 0
            last_time = 0
               
            
try:
    main()
except KeyboardInterrupt:
    pass
