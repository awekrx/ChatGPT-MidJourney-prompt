import configparser
import discord
from discord import app_commands
from modules.prompt import Prompt

config = configparser.ConfigParser()
config.read("config.ini")

auth = {
    "email": config["ChatGPT"]["email"],
    "password": config["ChatGPT"]["password"],
    "session_token": config["ChatGPT"]["session_token"],
}

prompter = Prompt(auth)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        await tree.sync()


client = Client()
tree = app_commands.CommandTree(client)


@tree.command(name="hello")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello from awekrx")


@tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Use `/prompt` for creating a new prompt for MidJourney bot\nMore info here https://github.com/awekrx/ChatGPT-MidJourney-prompt"
    )


@tree.command(
    name="prompt", description="Get prompt for MidJourney bot from your description"
)
@app_commands.describe(text="Image description")
@app_commands.describe(
    count_words="Description count (The more, the more details and more chaos)"
)
@app_commands.describe(mj_model="MidJourney model (v4, niji, testp)")
@app_commands.describe(prompt_model="Prompt model (weights, artistic)")
async def prompt(
    interaction: discord.Interaction,
    text: str,
    count_words: int,
    mj_model: str,
    prompt_model: str,
):
    mj_models = ["v4", "niji", "testp"]
    prompt_models = ["weights", "artistic"]
    if not mj_model in mj_models:
        await interaction.response.send_message(
            f"> `mj_model` not supported {mj_model}. Only: `v4`, `niji`, `testp`"
        )
    if not prompt_model in prompt_models:
        await interaction.response.send_message(
            f"> `prompt_model` not supported `{prompt_model}`. Only: `weights`, `artistic`"
        )
    await interaction.response.send_message("Generating...")
    response = prompter.ask(
        text=text,
        count_words=count_words,
        mj_model=mj_models.index(mj_model),
        prompt_model=prompt_models.index(prompt_model),
    )
    print(response)
    await interaction.edit_original_response(content=response)


client.run(config["Discord"]["bot_token"])
