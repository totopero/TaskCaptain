import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$')
all_assignments = {}
submissions = {}
emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('.start'):
        embed = discord.Embed(title='Let\'s get started', color=0xFF5733, description='Reply with .student if you are '
                                                                                      'a student, or reply with '
                                                                                      '.teacher if you are a teacher. '
                                                                                      'This will automatically '
                                                                                      'change your role and create '
                                                                                      'the according channels '
                                                                                      'necessary. Once your done '
                                                                                      'assigning roles, '
                                                                                      'type .mychannel. This will '
                                                                                      'create individual channels for '
                                                                                      'each user. '
                              )

        await message.channel.send(embed=embed)

    if msg.startswith('.student'):
        student_id = discord.utils.get(message.author.guild.roles, name="student").id
        await message.author.add_roles(discord.Object(student_id), reason='selected', atomic=True)

    if msg.startswith('.teacher'):
        teacher_id = discord.utils.get(message.author.guild.roles, name="teacher").id
        await message.author.add_roles(discord.Object(teacher_id), reason='selected', atomic=True)

    if msg.startswith('.mychannel'):
        if discord.utils.get(message.author.roles, name="student"):
            check = 0
            for channel in message.guild.channels:
                name = ''.join(ch for ch in message.author.name if ch.isalnum())
                if str(channel) == name.strip():
                    check += 1
            if check == 0:
                overwrites = {
                    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    message.guild.me: discord.PermissionOverwrite(read_messages=True),
                    message.author: discord.PermissionOverwrite(read_messages=True)
                }
                await message.guild.create_text_channel(f'{message.author.name}', overwrites=overwrites)

        if discord.utils.get(message.author.roles, name="teacher"):
            check2 = 0
            for channel in message.guild.channels:
                if str(channel) == 'teachers':
                    check2 += 1
            if check2 == 0:
                overwrites2 = {
                    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    message.guild.get_role(
                        discord.utils.get(message.author.guild.roles, name="teacher").id): discord.PermissionOverwrite(
                        read_messages=True),
                    message.guild.me: discord.PermissionOverwrite(read_messages=True),
                    message.author: discord.PermissionOverwrite(read_messages=True)
                }
                await message.guild.create_text_channel('teachers', overwrites=overwrites2)

    if msg.startswith('.assign'):
        if discord.utils.get(message.author.roles, name="student"):
            await message.channel.send('Students cannot use this command.')
        elif str(message.channel) != 'teachers':
            await message.channel.send('Teachers can only use this in their channel.')
        else:
            ask = discord.Embed(author=message.author.display_name, icon_url=message.author.avatar_url,
                                title='Creating a new Assignment',
                                description='Format assignment as: \n .create id(three digit number) %%% title %%% assignment description $$$ assignment due date(mm/dd/yyyy/hh/tt) \n Make sure the id is different than previous assignments')
            await message.channel.send(embed=ask)

    if msg.startswith('.create'):
        if discord.utils.get(message.author.roles, name="student"):
            await message.channel.send('Students cannot use this command.')
        elif str(message.channel) != 'teachers':
            await message.channel.send('Teachers can only use this in their channel.')
        else:
            msg = str(message.content)
            all_assignments[msg[8:11]] = msg[16:len(msg)]
            await message.channel.send(embed=display_assignment(message.author, msg[8:11], all_assignments[msg[8:11]]))
            await message.channel.send(
                'To change this assignment, simply create a new one with the same key. If you would like to assign this assignment to one individual, reply .giveto @studentuser key (mention them). To give to all students, reply .allassign key')

    if msg.startswith('.giveto'):
        if discord.utils.get(message.author.roles, name="student"):
            await message.channel.send('Students cannot use this command.')
        elif str(message.channel) != 'teachers':
            await message.channel.send('Teachers can only use this in their channel.')
        else:
            msg = str(message.content)
            user_id = int(msg[msg.find('@') + 2: msg.find('>')])
            student = await client.fetch_user(user_id)
            key = msg[msg.find('>') + 2:msg.find('>') + 5]
            name = student.name
            chname = ''.join(ch for ch in str(name) if ch.isalnum())
            channel = discord.utils.get(message.guild.channels, name=str(chname))
            await channel.send(f'Hi <@!{user_id}>! You have a new assignment.')
            await channel.send(embed=display_assignment(message.author, key, all_assignments[key]))

    if msg.startswith('.allassign'):
        if discord.utils.get(message.author.roles, name="student"):
            await message.channel.send('Students cannot use this command.')
        elif str(message.channel) != 'teachers':
            await message.channel.send('Teachers can only use this in their channel.')
        else:
            msg = str(message.content)
            key = msg[11:14]
            student_id = discord.utils.get(message.author.guild.roles, name="student").id
            for memb in message.author.guild.members:
                name = memb.name
                channel_name = ''.join(ch for ch in str(name) if ch.isalnum())
                for channel in message.guild.text_channels:
                    if str(channel) == channel_name:
                        await channel.send(f'Hi <@&{student_id}>! You have a new assignment.')
                        await channel.send(embed=display_assignment(message.author, key, all_assignments[key]))
    if msg.startswith('.done'):
        completion = discord.Embed(title=f'{message.author.display_name} completed assignment {msg[6:9]}',
                                   description=msg[9:len(msg)])
        teacher_channel = discord.utils.get(message.guild.text_channels, name='teachers')
        await teacher_channel.send(embed=completion)
        submissions[msg[6:9]].append(message.author.display_name)

    if msg.startswith('.checklist'):
        if discord.utils.get(message.author.roles, name="student"):
            await message.channel.send('Students cannot use this command.')
        elif str(message.channel) != 'teachers':
            await message.channel.send('Teachers can only use this in their channel.')
        else:
            await message.channel.send(
                embed=discord.Embed(title='Creating a Checklist:', description='format your response '
                                                                               'as (limit to 10 '
                                                                               'items): \n Item 1 $$$ '
                                                                               'Item 2 $$$ Item 3 $$$ '
                                                                               'Item 4'))
            unformatted_checklist = await client.wait_for('message', check=lambda m: m.author == message.author)
            unformatted_checklist = unformatted_checklist.content
            formatted_checklist = str(unformatted_checklist).split('$$$')
            if len(formatted_checklist) > 10:
                for i in range(1, len(formatted_checklist) - 9):
                    formatted_checklist.pop(10)
            checklist = ''
            for i in range(0, len(formatted_checklist)):
                checklist += f' {emojis[i]} {formatted_checklist[i]} \n \n '
            await message.channel.send(embed=discord.Embed(title='Checklist', description=checklist))
            await message.channel.send('To change this, simply restart the process with .checklist. Else, '
                                       'ping @student if you want to send it to every student, or ping @student_name '
                                       'if you want to send it to one student')
            recipient = await client.wait_for('message', check=lambda m: m.author == message.author)
            if recipient.content == '<@&' + str(discord.utils.get(message.guild.roles, name='student').id) + '>':
                for memb in message.author.guild.members:
                    name = memb.name
                    channel_name = ''.join(ch for ch in str(name) if ch.isalnum())
                    for channel in message.guild.text_channels:
                        if str(channel) == channel_name:
                            await channel.send(f'Hi {recipient.content}! You have a new checklist. React with each '
                                               f'number emoji to cross it out.')
                            sent_checklist = await channel.send(
                                embed=discord.Embed(title='Checklist', description=checklist))
                            for i in range(0, len(formatted_checklist)):
                                await sent_checklist.add_reaction(emojis[i])
            else:
                user_id = int(''.join(ch for ch in str(recipient.content) if ch.isalnum()))
                name = await client.fetch_user(user_id)
                chname = ''.join(ch for ch in str(name.display_name) if ch.isalnum())
                channel = discord.utils.get(message.guild.channels, name=str(chname))
                await channel.send(f'Hi {recipient.content}! You have a new checklist. React with each number emoji '
                                   f'to cross it out.')
                sent_checklist = await channel.send(embed=discord.Embed(title='Checklist', description=checklist))
                for i in range(0, len(formatted_checklist)):
                    await sent_checklist.add_reaction(emojis[i])


