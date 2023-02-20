"""
Application:  Game Timer
Author: Roy Campbell


"""
import os
import json
import pygame
from pygame.constants import (QUIT, K_SPACE, K_RETURN)
"""
Optional Imports as necessary
import sys
import time
import datetime
import os
import json
import pandas as pd
"""


# default functions setup
def config_array(string):
    if testvar:
        print("config_array", string)
    var_array = string.split(":")
    return var_array


def time_setup(time_array):
    if testvar:
        print("time_setup", time_array)
    timer_secs = (int(time_array[0]) * 60 * 60) + (int(time_array[1]) * 60) + int(time_array[2])
    return timer_secs


def config_exist(configFile, message):
    if testvar:
        print("config_exist")
    configFileExist = os.path.lexists(configFile)
    if configFileExist:
        with open(configFile, 'r') as jsonFile:
            # data = pd.read_json(jsonFile)
            data = json.loads(jsonFile.read())
    else:
        print(message)
        exit()

    # df = pd.DataFrame.from_dict(data, orient='index')
    # lst = df.values.tolist()
    return data


# Verify config json files exist and read them in.
# Find and import application config
appDir = os.path.dirname(os.path.abspath(__file__))
assetsDir = 'assets'
configDir = 'config'
configApp = os.path.join(appDir, assetsDir, configDir, 'config_app.json')
configEvent = os.path.join(appDir, assetsDir, configDir, 'config_event.json')
missingConfigApp = ' \
\n \
*** Error: Config File Missing \n \
There must be a "config_app.json" file in the "assets/config" directory \
\n '
missingConfigEvent = ' \
\n \
*** Error: Config File Missing \n \
There must be a "config_event.json" file in the "assets/config" directory \
\n '

testvar = True
if testvar:
    print("testvar")

configApp = config_exist(configApp, missingConfigApp)
configEvent = config_exist(configEvent, missingConfigEvent)


class Settings:

    # set up application constants and defaults

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (190, 113, 50)
    BLUE = (83, 145, 223)
    YELLOW = (255, 239, 40)
    VIOLET = (56, 0, 100)
    BROWN = (150, 75, 0)
    GRAY = (128, 128, 128)
    default_colours = [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET, BROWN, GRAY, WHITE, BLACK]
    # Clock Settings
    try:
        clock_color = (configEvent['ClockColor'])
    except NameError:
        clock_color = GREEN
    try:
        clock_color_warning = (configEvent['ClockColorWarning'])
    except NameError:
        clock_color_warning = YELLOW
    try:
        clock_color_ending = (configEvent['ClockColorEnding'])
    except NameError:
        clock_color_ending = RED
    try:
        clock_color_delay = (configEvent['ClockColorDelay'])
    except NameError:
        clock_color_delay = BLUE
    try:
        clock_color_delay_first_game = (configEvent['ClockColorDelayFirstGame'])
    except NameError:
        clock_color_delay_first_game = ORANGE

    gameSecs = int(time_setup(config_array(configEvent['GameTime'])))
    delaySecs = int(time_setup(config_array(configEvent['ClockDelayBetweenGames'])))
    warningSecs = int(time_setup(config_array(configEvent['ClockColorWarning'])))
    endingSecs = int(time_setup(config_array(configEvent['ClockColorEnding'])))
    delayFirstGameSecs = int(time_setup(config_array(configEvent['ClockDelayFirstGame'])))
    if delayFirstGameSecs > 100:
        print("delayFirstGameSecs too long")
        exit()
    pygame.init()
    screenSize = pygame.display.get_desktop_sizes()
    screenWidth = screenSize[0][0]
    screenHeight = screenSize[0][1]
    if configApp["FullScreen"] == "true":
        windowW = int(screenWidth)
        windowH = int(screenHeight)
    else:
        w = configApp["AppWidth"].split(':')
        h = configApp["AppHeight"].split(':')
        if w[1] == "%":
            windowW = int(screenWidth * (int(w[0]) / 100))
        else:
            windowW = int(screenWidth * (int(w[0]) / 100))  # todo modify for pixel size
        if h[1] == "%":
            windowH = int(screenHeight * (int(h[0]) / 100))
        else:
            windowH = int(screenHeight * (int(h[0]) / 100))  # todo modify for pixel size

    screen = pygame.display.set_mode([windowW, windowH])
    frameCount = 0
    frameRate = 60

    clock_font = config_array(configEvent['ClockFont'])
    if clock_font[2] == "%":
        clock_size = int(windowH * int(clock_font[1]) / 100)
    elif clock_font[2] == "pt":
        clock_size = int(clock_font[1])
    else:
        clock_size = int(clock_font[1])
    clockFont = pygame.font.SysFont(clock_font[0], clock_size)

    help_font = config_array(configEvent['HelpFont'])
    if help_font[2] == "%":
        help_size = int(windowH * int(help_font[1]) / 100)
    elif help_font[2] == "pt":
        help_size = int(help_font[1])
    else:
        help_size = int(help_font[1])
    helpFont = pygame.font.SysFont(help_font[0], help_size)

    delay_font = config_array(configEvent['ClockFirstGameDelayFont'])
    if delay_font[2] == "%":
        delay_size = int(windowH * int(delay_font[1]) / 100)
    elif delay_font[2] == "pt":
        delay_size = int(delay_font[1])
    else:
        delay_size = int(delay_font[1])
    delayFont = pygame.font.SysFont(delay_font[0], delay_size)

    screen_fill = configApp['BackgroundColor']

    file_path = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(file_path, configApp["AssetPath"])
    config_path = os.path.join(assets_path, configApp["ConfigPath"])
    image_path = os.path.join(assets_path, configApp["ImagesPath"])
    sound_path = os.path.join(file_path, "SoundsPath")


