#!/usr/bin/env python3
"""! @brief PyVader a Space Invader in Linux Terminal

 @file /home/timai/Documents/Cours/R&T A1/R1.07-SAE15-R2.08 Algorithmique et programmation/PROJET/SpaceInvader/tp3/doc/spaceInvader.py

 @section libs Librairies/Modules
  - os https://docs.python.org/3/library/os.html
  - random https://docs.python.org/3/library/random.html?highlight=random#module-random
  - time https://docs.python.org/3/library/time.html?highlight=time#module-time
  - typing https://docs.python.org/3/library/typing.html?highlight=typing#module-typing
  - SaisiCar from SaisiCar.py

 @section authors Author(s)
  - Build by Timaï SELMI in 29/11/2021 .
"""
import os
import random as r
import time as t
import typing as ty

import saisiCar


# Function
def init_head(settings: ty.Dict):
    """! @brief Procedure to display the head of the game board

    @param settings (ty.Dict): allows to adapt the width and length of the header, but also to display dynamically the ``SCORE``, ``LIFE`` and ``LEVEL``.
    """

    width: int = int(settings['width_tray'])
    horizontal_line: str = ''
    horizontal_score: str = "  SCORE   VIE   LEVEL    "
    counter: int = 0

    # Generate horizontal line
    while counter < width:
        horizontal_line = horizontal_line + '-'
        counter += 1

    # Generates the header display.
    print(horizontal_line)
    print(horizontal_score)
    print(f"  {settings['score']:5}    {settings['life']:2}      {settings['level']:2}     ")
    print(horizontal_line)

    # Assert
    assert type(settings) == dict
    assert len(settings) == 5


def gameboard(settings: ty.Dict, aliens_list: ty.List[ty.Dict[str, int]], spaceship_player: ty.Dict[str, int],
              laser: ty.Dict):
    """! @brief Procedure to display the aliens, the spaceship, and the laser.

    @param settings (ty.Dict): Contains the different parameters allowing the display of the game board.
    @param aliens_list (ty.List[ty.Dict[str, int]]): The list of aliens, each alien contains a dictionary that indicates the positional coordinates.
    @param spaceship_player (ty.Dict[str, int]): Position of the player and on the power of the shot.
    @param laser (ty.Dict): If the ``shoot_enable`` is enable, then the laser will be displayed.
    """

    # Spawn entities [aliens_list, spaceship_player]
    for y in range(settings['height_tray']):
        line: str = ''
        for x in range(settings['width_tray']):
            char: str = ' '
            # Aliens
            for alien in range(len(aliens_list) - 1):
                if aliens_list[alien]['posx'] == x and aliens_list[alien]['posy'] == y:
                    char = '@'
            # Spaceship
            if x == spaceship_player['posx'] and y == settings['height_tray'] - 1:
                char = '#'
            # Laser entities
            if x == laser['posx'] and y == laser['posy'] and laser['shoot_enable']:
                if spaceship_player['shoot'] == 3:
                    char = ':'
                if spaceship_player['shoot'] == 2:
                    char = '$'
                if spaceship_player['shoot'] == 1:
                    char = '-'
            line += char
        print(f"{line}")

    # Print last line at the end
    print("-" * settings['width_tray'])

    # Assert
    assert type(settings) == dict
    assert len(settings) == 5
    assert type(aliens_list) == list
    assert type(spaceship_player) == dict


