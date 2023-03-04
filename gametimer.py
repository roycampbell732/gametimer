import pygame
from pygame.constants import (KEYDOWN)
import sys
import time
import datetime
import os
import json
import pandas as pd


configFile = 'config_app.json'
path = f"./{configFile}"
missingConfig = ' \
\n \
*** Error: Config File Missing \n \
There must be a "config_app.json" file in the application directory \
\n \
'

configExist = os.path.lexists(path)
if configExist:
    with open(configFile, 'r') as jsonFile:
        # config = pd.read_json(jsonFile)
        config = json.loads(jsonFile.read())
else:
    print(missingConfig)
    exit()


config_df = pd.DataFrame.from_dict(config, orient='index')
print(config_df[0]['ClockDelayFirstGame'])


def config_array(string):
    print("config_array", string)
    var_array = string.split(":")
    return var_array


def time_setup(time_array):
    print("time_setup", time_array)
    timer_secs = (int(time_array[0]) * 60 * 60) + (int(time_array[1]) * 60) + int(time_array[2])
    return timer_secs


# set up application constants
SECOND = pygame.USEREVENT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (83, 145, 223)
YELLOW = (255, 239, 40)
gameSecs = time_setup(config_array(config_df[0]['GameTime']))
delaySecs = time_setup(config_array(config_df[0]['ClockDelayBetweenGames']))
delaySecsFG = time_setup(config_array(config_df[0]['ClockDelayFirstGame']))
warningSecs = time_setup(config_array(config_df[0]['ClockWarning']))
endingSecs = time_setup(config_array(config_df[0]['ClockEnding']))
startSoundFile = config_df[0]['StartSound']
endSoundFile = config_df[0]['EndSound']
endOfGameWarningSoundFile = config_df[0]['EndOfGameWarningSound']
countdownSoundFile = config_df[0]['CountdownSound']
soundPath = f"./{config_df[0]['AssetPath']}/{config_df[0]['SoundsPath']}"
startSound = f"{soundPath}/{startSoundFile}"
endSound = f"{soundPath}/{endSoundFile}"
endOfGameWarningSound = f"{soundPath}/{endOfGameWarningSoundFile}"
countdownSound = f"{soundPath}/{countdownSoundFile}"
soundVolume = config_df[0]['Volume']
volume = int(soundVolume) / 10
print("Volume", volume)
pygame.mixer.init()
delayRunning = False
soundPlayed = False
warningPlayed = False
endingPlayed = False
soundsPlayed = [delayRunning, soundPlayed, warningPlayed, endingPlayed]
width = 75
height = 75
frameCount = 0
frameRate = 60
clock = pygame.time.Clock()


# Set up Globals from json config_app file
# EventName =             df[0]['EventName']
# Location =              df[0]['Location']
# SiteName =              df[0]['SiteName']
# Sanctioned =            df[0]['Sanctioned']
# Browser =               df[0]['Browser']
# EventType =             df[0]['EventType']
# Wallpaper =             df[0]['Wallpaper']
# BackgroundColor =       df[0]['BackgroundColor']
# ClockFont =             df[0]['ClockFont']
# ClockColor =            df[0]['ClockColor']
# ClockColorDelay =       df[0]['ClockColorDelay']
# EventLogo =             df[0]['EventLogo']
# GameTime =              df[0]['GameTime']
# DelayBetweenGames =     df[0]['DelayBetweenGames']
# ScheduledStartTime =    df[0]['ScheduledStartTime']
# StartSound =            df[0]['StartSound']
# EndSound =              df[0]['EndSound']
# EndOfGameWarningSound = df[0]['EndOfGameWarningSound']
# CountdownSound =        df[0]['CountdownSound']
# start timer
pygame.init()
screenSize = pygame.display.get_desktop_sizes()

screenWidth = screenSize[0][0]
screenHeight = screenSize[0][1]
print(screenWidth)
print(screenHeight)
if screenWidth > 1000:
    windowW = int(screenWidth * (width / 100))
    windowH = int(screenHeight * (height / 100))
else:
    windowW = int(screenWidth)
    windowH = int(screenHeight)