def timer():
    if testvar:
        print("Timer __init__")
    gameSecs = Settings.gameSecs
    if Settings.warningSecs > 0:
        warningSecs = Settings.warningSecs
    else:
        if gameSecs > 60:
            warningSecs = 30
        else:
            warningSecs = int(gameSecs * .25)
    if Settings.endingSecs > 0:
        endingSecs = Settings.endingSecs
    else:
        if gameSecs > 60:
            endingSecs = 10
        else:
            endingSecs = int(Settings.warningSecs * .5)
    if Settings.delaySecs > 0:
        delayBetweenGamesSecs = Settings.delaySecs
    else:
        delayBetweenGamesSecs = 90

    if Settings.delayFirstGameSecs > 0:
        delayFirstGameSecs = Settings.delayFirstGameSecs
    else:
        delayFirstGameSecs = 5

    SECOND = pygame.USEREVENT
    clock = pygame.time.Clock()
    screen = Settings.screen
    screen.fill(Settings.screen_fill)
    pygame.time.set_timer(SECOND, 1000)
    running = False
    delayStart = False
    pause = True

    # Hard Coded Values to be extracted into json config
    delayClockConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25%"]]
    gameClockConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25%"]]
    warningClockConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25%"]]
    endingClockConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25%"]]
    delayBetweenGamesClockConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25%"]]


    delay_clock = [delayClockConfig, delayFirstGameSecs, delayColor, delayMessage]
    game_clock = [gameClockConfig, gameSecs, gameColor, gameMessage]
    warning_clock = [warningClockConfig, warningSecs, warningColor, warningMessage]
    ending_clock = [endingClockConfig, endingSecs, endingColor, endingMessage]
    delay_between_games_clock = [delayBetweenGamesClockConfig, delayBetweenGamesSecs, delayBetweenGamesColor, delayBetweenGamesMessage]

    timers_list = [delay_clock, game_clock, warning_clock, ending_clock, delay_between_games_clock]
    config_list = [clock, running, delayStart, pause]

    return timers_list, config_list

def running(self):
    gameSecs = Settings.gameSecs
    screen = Settings.screen
    frameCount = Settings.frameCount
    paused = False
    for event in pygame.event.get():
        if event.type == K_SPACE or event.type == K_RETURN:
            print("space pressed")
            paused = not paused
            while paused:
                if event.key == pygame.K_SPACE or event.type == K_RETURN:
                    paused = not paused
                    running = not running
        elif event.type == SECOND:
            if gameSecs > 0:
                gameSecs -= 1
            else:
                # stop timer
                running = False

    Settings.screen.fill(Settings.BLACK)
    # if 5 > gameSecs > 1:
    if warningSecs >= gameSecs > endingSecs:
        color = Settings.YELLOW
    elif gameSecs <= Settings.endingSecs:
        color = Settings.RED
    else:
        color = Settings.GREEN
    print(gameSecs)

# this is likely where def draw(self) belongs

def draw(self):
    if testvar:
        print("draw")
    minutes = gameSecs // 60
    seconds = gameSecs % 60
    timer = "{0:02}:{1:02}".format(minutes, seconds)
    display_text = Settings.clockFont.render(timer, True, color)
    help_message = "Press <SPACE> to pause and again to resume."
    help_text = Settings.helpFont.render(help_message, True, Settings.BLUE)
    timeRect = display_text.get_rect()
    timeRect.center = (int(Settings.windowW/2), int(Settings.windowH/2))
    helpRect = help_text.get_rect()
    helpRect.bottomleft = (int(Settings.windowW * .1), int(Settings.windowH * .9))
    screen.blit(display_text, timeRect)
    screen.blit(help_text, helpRect)
    frameCount += 1
    clock.tick(Settings.frameRate)
    pygame.display.flip()

    # Artifact
    # def run(self):
    #     if testvar:
    #         print("run")
    #     delayStart = True
    #     running = True
    #     pause = False
    #     while delayStart:
    #         clock.tick(60)
    #         watch_for_events()
    #         if not pause:
    #             draw()
    #             # events()
    #     while running:
    #         clock.tick(60)
    #         watch_for_events()
    #         if not pause:
    #             draw()
    #             # events()

    # def watch_for_events(self):
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 pause = not pause

    # artifact
    # def draw(self):
    #     background.draw(screen)
    #     pygame.display.flip()


if __name__ == '__main__':
    timers_list, config_list = timer()
    pygame.init()
    running()