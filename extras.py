#!/usr/bin/env python2.7  

import pygame

RED       = (255,0,0)
GREEN     = (0,255,0)


class Button:
  def __init__(self, text, new_colour):
      self.text = text
      self.is_hover = False
      self.default_color = (100,100,100)
      self.hover_color = (255,255,255)
      self.font_color = (0,0,0)
      self.obj = None
      if(new_colour == "GREEN"):
        self.default_color = GREEN
      if(new_colour == "RED"):
        self.default_color = RED     
      #####Anthony additions

  def label(self):
      '''button label font'''
      font = pygame.font.Font(None, 20)
      return font.render(self.text, 1, self.font_color)
      
  def color(self):
      '''change color when hovering'''
      if self.is_hover:
        return self.hover_color
      else:
        return self.default_color
         
  def draw(self, screen, mouse, rectcoord, labelcoord):
      '''create rect obj, draw, and change color based on input'''
      self.obj  = pygame.draw.rect(screen, self.color(), rectcoord)
      screen.blit(self.label(), labelcoord)
      
      #change color if mouse over button
      self.check_hover(mouse)
 
  def draw_nice(self, screen, mouse, rectcoord, labelcoord):
      '''create rect obj, draw, and change color based on input'''
      #self.obj  = pygame.draw.rect(screen, self.color(), rectcoord)
      self.obj = pygame.draw.ellipse(screen, self.color(), rectcoord) 
      screen.blit(self.label(), labelcoord)     
      #change color if mouse over button
      self.check_hover(mouse)
      
  def check_hover(self, mouse):
      '''adjust is_hover value based on mouse over button - to change hover color'''
      if self.obj.collidepoint(mouse):
        self.is_hover = True 
      else:
        self.is_hover = False