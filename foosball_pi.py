#!/usr/bin/env python2.7  
#script by Anthony Pino anthony_p1234@yahoo.com
import random
#import RPi.GPIO as GPIO  #include this later when on the PI
import glob #for listing all the files in a directory
import pygame
import sys
import os
from extras import Button

##SET GPIO to trigger on a low voltage 
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#GPIO.add_event_detect(23,GPIO.FALLING)
#GPIO.add_event_callback(23,red_score_interupt,1000) #debounce 1 second
#GPIO.add_event_detect(24,GPIO.FALLING)
#GPIO.add_event_callback(24,black_score_interupt,1000) #debounce 1 second

pygame.init()
pygame.mixer.init()
myfont = pygame.font.SysFont("monospace", 80)  #initialize system font

DISPLAY_SIZE = (400, 240)
RED_TEXT = (int(DISPLAY_SIZE[0]/3)-30,20)  ###Align score text to display
BLACK_TEXT = (int(DISPLAY_SIZE[0]*2/3)-30, 20)  ###Align score text to display
FPS = 60

PERCENTAGE_GOAL_VIDEO_PLAY = 0.7
PERCENTAGE_PENALTY_VIDEO_PLAY = 0.2

BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)
RED       = (255,0,0)
GREEN     = (0,255,0)

##First co-ord is x, second is y)
RED_BTN_CO = (80,125,90,30)
RED_BTN_TEXT = (RED_BTN_CO[0]+3,RED_BTN_CO[1]+3)
RED_PEN_CO = (RED_BTN_CO[0],RED_BTN_CO[1]+40,90,30)
RED_PEN_TXT = (RED_PEN_CO[0]+3,RED_PEN_CO[1]+3)


BLACK_BTN_CO = (225,125,90,30)
BLACK_BTN_TEXT = (BLACK_BTN_CO[0]+3,BLACK_BTN_CO[1]+3)
BLACK_PEN_CO = (BLACK_BTN_CO[0],BLACK_BTN_CO[1]+40,90,30)
BLACK_PEN_TXT = (BLACK_PEN_CO[0]+3,BLACK_PEN_CO[1]+3)

####
##Start the screen
# Initialise screen
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('Fe')
screen.fill(LIGHTGRAY)
pygame.display.flip() 

##directories
penalty_vid_dir = "./soccer/penaltyvid/"
goal_vid_dir = "./soccer/goalvid/"
start_vid = "./soccer/startvid/"
picture_dir = "./soccer/picture/*.jpg"
music_dir = "./soccer/music/*.mp3"
end_vid_dir = "./soccer/endvid/*.mpg"

###
#Create lists of files in these paths
penalty_videos = glob.glob(penalty_vid_dir + "*.mpg")
goal_videos = glob.glob(goal_vid_dir + "*.mpg")
start_videos = glob.glob(start_vid + "*.mpg")
pictures  = glob.glob(picture_dir)
music = glob.glob(music_dir)
end_vid = glob.glob(end_vid_dir)

#####
#Set the scores
red_score = 0
black_score = 0  


#######
#The buttons defined in extras.py
red_button = Button('Red Goal','RED')
black_button = Button('Black Goal','GREEN')
red_penalty_btn = Button('Red Penalty','RED')
black_penalty_btn = Button('Black Penalty','GREEN')



######
#DEFINE A bunch of functions

def random_chance(percentage_play):
  random_number = random.randint(1, 10)
  percentage = int(percentage_play*10)
  if( random_number < percentage):
    return true
  return false

##define what to do on interupt event
def red_score_interupt():
    red_score = red_score+1
    play_vid(goal_videos)  
    return
    
def red_score_interupt():
    black_score = black_score+1
    play_vid(goal_videos)
    return


def score_check(score_red,score_black):
  who_won = ""
  if( score_red >=5 and score_red - score_black >=2):
    who_won = "red"
  if( score_black >=5 and score_black - score_red >=2):
    who_won = "black"  
  if( score_red == 8):
    who_won = "red"
  if( score_black == 8):
    who_won = "black" 
  return who_won 

