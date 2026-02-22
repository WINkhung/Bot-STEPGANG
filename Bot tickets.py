import discord
from discord.ext import commands
from myserver import server_on

TOKEN = 'MTQ3NDgyMzkxNDY5MjgwNDgwMQ.Gp53sD.8SpGuqCm7E34gkK0o_Kp7C1m7h6AiujSONDFHs'
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ===== ปุ่มสร้าง Ticket =====
class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 สร้าง Ticket",
                       style=discord.ButtonStyle.green,
                       custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction,
                            button: discord.ui.Button):

        guild = interaction.guild
        user = interaction.user

        # เช็คว่ามี ticket อยู่แล้วไหม
        existing_channel = discord.utils.get(guild.text_channels,
                                             name=f"ticket-{user.name}")
        if existing_channel:
            await interaction.response.send_message("คุณมี Ticket อยู่แล้ว!",
                                                    ephemeral=True)
            return

        # สร้างห้อง
        overwrites = {
            guild.default_role:
            discord.PermissionOverwrite(read_messages=False),
            user:
            discord.PermissionOverwrite(read_messages=True,
                                        send_messages=True),
            guild.me:
            discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(name=f"ticket-{user.name}",
                                                  overwrites=overwrites)

        await channel.send(f"{user.mention} สวัสดี! ทีมงานจะมาตอบเร็ว ๆ นี้")
        await interaction.response.send_message(
            f"สร้าง Ticket แล้ว: {channel.mention}", ephemeral=True)


# ===== คำสั่งส่งปุ่ม Ticket =====
@bot.command()
async def setup(ctx):
    embed = discord.Embed(title="📩 ระบบ Ticket",
                          description="กดปุ่มด้านล่างเพื่อสร้าง Ticket",
                          color=discord.Color.blue())
    await ctx.send(embed=embed, view=TicketView())


@bot.event
async def on_ready():
    print(f"Bot พร้อมใช้งานแล้ว: {bot.user}")
    bot.add_view(TicketView())

server_on()

bot.run(TOKEN)
