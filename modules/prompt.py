import os
import re

from revChatGPT.V1 import Chatbot
from colorama import init as colorama_init
from modules.settings import *

colorama_init()


class Prompt:
    def __init__(self, config):
        if config["session_token"]:
            self.chatbot = Chatbot(
                config={
                    "session_token": config["session_token"],
                }
            )
        elif config["email"] and config["password"]:
            self.chatbot = Chatbot(
                config={
                    "email": config["email"],
                    "password": config["password"],
                }
            )
        else:
            raise ValueError("No login details")

    def __create_prompt(self, text: str, words: int, model: int = 0):
        model_name = Settings.prompt_models[model]["value"]
        return (
            open(f"./models/{model_name}.txt", "r")
            .read()
            .replace("NNN", str(words))
            .replace("TEXT", text)
        )

    def ask(
        self,
        text: str,
        count_words: int = 25,
        type: int = 0,
        resolution: int = 0,
        renderer: int = 0,
        content: int = 0,
        prompt_model: int = 0,
        mj_model: int = 0,
        colors: list[int] = [],
    ) -> str:
        if not isinstance(text, str):
            raise ValueError("Text must be a string")

        if not isinstance(count_words, int):
            raise ValueError("Count words must be a int")

        if not isinstance(type, int) and type < 0 and type > len(Settings.types) - 1:
            raise ValueError(
                f"Type must be a int and between 0 and {len(Settings.types) - 1}"
            )

        if (
            not isinstance(resolution, int)
            and resolution < 0
            and resolution > len(Settings.aspect_ratios) - 1
        ):
            raise ValueError(
                f"Resolution must be a int and between 0 and {len(Settings.aspect_ratios) - 1}"
            )

        if (
            not isinstance(renderer, int)
            and renderer < 0
            and renderer > len(Settings.renderers) - 1
        ):
            raise ValueError(
                f"Renderer must be a int and between 0 and {len(Settings.renderers) - 1}"
            )

        if (
            not isinstance(content, int)
            and content < 0
            and content > len(Settings.contents) - 1
        ):
            raise ValueError(
                f"Content must be a int and between 0 and {len(Settings.contents) - 1}"
            )

        if (
            not isinstance(mj_model, int)
            and mj_model < 0
            and mj_model > len(Settings.mj_models) - 1
        ):
            raise ValueError(
                f"MidJourney model must be a int and between 0 and {len(Settings.mj_models) - 1}"
            )

        if (
            not isinstance(prompt_model, int)
            and prompt_model < 0
            and prompt_model > len(Settings.prompt_models) - 1
        ):
            raise ValueError(
                f"Prompt model must be a int and between 0 and {len(Settings.mj_models) - 1}"
            )

        for color in colors:
            if (
                not isinstance(color, int)
                and color < 0
                and color > len(Settings.colors) - 1
            ):
                raise ValueError(
                    f"Color must be a int and between 0 and {len(Settings.colors) - 1}"
                )

        prompt = ""

        if mj_model == 2:
            prompt_model = 1

        url = ""
        if text.startswith("http"):
            url = text.split(" ")[0]
            text = " ".join(text.split(" ")[1:])
        response = ""

        try:
            for data in self.chatbot.ask(
                self.__create_prompt(text, count_words, prompt_model)
            ):
                response = data["message"]
        except:
            raise BaseException("ChatGPT Error")

        if response[-1] == ".":
            response = response[:-1]
        
        if mj_model == 2:
            mj_model_value = Settings.mj_models[mj_model]["value"]
            prompt = f"{response}, {mj_model_value}"
        elif mj_model == 1:
            mj_model_value = Settings.mj_models[mj_model]["value"]
            renderer_value = Settings.renderers[renderer]["value"]
            content_value = Settings.contents[content]["value"]
            resolution_value = Settings.aspect_ratios[resolution]["value"]
            color_value = ""
            for color in colors:
                color_value += Settings.colors[color]["value"] + ", "
            prompt = f"{response}, {renderer_value}, {content_value}, {color_value}, {mj_model_value} {resolution_value}"
        else:
            renderer_value = Settings.renderers[renderer]["value"]
            content_value = Settings.contents[content]["value"]
            type_value = Settings.types[type]["value"]
            resolution_value = Settings.aspect_ratios[resolution]["value"]
            color_value = ""
            for color in colors:
                color_value += Settings.colors[color]["value"] + ", "

            prompt = f"{response}, {renderer_value}, {content_value}, {color_value}, {type_value} {resolution_value}"

        print(prompt)
        prompt = prompt.replace(", ", " ")
        prompt = re.sub(r"\s{2,}", " ", prompt)
        parameters = []
        while True:
            found = re.match(r"--no\s\S+", prompt)
            if not found:
                break
            start = found.start()
            end = found.end()
            
            parameters.append(prompt[start:end])
            
            promptlist = list(prompt)
            for i in range(start, end + 1):
                promptlist[i] = ""
            prompt = "".join(promptlist)
        
        prompt += " " + " ".join(parameters)
        if url:
            return f"{url} {prompt}"
        else:
            return prompt

    def __show(self, list: list[dict], from_zero: bool = False):
        for i in range(len(list)):
            name = list[i]["name"]
            if i == 0 and not from_zero:
                print(f"[{YELLOW}Empty{RESET}] {name}")
            else:
                print(f"[{YELLOW}  {i}  {RESET}] {name}")

    def __check_parameter(
        self, parameter: str, parameter_parent: list[dict], parameter_name: str
    ):
        if parameter == "":
            parameter = 0
        elif parameter.isdigit():
            parameter = int(parameter)
            if parameter < 0 or parameter > len(parameter_parent) - 1:
                exit(
                    f"[{RED}Error{RESET}] {parameter_name} must be between 1 and {len(parameter_parent) - 1}"
                )
        else:
            exit(f"[{RED}Error{RESET}] {parameter_name} must be a number")
        return parameter

    def prompt(self):
        os.system("cls")

        prompt = None

        print(f"{GREEN}Prompt model{RESET}")
        self.__show(Settings.prompt_models)
        prompt_model = input(f"-> ")
        prompt_model = self.__check_parameter(
            prompt_model, Settings.prompt_models, "Prompt model"
        )

        print(f"{GREEN}MidJourney model{RESET}")
        self.__show(Settings.mj_models)
        mj_model = input(f"-> ")
        mj_model = self.__check_parameter(
            mj_model, Settings.mj_models, "MidJourney model"
        )

        print(f"{GREEN}Image description{RESET}")
        prompt: str = input(f"-> {BOLD}")

        print(
            f"{RESET}{GREEN}Description count (The more, the more details and more chaos){RESET}"
        )
        count: str = input(f"-> ")
        if count.isdigit():
            count = int(count)
        else:
            exit(f"[{RED}Error{RESET}] Description count must be a number")

        if not mj_model in [0, 1]:
            prompt = self.ask(
                text=prompt,
                count_words=count,
                prompt_model=prompt_model,
                mj_model=mj_model,
            )
        else:
            print(f"{RESET}{GREEN}Advanced settings{RESET}")
            self.__show(Settings.advanced_settings)
            advanced: str = input(f"-> ")
            if advanced == "1":
                prompt = self.ask(
                    text=prompt, count_words=count, prompt_model=prompt_model
                )

            else:
                type = 0
                if mj_model == 0:
                    print(f"{GREEN}Type image{RESET}")
                    self.__show(Settings.types)
                    type = input(f"-> ")
                    type = self.__check_parameter(type, Settings.types, "Type")

                print(f"{GREEN}Aspect ratio{RESET}")
                self.__show(Settings.aspect_ratios)
                resolution = input(f"-> ")
                resolution = self.__check_parameter(
                    resolution, Settings.aspect_ratios, "Resolution"
                )

                print(f"{GREEN}Render - Affects things (Beta){RESET}")
                self.__show(Settings.renderers)
                renderer = input(f"-> ")
                renderer = self.__check_parameter(
                    renderer, Settings.renderers, "Renderer"
                )

                print(f"{GREEN}Content - Additional refinements{RESET}")
                self.__show(Settings.contents)
                content = input(f"-> ")
                content = self.__check_parameter(content, Settings.contents, "Content")

                print(f"{GREEN}Color change - Enter separated by commas{RESET}")
                self.__show(Settings.colors)
                colors = input(f"-> ")
                colors = colors.split(",")
                if colors == [""]:
                    colors = []
                color_nubmers = []
                for color in colors:
                    color = color.replace(" ", "")
                    if color.isdigit():
                        color_nubmers.append(int(color))
                    else:
                        exit(f"[{RED}Error{RESET}] Color must be a number")

                prompt = self.ask(
                    text=prompt,
                    count_words=count,
                    type=type,
                    resolution=resolution,
                    renderer=renderer,
                    content=content,
                    prompt_model=prompt_model,
                    colors=color_nubmers,
                    mj_model=mj_model
                )

        print()
        print(f"{BLUE}Prompt{RESET}: {BOLD}\n" + prompt + RESET)
        return prompt
