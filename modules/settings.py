from colorama import Fore, Style

RESET = Style.RESET_ALL
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RED = Fore.RED
YELLOW = Fore.YELLOW
BOLD = '\033[1m'
PINK = Fore.LIGHTMAGENTA_EX


class Settings:
    prompt_models = [
        {"name": "Default - Short with weights", "value": "weigths"},
        {"name": f"Artistic ({BOLD}Creates a lot of chaos in images{RESET})", "value": "artistic"}
    ]

    mj_models = [
        {"name": "Default - v4"},
        {"name": f"Anime - Niji ({BOLD}Little curve{RESET})", "value": "--niji --q 2"},
        {"name": f"[{RED}Only artistic model{RESET}] High realism ({BOLD}Works well only on objects. For example: cloth{RESET})", "value": "--testp --s 1500"},
    ]

    advanced_settings = [
        {"name": "Yes"},
        {"name": "No"}
    ]

    types = [
        {"name": "No type", "value": "--v 4 --ar 3:2 --s 1000 --q 5"},
        {"name": "Anime", "value": "anime style::5 --v 4 --s 1000 --q 5"},
        {"name": "Photorealistic", "value": "high quality photo::5, soft light::2, sharp-focus::3, hyper realism::4 --v 4 --s 1000 --q 5"},
        {"name": "Avatar", "value": "high quality avatar::5, circle::5, square::5, sharp-focus::5 --v 4 --s 1000 --q 5"},
        {"name": f"{PINK}♡ Сouple avatar ♡{RESET}", "value": "anime::5, huge::4, kiss:4, high quality avatar::3, girl and boy::5, romantic::3 --v 4 --s 1000 --q 5"}
    ]

    aspect_ratios = [
        {"name": "1:2", "value": "--ar 1:2"},
        {"name": "2:1", "value": "--ar 2:1"},
        {"name": "2:3", "value": "--ar 2:3"},
        {"name": "3:2", "value": "--ar 3:2"},
        {"name": f"16:9 ({BOLD}Desktop wallpaper{RESET})", "value": "--ar 16:9"},
        {"name": f"9:16 ({BOLD}Mobile wallpaper{RESET})", "value": "--ar 9:16"},
        {"name": f"1:1 ({BOLD}Avatar{RESET})", "value": "--ar 1:1"}
    ]

    renderers = [
        {"name": "No render type", "value": ""},
        {"name": f"Octane Render ({BOLD}Universal for all styles{RESET})", "value": "octane render::4"},
        {"name": f"Unreal Engine Render ({BOLD}More suitable for armors{RESET})", "value": "unreal engine::4"},
        {"name": f"Ray Tracing Render ({BOLD}Improves lighting{RESET})", "value": "ray tracing::4, v-ray::4"},
        {"name": f"[{BLUE}Recommended{RESET}] Mixed Render ({BOLD}All-in-One{RESET})", "value": "octane render::3 unreale engine::3, v-ray::3"}
    ]

    contents = [
        {'name': 'General', 'value': ''},
        {'name': 'Character', 'value': 'character design::4'}, 
        {'name': 'Landscape', 'value': 'landscape desing::4'}, 
        {'name': 'Object', 'value': 'object design::4, one object::5, high object details::3, --no background-details, --no background'}, 
        {'name': 'Light', 'value': 'light-design::4, shaders::3'}, 
        {'name': 'Particles', 'value': 'particle design::4, particles::3, smoke::1, neon::1, flash::1, spark::1'}
    ]

    colors = [
        {'name': 'Nothing', 'value': ''},
        {'name': 'Red', 'value': 'red::10'},
        {'name': 'Blue', 'value': 'blue::10'},
        {'name': 'Green', 'value': 'green::10'},
        {'name': 'Purple', 'value': 'purple::10'},
        {'name': 'Pink', 'value': 'pink::10'},
        {'name': 'Orange', 'value': 'orange::10'},
        {'name': 'Yellow', 'value': 'orange::10'},
        {'name': 'Black', 'value': 'black::10'},
        {'name': 'White', 'value': 'white::10'},
        {'name': 'Grey', 'value': 'grey::10'},
    ]