import disnake
from disnake.ext import commands
import disnake.ui as ui
import asyncio

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

bot = commands.Bot(command_prefix = '!', test_guilds = [Your guilds here...], intents = disnake.Intents.all(), command_sync_flags=command_sync_flags)

@bot.event
async def on_ready():
    print("Bot has started!")

class LoginModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Введите ваш никнейм",
                placeholder="Nickname",
                custom_id="nickname",
                style=disnake.TextInputStyle.short
            )
        ]

        super().__init__(
            title="Проверка",
            custom_id="modal",
            components=components
        )

    # Обработка ответа
    async def callback(self, inter: disnake.ModalInteraction):
        await inter.author.edit(nick=inter.data.components[0]["components"][0]["value"])
        await inter.author.add_roles(disnake.utils.get(inter.guild.roles, id=Your role here...))
        await inter.response.send_message("ㅤ")
        await inter.delete_original_response(delay=None)
        await asyncio.sleep(3)
        await inter.author.edit(nick=None)
        await inter.author.remove_roles(disnake.utils.get(inter.guild.roles, id=Your role here...))

@bot.command()
async def soo(ctx):
    embed = disnake.Embed(title="Вы попали на проверку!",
                          description="Здравствуй, уважаемый игрок! Ты попал на проверку на сервере DragonsGrief. Чтобы начать проходить проверку, нажимай на кнопку ниже, вводи свой ник и заходи в канал \"Ожидание проверки\". Желаем удачного прохождения!",
                          colour=0xf5c000)
    embed.set_author(name="DragonsGrief",
                     icon_url="https://cdn.discordapp.com/attachments/1238736321896382546/1244022874054983743/framedev1.png?ex=66539a16&is=66524896&hm=ea4105611d1fef8096eaec96da9168d66e826b46b68f53aef5fce390804f14c9&")

    buttons = ui.View()
    buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="modal"))

    await ctx.channel.purge(limit=1)

    await ctx.send(embed=embed, components=[
        disnake.ui.Button(
            style=disnake.ButtonStyle.blurple,
            label="Верификация"
        )
    ],)

@bot.event
async def on_button_click(inter: disnake.MessageInteraction):
    modal = LoginModal()
    await inter.response.send_modal(modal=modal)

@bot.slash_command(name="modal", description="modal")
async def modal(inter):
    modal = LoginModal()
    await inter.response.send_modal(modal=modal)

bot.run("Your token here...")
