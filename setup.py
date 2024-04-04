from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    'packages': [],
    'include_files': ["assets/"],
    'excludes': []
}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('SecondChance.py', base=base)
]

setup(name='SecondChance',
      version = '2',
      description = 'A platformer-style video game with a mechanic of always giving the user a second chance. Functions like any normal platformer, but when the player dies to an enemy, they are given a second chance if they can pass minigames within the base game.',
      options = {'build_exe': build_options},
      executables = executables)
