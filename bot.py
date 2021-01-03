from datetime import datetime, timedelta
import pytz
import discord
import random
import time
import asyncio


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = discord.Client()


@client.event
async def on_ready():
    print('BlazingFart is ready, version' + str(discord.__version__))

    # bot id: 688796080804200487
    # my id: 433822554277281792


def show_time(datetime):
    day = datetime.day
    month = datetime.month
    year = datetime.year
    hour = datetime.hour
    minute = datetime.minute
    s = str(hour) + ':' + str(minute) + ' ' + str(day) + '/' + str(month) + '/' + str(year)
    return s


@client.event
async def on_message(message):
    if message.content.startswith('-'):
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
            embed.add_field(name='-getAndSendPinnedMsg #channel:',
                            value='gỡ ghim tin nhắn ở channel được gọi và gửi đến channel được mention', inline=False)

            await message.channel.send(embed=embed)

        if message.content.startswith('-random'):
            choice = str(message.content)
            print(choice)

        if message.content.startswith('-read') != -1 and not message.author.bot:
            print(message.mentions[0])
            print(len(message.mentions))

        if message.content.startswith('-jail') and (
                message.author.id == 433822554277281792 or message.author == message.author.guild.owner):
            for role in message.author.guild.roles:
                if str(role.name).lower() == 'người qua đường':
                    prison_role = role
                    break

            mention = message.mentions
            member = mention[0]
            msg = await message.channel.send('Do you want to jail this person? ' + str(member.mention))
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await message.channel.send('👎')
            else:
                await member.add_roles(prison_role)

        if message.content.startswith('-release') != -1 and (
                message.author.id == 433822554277281792 or message.author == message.author.guild.owner):
            mention = message.mentions
            member = mention[0]
            for role in member.roles:
                if str(role.name).lower() == 'người qua đường':
                    await member.remove_roles(role)
                    break

        if message.content.startswith('-time') != -1:
            # other timezones depends on west_time
            west_tz = pytz.timezone('US/Pacific')
            west_time = datetime.now(west_tz)
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
            if message.author == message.author.guild.owner or message.author.id == 433822554277281792:
                await message.channel.send(
                    "Are you sure to delete this channel's messages?\nY/y or N/n")
                check = False
                while not check:
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

        if message.content.startswith("-getAndSendPinnedMsg") != -1 and message.author == message.author.guild.owner:
            channel_mention_id = message.channel_mentions[0].id
            channel = message.author.guild.get_channel(channel_mention_id)
            msg = await message.channel.pins()
            for i in range(len(msg) - 1, -1, -1):
                await channel.send(str(len(msg) - i) + ". " + str(msg[i].author) + " said \n" + msg[i].content)
            await msg[i].unpin()

        if str(message.content) == "-locMem":
            category = ['Buôn chuyện', 'Text']
            # category id = 694822802108186666
            # if message.author == message.author.guild.owner:
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
                await message.channel.send(
                    "There is no member joined before " + str(week_before.date()) + " with less than " + str(
                        message_num) + " messages sent. \nNo further action needed. Have a good day ;) " + str(
                        message.author.mention))
            else:
                await message.channel.send(
                    "Do you want to kick " + str(len(inactive_member_id)) + " member(s) listed above? \nY/y or N/n")
                check = False
                while (check == False):
                    msg = await client.wait_for('message', timeout=600)
                    if msg.author == message.author and msg.channel == message.channel:
                        if str(msg.content) == 'Y' or str(msg.content) == 'y':
                            check = True
                            for i in range(len(inactive_member_id)):
                                mem = guild.get_member(inactive_member_id[i])
                                await mem.kick(reason='Inactive in text channels')
                            await message.channel.send(
                                "Kicking members completed, have a good day ;) " + str(message.author.mention))
                        elif str(msg.content) == 'N' or str(msg.content) == 'n':
                            check = True
                            await message.channel.send(
                                "Action completed, have a good day ;) " + str(message.author.mention))
                        else:
                            await message.channel.send("Invalid response, please try again")
                    else:
                        await message.channel.send('Only the owner of this server can do this!')

        if message.content.startswith('-rabbitdoubt') != -1:
            top_role = str(message.author.top_role)
            if top_role == 'Police' or top_role == 'Mascot' or message.author.guild.owner == message.author or message.author.id == 433822554277281792:
                print('Authorized')
            players_list = []
            for mention in message.mentions:
                players_list.append(mention)
            i = 0
            while i < len(players_list):
                if players_list.count(players_list[i]) > 1:
                    players_list.remove(players_list[i])
                    i -= 1
                i += 1

            if len(players_list) >= 6:
                # retrieve games' roles from guild
                # input: guild
                # output: dict{<str> role.name, <discord.Role> role}
                roles_dict = get_game_roles(message.author.guild)
                prev_roles_dict = set_game_roles(players_list, roles_dict)
                # assign roles
                # input: list[<discord.Member> player]
                # output: dict {<int> player_id: <str> rabbit or wolf}
                player_role_dict = await game_prep(players_list)
                for channel in message.author.guild.channels:
                    if channel.name == 'village':
                        village_channel = channel
                # game goes here
                # while game_check == False:
                print('return default roles')

                await return_roles(prev_roles_dict)

                print('finish everything')
            else:
                await message.channel.send('You do not have enough players to play the game (at least 6)')

        if message.content.startswith('-roles') != -1:
            mention = message.mentions
            member = message.author
            if len(mention) != 0:
                member = mention[0]

            title = 'Role list of ' + member.display_name
            embed = discord.Embed(
                title=title
            )
            roles_list = member.roles
            for role in roles_list:
                embed.add_field(name='Role:', value=str(role) + ' ' + str(role.id), inline=False)
            await message.channel.send(embed=embed)

            # role is discord.Role type

        # for role in roles_list:
        # embed.add_field(name='Role:', value= str(role) + ' ' + str(role.id), inline=False)
        # await message.channel.send(embed=embed)