def init_aliens(settings: ty.Dict, aliens_list: ty.List):
    """! @brief Procedure to create a list, containing dictionaries of each aliens.

    @param settings (ty.Dict): The ``LEVEL`` parameter will allow you to adapt the number of aliens to be generate.
    @param aliens_list (ty.List): Our exit list.
    """
    # Generation number of aliens_list in relation to the level
    alien_number: int = int(settings['level']) ** 2 + 15
    alien_posx: int
    alien_posy: int = -1
    shoot: int = 0
    alien_dict: ty.Dict[str, int]

    # Generation of the alien dictionary
    for alien in range(int(alien_number)):
        # Generate 10 aliens_list per line maximum
        alien_posx = alien % 10
        if alien_posx == 0:
            alien_posy += 1

        # Assignment of the different keys calculated above        
        aliens_dict = {'posx': alien_posx,
                       'posy': alien_posy,
                       'shoot': shoot,
                       'sens': 0}

        aliens_list.append(aliens_dict)

    # Randomly gives the ability to shoot ['shoot': KEY]
    for alien in r.sample(aliens_list, 5):
        alien['shoot'] = r.randint(2, 3)

    # Assert
    assert type(settings) == dict
    assert len(settings) == 5
    assert type(aliens_list) == list


def move_entities(alien_list: ty.List, settings: ty.Dict, spaceship_player: ty.Dict, action_input: str, laser: ty.Dict):
    """! @brief This procedure will allow to modify the different keys, in order to create a pseudo-movement.

    @param alien_list (ty.List): Each dictionary contains the keys ``POSX``, ``POSY``.
    @param settings (ty.Dict): The ``width_tray`` key will prevent overflow.
    @param spaceship_player (ty.Dict): Contains the ``POSX`` keys which will be modified according to the player's action.
    @param action_input (str): the character will determine the movement of the spaceship.
    @param laser (ty.Dict): If the key ``shoot_enable = TRUE``, then there will be a move.

    @return bool: If the player's action is "o" then a shot is triggered.
    """

    shoot_enable: bool = None

    # Select each aliens_list
    for alien in range(len(alien_list)):
        # Go right side
        if alien_list[alien]['sens'] == 0:
            if alien_list[alien]['posx'] < settings['width_tray'] - 1:
                alien_list[alien]['posx'] += 1
            else:
                alien_list[alien]['posy'] += 1
                alien_list[alien]['sens'] = 1
        # Go left side
        else:
            if alien_list[alien]['posx'] > 0:
                alien_list[alien]['posx'] -= 1
            else:
                alien_list[alien]['posy'] += 1
                alien_list[alien]['sens'] = 0
    # Spaceship
    if action_input == 'k':
        spaceship_player['posx'] -= 1
    elif action_input == 'm':
        spaceship_player['posx'] += 1
    elif action_input == 'o':
        shoot_enable = True
    # Laser
    if laser['shoot_enable']:
        laser['posy'] -= 1

    return shoot_enable

    # Assert
    assert type(settings) == dict
    assert len(settings) == 5
    assert type(alien_list) == list


def game_run(alien_list: ty.List, settings: ty.Dict, speed: float, spaceship_player: ty.Dict) -> bool:
    """! @brief The function will check the different conditions for continuing the game. If the ``LIFE`` drops to 0, then True
    is returned. The player loses life when an alien reaches the value of the ``high_tray``, moreover the game is
    reloaded.. If all aliens are destroyed, then a new list is generated, and the player's weapon is more powerful.

    @param spaceship_player (ty.Dict): the key ``shoot`` will allow to modify the power of the weapon.
    @param speed (float): Accelerate or decelerate the speed of play.
    @param alien_list (ty.List): The alien list that will be regenerated and or used in the game conditions.
    @param settings (ty.Dict): Contains the ``high_tray`` which determines whether the alien has reached the end of the gameboard.

    @return bool: If the key ``LIFE`` is 0, then it is game over, and returns ``TRUE``.
    """
    height: int = settings['height_tray'] - 1
    game_finish: bool = False

    # All the aliens are dead except one.
    if len(alien_list) == 0:
        settings['level'] += 1
        # Speed of play
        speed -= 0.01
        # Generation of a new alien list
        init_aliens(settings, alien_list)
        # Shooting boost
        if spaceship_player['shoot'] < 4:
            spaceship_player['shoot'] += 1

    # The invader is here
    for alien in alien_list:
        if alien['posy'] == height:
            alien_list.clear()
            settings['life'] -= 1
            speed += 0.01
            spaceship_player['shoot'] = 1
            # Init the gameboard
            init_aliens(game_settings, alien_list)
            speed += 0.01

    if settings['life'] <= 0:
        game_finish = True

    return game_finish


