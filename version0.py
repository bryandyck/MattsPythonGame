# import necessary modules and packages
import time
import sys
import pygame
from pygame.locals import *

# define global constants for pygame initialization
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 30

# define a global variable to hold the images that you will use
IMAGES = {}
SOUNDS = {}

# global variables to hold pygame window and global drawing objects
WINDOW = None
FPS_CLOCK = None

# using a dictionary to hold an unordered list of keys relating to certain speeds,
# this way I am able to locate a certain speed easily using a key without having to sort anything.
# So i can add any speed whenever I want or change it and not worry about some sort of order
VELOCITIES = {"0.1-1": 22,
              "1.01-2": 20,
              "2.01-3": 18,
              "3.01-4": 16,
              "4.01-5": 14,
              "5.01-6": 12,
              "6.01-7": 10,
              "7 more": 8}


# olympics// a sprinting game
def main():
    global WINDOW, FPS_CLOCK

    # call the initialize_game function below to initialize pygame and seup the window
    initialize_game()

    # define the main flow of the game here. It gets called from the lines at
    # the bottom when this file is called as a script

    # display a simple welcome screen. In the future, this can be extended to show the leaderbard
    display_welcome_screen()

    # initialise a variable for the current time, to be used later...
    start_time = time.time()

    # call run time trial to get the speed of the runner
    run_time_trial()

    # this variable now takes in the current time, same as what we used before. But this time is only set
    # after you have completed the time trial
    end_time = time.time()

    # we can work out time taken to press ten times by taking away the initial time, from the end time. Giving
    # us seconds (round to 2 hundredths)
    overall_time = round(end_time - start_time, 2)

    # time sleep is just a brief wait so code does not come out clunky and too quickly
    time.sleep(0.5)

    # format is a nice try to implement a variable at the end of which is not global, allowing it to be entered
    # in the string
    # this works no matter what rounded seconds is meaning there is that flexibility
    show_time_trial_result(overall_time)

    user_start_velocity = get_velocity_from_keystrokes_per_second(overall_time)

    # figuring out a minimum time for the user to complete the race in
    # speed = distance / time
    minimum_time = 100.0 / user_start_velocity

    time.sleep(2)
    print("\nThe Race is starting! When you see go, hit the right arrow!")
    # the time between go and space is the delay in time it took for the user to begin his or her run, this must be
    # added to the total initial minimum time.
    print("\n3...")
    time.sleep(1.5)
    print("\n2...")
    time.sleep(1.5)
    print("\n1...")
    time.sleep(2)
    print("\nGO!")

    start_delay_current_time = time.time()
    pressed = False
    while not pressed:
        for event in pygame.event.get():
            # if the user closes the window or hits the escape key, then quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit_game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                pressed = True

    end_delay_current_time = time.time()

    delayed_starting_time = end_delay_current_time - start_delay_current_time
    rounded_delayed_starting_time = (round(delayed_starting_time, 2))
    print(" ")
    print(rounded_delayed_starting_time)
    # here we take into account the time it takes for the user to begin running
    # we add this time to the already total minimum time
    # this gives us a total time now as the character will begin to run
    total_time = minimum_time + rounded_delayed_starting_time
    # this is just to make sure it works
    print("\nYour current total time is {t}".format(t=(round(total_time, 2))))


def show_time_trial_result(overall_time):
    display_game_background()
    display_text("You Did it in {t} Seconds!".format(t=overall_time), location=(150, 200))
    display_text("Press enter to continue.", location=(150, 250))
    update_display_and_wait_for_enter_key_press()


def run_time_trial():
    # create a while loop, this is to register and display key presses until it has been pressed ten times.
    press_count = 0
    text_to_show = "Press the space key 10 times as fast as you can to determine your velocity."
    while press_count < 10:
        for event in pygame.event.get():

            # if the user closes the window or hits the escape key, then quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit_game()

            # this essentially registers whenever the key space has been pressed by the user.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # incrementing the press count.
                press_count += 1
                # displaying the total count you have pressed it, after pressing it until you get to 10.
                text_to_show = "you pressed space {p} out of 10 times".format(p=press_count)

        # draw sprites
        display_game_background()
        display_text(text_to_show, location=(100, 300))

        update_screen()


def display_welcome_screen():
    display_welcome_background()
    display_text("Welcome to the game!", font_size=30, location=(100, 200))
    display_text("Press enter to continue.", font_size=30, location=(150, 240))
    update_display_and_wait_for_enter_key_press()