print(windowW, windowH)
print(type(windowW), type(windowH))
screen = pygame.display.set_mode([windowW, windowH])
timeFont = pygame.font.SysFont("Arial", int(windowH/2))
helpFont = pygame.font.SysFont("Arial", 18)
screen.fill(BLACK)
pygame.time.set_timer(SECOND, 1000)
minutes = 0
seconds = 0
gameRunning = False
pauseTimerPlaying = False

timerCount = 0
oldTimerCount = 0
running = True
paused = False
secs = delaySecsFG
minutes = secs // 60
seconds = secs % 60
prevSec = secs + 1
color = config_df[0]['ClockColorDelayFirstGame']



def timerSwitchSound(secs, gameRunning, timerCount, soundsPlayed):
    delayRunning, soundPlayed, warningPlayed, endingPlayed = soundsPlayed
    if (timerCount == 0 or (timerCount %2 == 0 and secs == delaySecs)) and not delayRunning:
        delayRunning = True
        soundPlayed = False
        warningPlayed = False
        endingPlayed = False

        delayVolume = volume / 2
        # pygame.mixer.Sound.set_volume(countdownSound, 0.2)
        pygame.mixer.music.load(countdownSound)
        pygame.mixer.music.set_volume(delayVolume)
        pygame.mixer.music.play(loops=-1)
    if gameRunning:
        delayRunning = False
        if secs == gameSecs and timerCount % 2 == 1 and not soundPlayed:
            print("sound start")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.load(startSound)
            pygame.mixer.music.play(loops=1)
            soundPlayed = True
        if secs == warningSecs and timerCount % 2 == 1 and not warningPlayed:
            pygame.mixer.Sound.set_volume(volume)
            pygame.mixer.music.load(endOfGameWarningSound)
            pygame.mixer.music.play(loops=1)
            warningPlayed = True
        if secs == 0 and timerCount % 2 == 1 and not endingPlayed:
            pygame.mixer.Sound.set_volume(volume)
            pygame.mixer.music.load(endSound)
            pygame.mixer.music.play(loops=1)
            endingPlayed = True
        print("playing sound")

    return delayRunning, soundPlayed, warningPlayed, endingPlayed


def timerSwitch(prevSec, secs, gameRunning, timerCount):
    if secs == 0 and prevSec == 1:
        gameRunning = not gameRunning
        timerCount += 1
        if gameRunning:
            secs = gameSecs + 1
        else:
            secs = delaySecs + 1
    return secs, gameRunning, timerCount


def gameClockColor(secs):
    if warningSecs > secs > endingSecs:
        color = config_df[0]['ClockColorWarning']
    elif secs <= endingSecs:
        color = config_df[0]['ClockColorEnding']
    else:
        color = config_df[0]['ClockColor']
    return color


while running:
    print(timerCount, secs)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            paused = not paused
            print("Paused", paused)
            if pygame.key.name(event.key) == 'space':
                print("space")
            if pygame.key.name(event.key) == 'return':
                print("return")
            if pygame.key.name(event.key) == 'escape':
                print("escape")
                pygame.quit()
                sys.exit()
        if not paused and event.type == SECOND:
            secs, gameRunning, timerCount = timerSwitch(prevSec, secs, gameRunning, timerCount)
            print("second")

            if secs > 0:
                prevSec = secs
                secs -= 1
                minutes = secs // 60
                seconds = secs % 60
    if gameRunning:
        color = gameClockColor(secs)
    else:
        color = config_df[0]['ClockColorDelay']

    timer = "{0:02}:{1:02}".format(minutes, seconds)
    display_text = timeFont.render(timer, True, color)
    help_message = "Press <SPACE> to pause and again to resume."
    help_text = helpFont.render(help_message, True, BLUE)
    timeRect = display_text.get_rect()
    timeRect.center = (int(windowW/2), int(windowH/2))
    helpRect = help_text.get_rect()
    helpRect.midbottom = (int(windowW), int(windowH * .9))
    screen.fill(BLACK)
    screen.blit(display_text, timeRect)
    screen.blit(help_text, helpRect)
    if not gameRunning:
        soundsPlayed = timerSwitchSound(secs, gameRunning, timerCount, soundsPlayed)
    elif gameRunning and not soundPlayed:
        soundsPlayed = timerSwitchSound(secs, gameRunning, timerCount, soundsPlayed)
    frameCount += 1
    clock.tick(frameRate)
    pygame.display.flip()

pygame.quit()