# input: list [<int> discord.Member.id]
# output: dict {<int> member.id: <str> game's role}
async def game_prep(players_list):
    player_role_dict = {}
    for member in players_list:
        player_role_dict[member] = 'none'

    role_counter = {}
    role_counter['wolf'] = 0
    role_counter['rabbit'] = 0
    role_max_counter = {}
    role_max_counter['wolf'] = 1 + int((len(players_list) - 6) / 2)
    role_max_counter['rabbit'] = len(players_list) - role_max_counter['wolf']

    while role_counter['wolf'] + role_counter['rabbit'] != len(players_list):
        # loop to find a random player
        random_player = random.choice(list(player_role_dict.keys()))
        # role_zero = player_role_dict[random_player_id][0]
        while player_role_dict[random_player] == 'none':
            random_player = random.choice(list(player_role_dict.keys()))
        # randomize a role
        role = ''
        if random.randint(1, 100) % 2 == 0:
            role = 'rabbit'
        else:
            role = 'wolf'
        # check if role is givable or not aka if role exceeds maximum
        if role_counter[role] >= role_max_counter[role]:
            if role == 'wolf':
                role = 'rabbit'
            else:
                role = 'wolf'
        # assign that player the role
        player_role_dict[random_player] = role
        role_counter[role] += 1

    return player_role_dict


# input: discord.Guild
# output: dict{wolf: <int>wolf_id, rabbit: <int>rabbit_id, dead: <int>dead_id}
# done
def get_game_roles(guild):
    roles_dict = {}
    for role in guild.roles:
        if role.name == 'alive':
            roles_dict['alive'] = role
        elif role.name == 'dead':
            roles_dict['dead'] = role
    return roles_dict


# input: <dict> player_role_dict
# output: no output
# done
async def return_roles(player_prev_roles_dict):
    for member in player_prev_roles_dict:
        for role in member.roles:
            if role.name != '@everyone':
                await member.remove_roles(role)

    for member in player_prev_roles_dict:
        for role in player_prev_roles_dict[member]:
            await member.add_roles(role)


# input: <dict>
# output: <bool> kill completion
# done
async def bite(player_role_dict, roles_dict, message):
    killed_success = False

    victim = message.mentions[0]
    await message.channel.send('Wolf chose to kill this player: ' + str(victim.name))
    if player_role_dict[victim][0].name == 'rabbit':
        player_role_dict[victim][0] = roles_dict['dead']
        await victim.add_roles(player_role_dict[victim][0])
        killed_success = True

    return killed_success


# done
async def send_alive_players(player_role_dict, channel):
    embed = discord.Embed(
        title='Alive players:'
    )
    for member in player_role_dict:
        if player_role_dict[member][0].name == 'rabbit':
            embed.add_field(name=str(member.name), inline=False)
    await channel.send(embed=embed)


# input: list[<discord.Member>], dict {'alive' : discord.Role, 'dead' : discord.Role}
# output: dict{<discord.Member> player, list[discord.Role] role in server}
# functions: return roles in server, remove current roles, set game's role
# done
async def set_game_roles(player_list, roles_dict):
    prev_role_dict = {}
    for member in player_list:
        prev_role = []
        for role in member.roles:
            if role.name != '@everyone':
                prev_role.append(role)
                await member.remove_roles(role)

        prev_role_dict[member] = prev_role
        await member.add_roles(roles_dict['alive'])

    return prev_role_dict


async def game_check(player_role_dict, channel):
    role_count = {}
    role_count['wolf'] = 0
    role_count['rabbit'] = 0
    role_count['dead'] = 0
    for member in player_role_dict:
        role_count[player_role_dict[member][0].name] += 1

    state = 'none'
    if role_count['wolf'] == 0:
        if role_count['rabbit'] > 0:
            state = 'rabbit'
            await channel.send('Rabbit wins!')
    else:
        if role_count['rabbit'] <= role_count['wolf']:
            state = 'wolf'
            await channel.send('Wolf wins!')
    return state


async def calc_day_time(player_role_dict):
    time = 5 * 60
    for member in player_role_dict:
        if player_role_dict[member][0].name != 'dead':
            time += 2 * 60
    return time


async def game(player_role_dict, village_channel, dead_channel):
    while game_check(player_role_dict) == 'none':
        time_day = calc_day_time(player_role_dict)
        day_timer(time_day, village_channel)


async def day_timer(time, channel):
    await channel.send('You may start discussing')


client.run(token)