@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        num = reaction.emoji
        emoji_ind = 0
        for i in range(0, 10):
            if emojis[i] == num:
                emoji_ind = i
        edit = ''
        strike = False

        if emoji_ind != 9:
            start = reaction.message.embeds[0].description.find(emojis[emoji_ind]) + 3
            end = reaction.message.embeds[0].description.find(emojis[emoji_ind + 1])
            for i in range(0, len(reaction.message.embeds[0].description)):
                if i == start:
                    strike = True
                    edit = edit + (reaction.message.embeds[0].description[i] + '\u0336')
                if i == end - 6:
                    strike = False
                if not strike:
                    edit += reaction.message.embeds[0].description[i]
                if strike:
                    edit += (reaction.message.embeds[0].description[i] + '\u0336')

        if emoji_ind == 9:
            i = 0
            while i < (reaction.message.embeds[0].description.find(emojis[emoji_ind]) + 3):
                edit += reaction.message.embeds[0].description[i]
                i += 1
            while i < len(reaction.message.embeds[0].description):
                edit += (reaction.message.embeds[0].description[i] + '\u0336')

        new_embed = discord.Embed(title="checklist", description=edit)
        await reaction.message.edit(embed=new_embed)


def display_assignment(author, key, message):
    display = discord.Embed(title=key + ' ' + message[0:message.find('%%%')],
                            description=message[(message.find('%%%') + 3):message.find('$$$')])
    display.set_author(name=author.display_name,
                       icon_url=author.avatar_url)
    dd = message[message.find('$$$') + 3: len(message)]
    formatted_due = f'{dd[0:11]} at {dd[12:14]}:{dd[15:17]}'
    display.add_field(name="Due Date: ", value=formatted_due, inline=True)
    return display


client.run(os.getenv('TOKEN'))