def update_display_and_wait_for_enter_key_press():
    enter_pressed = False
    while not enter_pressed:
        for event in pygame.event.get():

            # if the user closes the window or hits the escape key, then quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit_game()

            # this essentially registers whenever the key space has been pressed by the user.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # incrementing the press count.
                enter_pressed = True

        update_screen()


def update_screen():
    global FPS_CLOCK

    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def display_text(text, font='Comic Sans MS', font_size=24, colour=(0, 0, 0), location=(0, 0)):
    global WINDOW
    my_font = pygame.font.SysFont(font, font_size)
    text_surface = my_font.render(text, False, colour)
    WINDOW.blit(text_surface, location)


def display_welcome_background():
    global WINDOW, IMAGES
    WINDOW.blit(IMAGES['welcome_background'], (0, 0))


def display_game_background():
    global WINDOW, IMAGES
    WINDOW.blit(IMAGES['game_background'], (0, 0))


def display_runner(progress_percent):
    global WINDOW, IMAGES
    WINDOW.blit(IMAGES['runner'], (200 + 400 * progress_percent, 400))


def initialize_game():
    global WINDOW, FPS_CLOCK, IMAGES

    pygame.init()
    pygame.font.init()

    FPS_CLOCK = pygame.time.Clock()

    # set up the actual pygame window display
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # name of the window
    pygame.display.set_caption("Matt's Athletic's Championship")

    # load background images
    IMAGES["welcome_background"] = pygame.image.load("Images\\welcome_background.png").convert_alpha()
    IMAGES["game_background"] = pygame.image.load("Images\\game_background.png").convert_alpha()
    IMAGES["runner"] = pygame.image.load("Images\\runner.png").convert_alpha()

    # load number images
    IMAGES["0"] = pygame.image.load("Images\\0.png").convert_alpha()
    IMAGES["1"] = pygame.image.load("Images\\1.png").convert_alpha()
    IMAGES["2"] = pygame.image.load("Images\\2.png").convert_alpha()
    IMAGES["3"] = pygame.image.load("Images\\3.png").convert_alpha()
    IMAGES["4"] = pygame.image.load("Images\\4.png").convert_alpha()
    IMAGES["5"] = pygame.image.load("Images\\5.png").convert_alpha()
    IMAGES["6"] = pygame.image.load("Images\\6.png").convert_alpha()
    IMAGES["7"] = pygame.image.load("Images\\7.png").convert_alpha()
    IMAGES["8"] = pygame.image.load("Images\\8.png").convert_alpha()
    IMAGES["9"] = pygame.image.load("Images\\9.png").convert_alpha()
    #IMAGES["."] = pygame.image.load("Images\\dot.png").convert_alpha()

    # load text images
    IMAGES["go"] = pygame.image.load("Images\\go.png").convert_alpha()
    IMAGES["gameover"] = pygame.image.load("Images\\gameover.png").convert_alpha()

    # load sound files
    SOUNDS["starter_pistol"] = None

def get_velocity_from_keystrokes_per_second(seconds_for_ten_keystrokes):
    global VELOCITIES

    # using rounded seconds we have a value that fits a certain key
    # we use the dictionary, to find the key it fits
    # we then return the value at that certain key
    # this value is the users starting speed.
    if 0 < seconds_for_ten_keystrokes < 1.01:
        velocity = VELOCITIES["0.1-1"]
    elif 1 < seconds_for_ten_keystrokes < 2.01:
        velocity = VELOCITIES["1.01-2"]
    elif 2 < seconds_for_ten_keystrokes < 3.01:
        velocity = VELOCITIES["2.01-3"]
    elif 3 < seconds_for_ten_keystrokes < 4.01:
        velocity = VELOCITIES["3.01-4"]
    elif 4 < seconds_for_ten_keystrokes < 5.01:
        velocity = VELOCITIES["4.01-5"]
    elif 5 < seconds_for_ten_keystrokes < 6.01:
        velocity = VELOCITIES["5.01-6"]
    elif 6 < seconds_for_ten_keystrokes < 7.01:
        velocity = VELOCITIES["6.01-7"]
    else:  # 7 < seconds_for_ten_keystrokes:
        velocity = VELOCITIES["7 more"]

    print("\nYour Starting Velocity is {v} mph".format(v=velocity))
    return velocity


def quit_game():
    pygame.quit()  # this exits the pygame window
    sys.exit(0)  # this exits the application


# Only execute the main function if this script is running directly. If it is part
# of a library then it should not execute
if __name__ == "__main__":
    main()
