import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# Create_Poll variables:
numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

scheduler = AsyncIOScheduler()


class Create_Polls(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.polls = []

    # ----------POLL-----------------------------
            
    @commands.command(name="Poll", aliases=["createPoll", "CreatePoll"])
    @has_permissions(manage_guild=True)
    async def _createPoll(self, ctx, hours: int, question: str, *options):
        if len(options) > 10:
            await ctx.send("You can only supply up to 10 options.")
        else:
            embed = discord.Embed(title="Poll", description=question, colour=ctx.author.colour, timestamp=datetime.utcnow())

            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
                    ("Instructions", "React to vote!", False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            message = await ctx.send(embed=embed)

            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)

            self.polls.append((message.channel.id, message.id))

            scheduler.add_job(self.poll_ended, "date", run_date=datetime.now()+timedelta(seconds=hours),
									   args=[message.channel.id, message.id])
            scheduler.start()

    async def poll_ended(self, channel_id, message_id):
        message = await self.client.get_channel(channel_id).fetch_message(message_id)

        most_voted = max(message.reactions, key=lambda r: r.count)
        
        await message.channel.send(f"The most voted option was the number {most_voted} making it the winner!")
        #print("Its harder than it looks, said a wise man.")
        print(most_voted)

    @commands.Cog.listener()      # Events
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in (poll[1] for poll in self.polls):
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)

            for reaction in message.reactions:
                if (not payload.member.bot   #I dont get why client doesnt work and bot does, but it works this way
                    and payload.member in await reaction.users().flatten()
                    and reaction.emoji != payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, payload.member)


# --------------------------------------------


def setup(client):
    client.add_cog(Create_Polls(client))   

