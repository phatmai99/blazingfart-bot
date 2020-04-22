from datetime import datetime, timedelta,date

import discord
import time
import asyncio
from discord import Guild
from discord import Role


# id = 688502199168663553


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to the server {member.mention}""")


    #bot id: 688796080804200487
    #my id: 433822554277281792

    #class Player:
    #    def __init__:

    #if str(message) == "!playTienLen":
    #    channel = await Guild.create_text_channel('Tien-Len-Channel')
    #    channel.send(f"""Who do you want to invite? (tag them in)""")
    #    last_msg = channel.fetch_message(channel.last_message_id)
    #    player_list = last_msg.raw_channel_mentions
    #    for i in range(len(player_list)):

def show_time(datetime):
    day = datetime.day
    month = datetime.month
    year = datetime.year
    hour = datetime.hour
    minute = datetime.minute
    s = str(hour)+':'+str(minute)+' '+str(day)+'/'+str(month)+'/'+str(year)
    return s

@client.event
async def on_message(message):
    if len(message.content) > 0:
        if message.content[0] == '-':
            if message.content == '-help':
                description = 'Available commands (prefix: -)'
                embed = discord.Embed(
                    title='Commands',
                    description=description
                )
                embed.add_field(name='-locMem:', value='lọc mem ít tương tác trong các text-channels', inline=False)
                embed.add_field(name='-time:', value='hiện thời gian hiện tại của thành viên trong server', inline=False)
                embed.add_field(name='-time @member:', value='hiện thời gian hiện của member được mention', inline=False)
                embed.add_field(name='-deleteMessage:', value='xoá toàn bộ tin nhắn trong một text-channel', inline=False)
                embed.add_field(name='-getAndSendPinnedMsg #channel:', value='gỡ ghim tin nhắn ở channel được gọi và gửi đến channel được mention', inline=False)

                await message.channel.send(embed=embed)

            if message.content.find('-read') != -1 and message.author.bot == False:
                print(message.mentions)
                print(len(message.mentions))

            if message.content.find('-time') != -1:
                gmt_time = datetime.today()
                west_time = gmt_time + timedelta(hours=-7)
                east_time = west_time + timedelta(hours=3)
                vn_time = west_time + timedelta(hours=14)
                mention = message.mentions
                embed = discord.Embed()

                if len(mention) == 0:
                    embed.add_field(name='US West time: ', value=show_time(west_time), inline=True)
                    embed.add_field(name='US East time: ', value=show_time(east_time), inline=True)
                    embed.add_field(name='VN time: ', value=show_time(vn_time), inline=True)
                else:
                    mentioned_user_id = mention[0].id
                    #                   Chaos                  Mola                 Mì              Meow
                    east_user_id = [559602926809513986, 344499560972025856, 680927590101286962, 653656019041386496]
                    #                   Phat                andrea.
                    west_user_id = [433822554277281792, 596575593420685344]
                    if mentioned_user_id in east_user_id:
                        s = mentioned_user_id
                        embed.add_field(name='US East time: ', value=show_time(east_time), inline=True)
                    elif mentioned_user_id in west_user_id:
                        embed.add_field(name='US West time: ', value=show_time(west_time), inline=True)
                    else:
                        embed.add_field(name='VN time: ', value=show_time(vn_time), inline=True)
                await message.channel.send(embed=embed)

            if str(message.content) == "-deleteMessage":
                if message.author == message.author.guild.owner:
                    await message.channel.send(
                        "Are you sure to delete this channel's messages?\nY/y or N/n")
                    check = False
                    while (check == False):
                        msg = await client.wait_for('message', timeout=600)
                        if msg.author == message.author and msg.channel == message.channel:
                            if str(msg.content) == 'Y' or str(msg.content) == 'y':
                                check = True
                                async for msg in message.channel.history(limit=None):
                                    await msg.delete()
                            elif str(msg.content) == 'N' or str(msg.content) == 'n':
                                check = True
                                await message.channel.send("Action cancelled" + str(message.author.mention))
                            else:
                                await message.channel.send("Invalid response, please try again")
                else:
                    await message.channel.send('Only the owner of this server can do this!')

            if message.content.find("-getAndSendPinnedMsg") != -1 and message.author == message.author.guild.owner:
                channel_mention_id = message.channel_mentions[0].id
                channel = message.author.guild.get_channel(channel_mention_id)
                msg = await message.channel.pins()
                for i in range(len(msg) - 1, -1, -1):
                    await channel.send(str(len(msg) - i) + ". " + str(msg[i].author) + " said \n" + msg[i].content)
                    await msg[i].unpin()


            if str(message.content) == "-locMem":
                category = ['Buôn chuyện', 'Text']
                # category id = 694822802108186666
                if message.author == message.author.guild.owner:
                    text_channels = []
                    newbie_members = []
                    days_delta = 7
                    if str(message.channel.category) in category:
                        days_delta = -1
                        print('Change days_delta to ' + str(days_delta))
                    week_before = datetime.today() - timedelta(days=days_delta)
                    guild = message.guild

                    for chn in guild.channels:
                        if str(chn.type) == 'text' and str(chn.category) in category:
                            text_channels.append(chn)
                    await message.channel.send("Finish fetching channels")

                    for member in guild.members:
                        highest_role = member.roles[len(member.roles) - 1]
                        if str(highest_role) == 'Newbie' or str(highest_role) == 'Homies':
                            if member.joined_at < week_before:
                                newbie_members.append(member)
                    await message.channel.send("Finish fetching members")

                    dict = {}
                    for i in range(len(newbie_members)):
                        dict[newbie_members[i].id] = 0

                    key = list(dict.keys())
                    message_num = 10
                    if str(message.channel.category) == 'Text':
                        message_num = 1000
                    inactive_member_id = []

                    counter = 0
                    await message.channel.send(
                        "Searching through server's message history, this will take a while, please be patient ^^")

                    for i in range(len(text_channels)):
                        async for msg in text_channels[i].history(limit=None):
                            counter += 1
                            if int(msg.author.id) in dict:
                                dict[msg.author.id] += 1
                    await message.channel.send("Total: " + str(counter) + " messages")
                    embed_inMember = discord.Embed()
                    for i in range(len(key)):
                        mem = guild.get_member(key[i])
                        if (dict[key[i]]) < message_num:
                            inactive_member_id.append(mem.id)
                            s = str(dict[key[i]]) + " messages from " + str(mem.joined_at.date())
                            embed_inMember.add_field(name=str(mem.name), value=s, inline=False)

                    await message.channel.send(embed=embed_inMember)

                    if len(inactive_member_id) == 0:
                        await message.channel.send("There is no member joined before " + str(week_before.date()) + " with less than " + str(message_num) + " messages sent. \nNo further action needed. Have a good day ;) " + str(message.author.mention))
                    else:
                        await message.channel.send("Do you want to kick " + str(len(inactive_member_id)) + " member(s) listed above? \nY/y or N/n")
                        check = False
                        while (check == False):
                            msg = await client.wait_for('message', timeout=600)
                            if msg.author == message.author and msg.channel == message.channel:
                                if str(msg.content) == 'Y' or str(msg.content) == 'y':
                                    check = True
                                    for i in range(len(inactive_member_id)):
                                        mem = guild.get_member(inactive_member_id[i])
                                        await mem.kick(reason='Inactive in text channels')
                                    await message.channel.send("Kicking members completed, have a good day ;) " + str(message.author.mention))
                                elif str(msg.content) == 'N' or str(msg.content) == 'n':
                                    check = True
                                    await message.channel.send("Action completed, have a good day ;) " + str(message.author.mention))
                                else:
                                    await message.channel.send("Invalid response, please try again")
                else:
                    await message.channel.send('Only the owner of this server can do this!')

#updating tokens
#updating tokens #2
client.run(token)
