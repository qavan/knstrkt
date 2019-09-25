import discord
import random
import os
import sys
import cfg
from discord.ext import commands
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Logged in as', "\""+bot.user.name+"\"", 'ID:', bot.user.id)


@bot.command(description='integer roll')
async def roll(ctx, a: str, *b: int):
    await ctx.message.delete()
    if a == 'e':
        embed = discord.Embed(title='KONSTRAKT', description='!roll Example:', color=discord.Colour.dark_orange())
        embed.add_field(name="!roll A B", value='Gives the random int from A to B.', inline=False)
        embed.add_field(name="!roll A/B", value='Gives the random int from 1 to B A times.', inline=False)
        await ctx.send(embed=embed, delete_after=cfg.del_timeout)
        return
    try:
        rolls, maximum = map(int, a.split('/'))
    except ValueError:
        try:
            result = str(random.randint(int(a), b[0]))
            await ctx.send(result, delete_after=cfg.del_timeout)
            return
        except (ValueError, IndexError):
            await ctx.send('Format has to be in N to N or N/N! Examples: !roll e .')
            return
    result = ', '.join(str(random.randint(1, maximum)) for x in range(rolls))
    await ctx.send(result, delete_after=cfg.del_timeout)


@bot.command(description='random choose from variants')
async def choose(ctx, *choices: str):
    await ctx.send('Chosen', random.choice(choices))


@bot.command(description='bot restart')
async def r(ctx):
    await ctx.send('Bot restarting...')
    os.execl(sys.executable, 'python3.6', __file__, *sys.argv[1:])


@bot.command(description='delete messages from chat[channel]')
async def delete(ctx, count: str = '', name: str = ''):
    print(count, name)
    await ctx.message.delete()
    if count == '' and name == '':
        await ctx.send('Unknown format! Examples: !delete e .')
        return
    elif count != 'e' and count != 'all' and name == '':
        try:
            counter = int(count)
            async for message in ctx.channel.history():
                await message.delete()
                counter -= 1
                if counter == 0:
                    break
            await ctx.send('Has been deleted ' + count + ' message(s).', delete_after=cfg.del_timeout)
            return
        except ValueError:
            await ctx.send('Unknown format! Examples: !delete e .')
            return
    elif count == 'e':
        embed = discord.Embed(title='KONSTRAKT', description='!delete Example:', color=discord.Colour.dark_orange())
        embed.add_field(name="!delete N", value='Deletes last N messages in channel.', inline=False)
        embed.add_field(name="!delete all", value='Deletes all messages in channel.', inline=False)
        embed.add_field(name="!delete 5 @member", value='Deletes last 5 messages of mentioned member.', inline=False)
        embed.add_field(name="!delete e", value='Gives this help.', inline=False)
        await ctx.send(embed=embed, delete_after=cfg.del_timeout)
        return
    elif count == 'all' and name == '':
        counter = 0
        async for message in ctx.channel.history():
            counter += 1
            await message.delete()
        await ctx.send('All messages('+str(counter)+') in channel has been deleted.', delete_after=cfg.del_timeout)
        return
    elif count != '' and name != '':
        try:
            counter = int(count)
            async for message in ctx.channel.history():
                if message.author.id == ctx.message.mentions[0].id:
                    counter -= 1
                    await message.delete()
                    if counter == 0:
                        break
            await ctx.send('Founded and deleted [' + str(abs(counter-int(count))) + '] message(s) from preassigned['
                           + str(count) + '] of userID=' + str(ctx.message.mentions[0].id) + '.')
        except (ValueError, IndexError):
            await ctx.send('Unknown format! Examples: !delete e .')
            return
bot.run('')