def render_backgorund():
  surface_image = pygame.image.load(pictures[0])
  surface_image = pygame.transform.scale(surface_image, DISPLAY_SIZE)
  screen.blit(surface_image,(0,0))     ##surface_image.convert(screen)
  red_button.draw(screen, mouse, RED_BTN_CO, RED_BTN_TEXT)
  black_button.draw(screen, mouse, BLACK_BTN_CO, BLACK_BTN_TEXT)
  red_penalty_btn.draw(screen, mouse, RED_PEN_CO, RED_PEN_TXT)
  black_penalty_btn.draw(screen, mouse, BLACK_PEN_CO, BLACK_PEN_TXT)
  pygame.display.flip() 

def play_sound(sound_list):
  pygame.mixer.init()
  pygame.mixer.music.load(random.choice(sound_list))
  pygame.mixer.music.set_volume(1)
  pygame.mixer.music.play(0)

#function to restart the program
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def draw_score(score_red,score_black):
    score_text_red = myfont.render(score_red, 1, RED)  
    score_text_black = myfont.render(score_black, 1, GREEN)  
    screen.blit(score_text_red, RED_TEXT)
    screen.blit(score_text_black, BLACK_TEXT)
    pygame.display.flip() 
  
def play_vid(video_list):
    pygame.mixer.quit() #stop the mixer, so that the video can play
    movie = pygame.movie.Movie(random.choice(video_list))
    #movie = pygame.transform.scale(movie, DISPLAY_SIZE)  
    #screen = pygame.display.set_mode(DISPLAY_SIZE)   ###normally movie.get_size()
    movie_screen = pygame.Surface(DISPLAY_SIZE).convert() ##normally movie.get_size()
    movie.set_display(screen,(0,0,DISPLAY_SIZE[0],DISPLAY_SIZE[1]))  ##was movie_screen
    pygame.display.flip() 
    print "playing movie"
    movie.play()
    pygame.mixer.init() #start mixer for the sounds again
    return

def red_wins():
  #red wins code here
  play_vid(end_vid)
  return
  
def black_wins():
  #black wins code here
  play_vid(end_vid)
  return  
    
#play start vid
play_vid(start_videos)

done = False
pygame.mixer.init()
mouse = pygame.mouse.get_pos()
clock = pygame.time.Clock()
##Start an endless loop
while not done:
  #draw scores on screen
  clock.tick(60)
  mouse = pygame.mouse.get_pos()
  
  
  ##Check for music playing, if not play something
  if not pygame.mixer.music.get_busy():
    play_sound(music)
 
  
  render_backgorund()  
  draw_score(str(red_score),str(black_score))
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
            run = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      if red_button.obj.collidepoint(mouse):
        red_score = red_score +1
      elif black_button.obj.collidepoint(mouse):
        black_score = black_score +1
      if red_penalty_btn.obj.collidepoint(mouse):
        red_score = red_score -1
      elif black_penalty_btn.obj.collidepoint(mouse):
        black_score = black_score -1
  #my_input = raw_input("What's your selection?: ")
  my_input = ""
  
  ##Replace these with button presses eventually  
  if my_input == "RESTART":
    restart_program()
    continue
  if my_input == "BLACK":
    #play_vid(goal_videos)
    play_sound(music)
    black_score = black_score +1
    print "Updating Black"
    
  if my_input == "RED":
    #play_vid(goal_videos)
    play_sound(music)
    red_score = red_score +1
    
  if my_input == "RED_DOWN":   
    #play_vid(penalty_videos)
    play_sound(music)
    red_score = red_score -1   
  if my_input == "BLACK_DOWN":   
    #play_vid(penalty_videos)
    play_sound(music)
    
    red_score = black_score -1   
 
  if(score_check(red_score,black_score) == "black" ):
    black_wins()
    done = True
    
  if(score_check(red_score,black_score) == "red" ):
    red_wins()  
    done = True

  #check make sure scores arent too small
  if(red_score < 0):
    red_score = 0
  if(black_score <0):
    black_score =0
    
  
    

#cleanup everything
#GPIO.cleanup()
restart_program()





