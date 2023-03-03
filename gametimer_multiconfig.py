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
    print("config_array", string)
    var_array = string.split(":")
    return var_array


def time_setup(time_array):
    print("time_setup", time_array)
    timer_secs = (int(time_array[0]) * 60 * 60) + (int(time_array[1]) * 60) + int(time_array[2])
    return timer_secs


def config_exist(configFile, message):
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
    warningSecs = int(time_setup(config_array(configEvent['ClockWarning'])))
    endingSecs = int(time_setup(config_array(configEvent['ClockEnding'])))
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

    top_font = config_array(configEvent['TopFont'])
    if top_font[2] == "%":
        top_size = int(windowH * int(top_font[1]) / 100)
    elif top_font[2] == "pt":
        top_size = int(top_font[1])
    else:
        top_size = int(top_font[1])
    topFont = pygame.font.SysFont(top_font[0], top_size)

    bottom_font = config_array(configEvent['BottomFont'])
    if bottom_font[2] == "%":
        delay_size = int(windowH * int(bottom_font[1]) / 100)
    elif bottom_font[2] == "pt":
        bottom_size = int(bottom_font[1])
    else:
        bottom_size = int(bottom_font[1])
    bottomFont = pygame.font.SysFont(bottom_font[0], bottom_size)

    screen_fill = configApp['BackgroundColor']

    # Hard Coded Values to be extracted into json config
    windowConfig = [["topRow", "25:%"], ["middleRow", "50:%"], ["bottomRow", "25:%"]]
    windowClockConfig = [["topRow", "10:%"], ["middleRow", "80:%"], ["bottomRow", "10:%"]]

    file_path = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(file_path, configApp["AssetPath"])
    config_path = os.path.join(assets_path, configApp["ConfigPath"])
    image_path = os.path.join(assets_path, configApp["ImagesPath"])
    sound_path = os.path.join(file_path, "SoundsPath")


def timer():
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

    screen = Settings.screen
    screen.fill(Settings.screen_fill)
    running = True
    delayStart = True
    pause = False
    delayBetween = False

    delay_clock = [Settings.windowConfig, delayFirstGameSecs, Settings.clock_color_delay_first_game,
                   configEvent['DelayMessage']]
    game_clock = [Settings.windowClockConfig, gameSecs, Settings.clock_color, configEvent['GameMessage']]
    warning_clock = [Settings.windowClockConfig, warningSecs, Settings.clock_color_warning, configEvent['WarningMessage']]
    ending_clock = [Settings.windowClockConfig, endingSecs, Settings.clock_color_ending, configEvent['EndingMessage']]
    delay_between_games_clock = [Settings.windowConfig, delayBetweenGamesSecs, Settings.clock_color_delay,
                                 configEvent['DelayBetweenGamesMessage']]

    timers_list = [delay_clock, game_clock, warning_clock, ending_clock, delay_between_games_clock]
    config_list = [running, delayStart, delayBetween, pause]

    return timers_list, config_list


def running(timers, configs):
    SECOND = pygame.USEREVENT
    pygame.time.set_timer(SECOND, 1000)
    clock = pygame.time.Clock()

    delay_timer = timers[0]
    game_timer = timers[1]
    warning_timer = timers[2]
    ending_timer = timers[3]
    delay_between_games_timer = timers[4]
    screen = Settings.screen
    frameCount = Settings.frameCount
    sequence = ['delay_timer', 'game_timer', 'delay_between_games']
    if delay_timer[1] <=1:
        s_count = 1
    else:
        s_count = 0
    timers_running = True

    running = config_list[0]
    delay_start = config_list[1]
    delayBetween = config_list[2]
    pause = config_list[3]
    gameSecs = game_timer[1]
    warningSecs = warning_timer[1]
    endingSecs = ending_timer[1]
    delayBetweenGamesSecs = delay_between_games_timer[1]
    while s_count <= 2:
        if s_count == 0 and delay_start and delay_timer[1] > 1:
            clock_params = delay_timer
        elif s_count == 1:
            clock_params = game_timer
        elif s_count == 2 :
            clock_params = delay_between_games_timer
        for event in pygame.event.get():
            if event.type == K_SPACE or event.type == K_RETURN:
                print("space pressed")
                pause = not pause
                while pause:
                    if event.key == pygame.K_SPACE or event.type == K_RETURN:
                        pause = not pause
                        running = not running
            elif event.type == SECOND:
                if not delayBetween:
                    if gameSecs > 0:
                        gameSecs -= 1
                    else:
                        # stop timer
                        running = False
                        delayBetween = not delayBetween
                else:
                    if delayBetweenGamesSecs > 0:
                        delayBetweenGamesSecs -= 1
                    else:
                        delayBetween = not delayBetween

        Settings.screen.fill(Settings.BLACK)
        # if 5 > gameSecs > 1:
        if gameSecs > warningSecs:
            draw(game_timer, gameSecs, screen, clock, frameCount)
        if warningSecs >= gameSecs > endingSecs:
            draw(warning_timer, gameSecs, screen, clock, frameCount)
        elif gameSecs <= endingSecs:
            draw(ending_timer, gameSecs, screen, clock, frameCount)
        elif gameSecs <= 0:
            delayBetween = not delayBetween
            draw(delay_between_games_timer, delayBetweenGamesSecs, screen, clock, frameCount)
        else:
            s_count += 1

# this is likely where def draw(self) belongs


def draw(*args):
    clock_to_draw = args[0]
    clockSecs = args[1]
    screen = args[2]
    clock = args[3]
    frameCount = args[4]
    minutes = clockSecs // 60
    seconds = clockSecs % 60

    windowConfig = Settings.windowConfig
    # windowClockConfig = Settings.windowClockConfig
    timer_display = "{0:02}:{1:02}".format(minutes, seconds)
    top_display = Settings.clockFont.render(clock_to_draw[3], True, clock_to_draw[2])
    main_display = Settings.clockFont.render(timer_display, True, clock_to_draw[2])
    bottom_display = Settings.clockFont.render(clock_to_draw[3], True, clock_to_draw[2])
    # help_text = Settings.helpFont.render(help_message, True, Settings.BLUE)
    for k, v in windowConfig:
        row = v.split(':')
        rowValue = int(row[0])
        if k == 'topRow':
            topRow = [rowValue, row[1]]
        elif k == 'middleRow':
            middleRow = [rowValue, row[1]]
        elif k == 'bottomRow':
            bottomRow = [rowValue, row[1]]

    topRect = top_display.get_rect()
    topRect.midtop = (int(Settings.windowW), int(Settings.windowH * topRow[0] / 100))
    mainRect = main_display.get_rect()
    mainRect.center = (int(Settings.windowW), int(Settings.windowH * middleRow[0] / 100))
    bottomRect = bottom_display.get_rect()
    bottomRect.midbottom = (int(Settings.windowW), int(Settings.windowH * bottomRow[0] / 100))
    print(Settings.windowW, Settings.windowH)
    # print(top_display)
    print(main_display)
    # print(bottom_display)
    screen.blit(main_display, mainRect)
    screen.blit(top_display, topRect)
    screen.blit(bottom_display, bottomRect)
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
    timer_list, config_list = timer()
    pygame.init()
    running(timer_list, config_list)