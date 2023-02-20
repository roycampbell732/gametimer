import os
import pygame
import json


def config_array(string):
    var = string.split(":")
    return var


def time_setup(self):
    print(self)
    timer_secs = (int(self[0]) * 60 * 60) + (int(self[1]) * 60) + int(self[2])
    print(timer_secs)
    return timer_secs


class Settings:

    def config_setup():   # Verify config json files exist and read them in.
        # Find and import application config
        appDir = os.path.dirname(os.path.abspath(__file__))
        assetsDir = 'assets'
        configDir = 'config'
        configApp = os.path.join(appDir, 'config_app.json')
        configEvent = os.path.join(appDir, 'config_event.json')
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

        def config_exist(configFile, message):
            configFileExist = os.path.lexists(configFile)
            if configFileExist:
                with open(configFile, 'r') as jsonFile:
                    # data = pd.read_json(jsonFile)
                    data = json.loads(jsonFile.read())
                    print("37 - type(data)", type(data))
            else:
                print(message)
                exit()

            # df = pd.DataFrame.from_dict(data, orient='index')
            # lst = df.values.tolist()
            return data

        config1 = config_exist(configApp, missingConfigApp)
        config2 = config_exist(configEvent, missingConfigEvent)
        return config1, config2

    # set up application constants and defaults
    configApp, configEvent = config_setup()

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
    try:
        clock_color = (configEvent['ClockColor'])
    except NameError:
        clock_color = GREEN


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
