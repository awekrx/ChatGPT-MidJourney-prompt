import os
import re

from revChatGPT.V1 import Chatbot as ChatbotV1
from revChatGPT.V3 import Chatbot as ChatbotV3
from .settings.V5 import V5_settings
from .settings.V4 import V4_settings
from .settings.niji import niji_settings
from .settings.testp import testp_settings


class PromptGenerator:
    url_regex = r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
    no_param_regex = r"(no\s\w+)\:\:\d+|--no\s\S+"
    aspect_ratio_regex = r"^\d+:\d+$"

    def __init__(self, config):
        if config["api_key"]:
            self.chatbot = ChatbotV3(config["api_key"])
        else:
            self.chatbot = ChatbotV1(config)

    def __create_prompt(self, text: str, model: str, words: int):
        return (
            open(f"{os.path.dirname(__file__)}/prompt_models/{model}.txt", "r")
            .read()
            .replace("NNN", str(words))
            .replace("TEXT", text)
        )

    def __ask(self, prompt):
        response = ""
        if isinstance(self.chatbot, ChatbotV1):
            for data in self.chatbot.ask(prompt):
                response = data["message"]
        else:
            response = self.chatbot.ask(prompt)

        if response[0] == '"':
            response = response[1:]
            if response[-1] == '"':
                response = response[:-1]

        if response[-1] == ".":
            response = response[:-1]

        return response

    def __slice_no_parameters(self, response):
        no_parameters = []
        found = re.search(self.no_param_regex, response)
        while found:
            start = found.start()
            end = found.end()

            if found.group(1):
                no_parameters.append(f"--{found.group(1)}")
            else:
                no_parameters.append(found.group())

            response_to_list = list(response)
            for i in range(start, end):
                # Bug: extra space
                response_to_list[i] = ""
            response = "".join(response_to_list)
            found = re.search(self.no_param_regex, response)

        return response, no_parameters

    def __check_parameter_in_config_and_settings(
        self, config_name, model_settings_name, config, model_settings
    ):
        return (
            config_name in config
            and config[config_name] in model_settings[model_settings_name]
        )

    def __add_custom_parameters_to_prompt(
        self, prompt, config, settings, exclude: list[str] = []
    ):
        parameters = [
            {
                "config_name": "renderer",
                "settings_name": "renderers",
            },
            {
                "config_name": "content",
                "settings_name": "contents",
            },
            {
                "config_name": "type",
                "settings_name": "types",
            },
            {
                "config_name": "aspect_ratio",
                "settings_name": "aspect_ratios",
            },
        ]
        for parameter in parameters:
            if not parameter["config_name"] in exclude:
                if self.__check_parameter_in_config_and_settings(
                    parameter["config_name"],
                    parameter["settings_name"],
                    config,
                    settings,
                ):
                    prompt += (
                        " "
                        + settings[parameter["settings_name"]][
                            config[parameter["config_name"]]
                        ]
                    )
        return prompt

    def __check_and_add_color(self, prompt, config):
        if "color" in config and isinstance(config["color"], str):
            prompt += " " + f"{config['color']}::10"
        return prompt

    def __check_and_add_url(self, prompt, config):
        if "url" in config and re.search(self.url_regex, config["url"]):
            prompt = config["url"] + " " + prompt
        return prompt

    def __check_and_add_no_parameters(self, prompt, no_parameters):
        if len(no_parameters) > 0:
            prompt += " " + " ".join(no_parameters)
        return prompt

    def V5(self, text: str, config: dict[str, str] = {}, words: int = 35):
        model = "weights"
        if self.__check_parameter_in_config_and_settings(
            "model", "prompt_models", config, V5_settings
        ):
            model = V5_settings["prompt_models"][config["model"]]

        gpt_prompt = self.__create_prompt(text, model, words)
        gpt_response = self.__ask(gpt_prompt)
        mj_prompt, no_parameters = self.__slice_no_parameters(gpt_response)

        mj_prompt = self.__check_and_add_url(mj_prompt, config)

        mj_prompt = self.__check_and_add_color(mj_prompt, config)

        mj_prompt = self.__add_custom_parameters_to_prompt(
            mj_prompt, config, V5_settings, ["aspect_ratio"]
        )

        if "aspect_ratio" in config and re.search(
            self.aspect_ratio_regex, config["aspect_ratio"]
        ):
            mj_prompt += " " + f"--ar {config['aspect_ratio']}"

        mj_prompt += " --v 5 --s 1000 --q 2"

        mj_prompt = self.__check_and_add_no_parameters(mj_prompt, no_parameters)

        return mj_prompt

    def V4(self, text: str, config: dict[str, str] = {}, words: int = 35):
        model = "weights"
        if self.__check_parameter_in_config_and_settings(
            "model", "prompt_models", config, V4_settings
        ):
            model = V4_settings["prompt_models"][config["model"]]

        gpt_prompt = self.__create_prompt(text, model, words)
        gpt_response = self.__ask(gpt_prompt)
        mj_prompt, no_parameters = self.__slice_no_parameters(gpt_response)

        mj_prompt = self.__check_and_add_url(mj_prompt, config)

        mj_prompt = self.__check_and_add_color(mj_prompt, config)

        mj_prompt = self.__add_custom_parameters_to_prompt(
            mj_prompt, config, V4_settings
        )

        mj_prompt += " --v 4 --s 1000 --q 5"

        mj_prompt = self.__check_and_add_no_parameters(mj_prompt, no_parameters)

        return mj_prompt

    def niji(self, text: str, config: dict[str, str] = {}, words: int = 35):
        model = "weights"
        if self.__check_parameter_in_config_and_settings(
            "model", "prompt_models", config, niji_settings
        ):
            model = niji_settings["prompt_models"][config["model"]]

        gpt_prompt = self.__create_prompt(text, model, words)
        gpt_response = self.__ask(gpt_prompt)
        mj_prompt, no_parameters = self.__slice_no_parameters(gpt_response)

        mj_prompt = self.__check_and_add_url(mj_prompt, config)

        mj_prompt = self.__check_and_add_color(mj_prompt, config)

        mj_prompt = self.__add_custom_parameters_to_prompt(
            mj_prompt, config, niji_settings, ["type"]
        )

        mj_prompt += " --niji --q 2"

        mj_prompt = self.__check_and_add_no_parameters(mj_prompt, no_parameters)

        return mj_prompt

    def testp(self, text: str, config: dict[str, str] = {}, words: int = 35):
        gpt_prompt = self.__create_prompt(text, "artistic", words)
        gpt_response = self.__ask(gpt_prompt)
        mj_prompt, no_parameters = self.__slice_no_parameters(gpt_response)

        mj_prompt = self.__check_and_add_url(mj_prompt, config)

        if self.__check_parameter_in_config_and_settings(
            "aspect_ratio", "aspect_ratios", config, testp_settings
        ):
            mj_prompt += " " + testp_settings["aspect_ratios"][config["aspect_ratio"]]

        mj_prompt += " --testp --s 1500"

        mj_prompt = self.__check_and_add_no_parameters(mj_prompt, no_parameters)

        return mj_prompt