def alien_hit(alien_list: ty.List, spaceship_player: ty.Dict) -> int:
    """! @brief This function is no longer useful ( abandoned). The function looks for aliens whose ``POSX`` is the same as the
    player's position, and then looks for which of these aliens ``POSY`` is the highest

    @param alien_list (ty.List): The function looks for aliens whose ``POSX`` is the same as the player's position, and then looks for which of these aliens ``POSY`` is the highest.
    @param spaceship_player (ty.Dict): Compare the ``POSX`` with the alien.

    @return int: Returns the value of the maximum ``POSY`` in the list of aliens, whose ``POSX`` is identical to the player.
    """
    pos_y: int = 0
    check_posx: bool

    for alien in range(len(alien_list)):
        # Compare if the alien's x-coordinates are equivalent to the spacecraft
        check_posx = alien_list[alien]['posx'] == spaceship_player['posx']
        # Find the max y of the column
        if check_posx and alien_list[alien]['posy'] >= pos_y:
            pos_y = alien_list[alien]['posy']
    return pos_y


def alien_score(aliens_list: ty.List, laser: ty.Dict, settings: ty.Dict):
    """! @brief Procedure that will handle the alien hitbox, and add points to the score.

    @param aliens_list (ty.List): If the x and y coordinates of the alien are identical to the laser, then it will be removed from the list.
    @param laser (ty.Dict): If the laser data is identical to an alien, then it will be reset. Its ``shoot_enable`` key.
    will be set to false, and will no longer be displayed during the display procedure.
    @param settings (ty.Dict): We will add the score based on the laser power ``shoot_power``.
    """
    for alien in range(len(aliens_list)):
        if aliens_list[alien]['posx'] == laser['posx'] and aliens_list[alien]['posy'] == laser['posy']:
            aliens_list.pop(alien)
            if laser['shoot_power'] == 2:
                settings['score'] += 10
            if laser['shoot_power'] == 1:
                settings['score'] += 5

            laser['shoot_power'] -= 1
            break

    if laser['shoot_power'] == 0:
        laser['posx'] = ''
        laser['posy'] = ''
        laser['shoot_enable'] = False


if __name__ == "__main__":
    game_settings: ty.Dict[str, int] = {'width_tray': 25,
                                        'height_tray': 20,
                                        'score': 0,
                                        'life': 4,
                                        'level': 1}
    game_end: bool = False
    # Init aliens_list list
    aliens: ty.List[ty.Dict] = []
    init_aliens(game_settings, aliens)
    # Other entities
    spaceship: ty.Dict[str, int] = {'posx': game_settings['width_tray'] // 2,
                                    'shoot': 1}
    laser_shoot: ty.Dict[str, int] = {'posx': '',
                                      'posy': '',
                                      'shoot_enable': False,
                                      'shoot_power': ''}
    # Game speed
    game_speed: float = 0.1
    # Player action_input
    kb = saisiCar.SaisiCar()
    action_player: str = ""

    while game_end == False and action_player != "q":
        action_player = kb.recupCar(['m', 'o', 'k', 'q'])
        alien_score(aliens, laser_shoot, game_settings)
        game_end = game_run(aliens, game_settings, game_speed, spaceship)

        # Print gameboard
        os.system("clear")
        init_head(game_settings)
        gameboard(game_settings, aliens, spaceship, laser_shoot)

        # Takes into account the player's actions
        if move_entities(aliens, game_settings, spaceship, action_player, laser_shoot):
            laser_shoot = {'posx': spaceship['posx'],
                           'posy': game_settings['height_tray'] - 2,
                           'shoot_enable': True,
                           'shoot_power': spaceship['shoot']}
        t.sleep(game_speed)
