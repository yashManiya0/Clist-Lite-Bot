import discord
import requests
import time
import json
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import random
from discord.ext import commands
import praw

load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')
CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
REDDIT_USERNAME=os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD=os.getenv('REDDIT_PASSWORD')
OWNER_DISCORD_ID=int((os.getenv('OWNER_DISCORD_ID')).strip())
# print('Username : ',REDDIT_USERNAME)
# print(type(REDDIT_USERNAME))



r = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,username=REDDIT_USERNAME, password=REDDIT_PASSWORD, user_agent='prawxyz')
subr1 = r.subreddit('programmingmemes')
topmemes = subr1.hot(limit=50)
all_memes = []
for i in topmemes:
    all_memes.append([i.title, i.url])

handle_details={}
member_handles={}


bot = commands.Bot(command_prefix=";",owner_id=OWNER_DISCORD_ID)
bot.remove_command('help')


# events events events events events events events events events events events events events events events events
# events events events events events events events events events events events events events events events events
# events events events events events events events events events events events events events events events events

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Recollecting all the Contest Timings'))
    print('Bot is Readyyyyyyyyyy')

@bot.event
async def on_message(msg):
    await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required number of arguments for the command **{ctx.command.name}**. \nFor syntax, type : ;help  <command>")
    elif isinstance(error, commands.CommandOnCooldown):
        if error.retry_after > 3600:
            reaf = '{:.2f}'.format(error.retry_after/3600)
            time = reaf+' hours'
        elif error.retry_after > 60:
            reaf = '{:.2f}'.format(error.retry_after/60)
            time = reaf+' minutes'
        else:
            reaf = '{:.2f}'.format(error.retry_after)
            time = reaf+' seconds'
        await ctx.send("The command **{}** is under cooldown. So please retry after {}.".format(ctx.command.name, time))
    else:
        raise error



# help help help help help help help help help help help help help help help help help help help help help help help help
# help help help help help help help help help help help help help help help help help help help help help help help help
# help help help help help help help help help help help help help help help help help help help help help help help help

@bot.group(invoke_without_command=True)
async def help(ctx,*s):
    if len(s)==0:
        e = discord.Embed(title='Inbuilt Commands for Clist Lite bot',
                        description='For extended info on a command, use :\n;help  <command>', color=discord.Colour.green())
        e.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2015/07/18/13/29/question-850361_960_720.jpg')
        e.add_field(name='Help', value=';help <command>',inline=False)
        e.add_field(name='Clear', value=';clear <number>',inline=False)
        e.add_field(name='Register',value=';register <member_tag> <cf_handle>',inline=False)
        e.add_field(name='User Data', value=';userinfo <member_tag>',inline=False)
        e.add_field(name='Upcoming Contests', value=';clist future',inline=False)
        e.add_field(name='Stalk', value=';stalk <cf_handle>',inline=False)
        e.add_field(name='Memes', value=';meme',inline=False)
        e.set_footer(icon_url=ctx.author.avatar_url,text='Requested by '+ctx.author.name)
        await ctx.send(embed=e)


@help.command()
async def clear(ctx):
    e = discord.Embed(
        title='Clear', description='This command deletes the requested number of messages (incluing the bots\' , by default 2).', color=ctx.author.color)
    e.add_field(name='Syntax', value=';clear <number>')
    e.add_field(name='Command Aliases', value='delete \n clr')
    await ctx.send(embed=e)


@help.command()
async def register(ctx):
    e = discord.Embed(
        title='Register', description='This command registers the member tag with given CF Handle.', color=ctx.author.color)
    e.add_field(name='Syntax', value=';register <member_tag> <cf_handle>')
    e.add_field(name='Command Aliases', value='reg')
    await ctx.send(embed=e)


@help.command()
async def userinfo(ctx):
    e = discord.Embed(
        title='Userinfo', description='This command gives info of the requested member of the server.', color=ctx.author.color)
    e.add_field(name='Syntax', value=';userinfo  <member_tag>')
    e.add_field(name='Command Aliases', value='userdata')
    await ctx.send(embed=e)


@help.command()
async def clist(ctx):
    e = discord.Embed(
        title='Upcoming Contests', description='This command gives you the list of Upcoming Contests on CodeForces and CodeChef. Use "short"/"long" parameters for filtering the contests you want.', color=ctx.author.color)
    e.add_field(name='Syntax', value=';clist future')
    e.add_field(name='Command Aliases', value='clist future short\nclist future long')
    await ctx.send(embed=e)


@help.command()
async def stalk(ctx):
    e = discord.Embed(
        title='Stalk', description='This command gives you a list of recently solved problems by the given person.', color=ctx.author.color)
    e.add_field(name='Syntax', value=';stalk <CF_handle>')
    e.add_field(name='Command Aliases', value='Stalk')
    await ctx.send(embed=e)


@help.command()
async def meme(ctx):
    e = discord.Embed(
        title='Meme', description='This command generates random Programming related memes from Reddit.', color=ctx.author.color)
    e.add_field(name='Syntax', value=';meme')
    e.add_field(name='Command Aliases', value='memes')
    await ctx.send(embed=e)



# commands commands commands commands commands commands commands commands commands commands commands commands commands commands
# commands commands commands commands commands commands commands commands commands commands commands commands commands commands
# commands commands commands commands commands commands commands commands commands commands commands commands commands commands

@bot.command(aliases=['delete', 'clr', 'Clear'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, n=2):
    await ctx.channel.purge(limit=n)


@bot.command(aliases=['reg','Register'])
async def register(ctx,member:discord.Member,handle):

    def to_days(secs):
        hrs=int(secs//3600)
        if hrs<24:
            return str(hrs)+' hours'
        return str(hrs//24)+' days'

    curr_time=time.time()
    url='https://codeforces.com/api/user.info?handles='+handle
    req=requests.get(url).text
    raw_data=json.loads(req)

    if raw_data['status']!='OK':
        await ctx.send('Some error occurred.\n'+raw_data['comment'])

    else:
        colours={'unrated':discord.Color.light_grey(),'newbie':discord.Color.dark_gray(),'pupil':discord.Color.dark_green(),'specialist':discord.Color.from_rgb(80, 184, 184),'expert':discord.Color.from_rgb(0, 0, 184),'candidate master':discord.Color.purple(),'master':discord.Color.orange(),'international master':discord.Color.dark_orange(),'grandmaster':discord.Color.red(),'international grandmaster':discord.Color.red(),'legendary grandmaster':discord.Color.dark_red()}
        result=raw_data['result']
        for user_data in result:
            d={}
            curr_handle=user_data['handle']
            d['last_seen']=to_days(curr_time-user_data['lastOnlineTimeSeconds'])
            d['first_name']='Not Found'
            d['last_name']='Not Found'
            if 'firstName' in user_data:
                d['first_name']=user_data['firstName']
            if 'lastName' in user_data:
                d['last_name']=user_data['lastName']
            d['avatar']=user_data['avatar']
            d['rank']=user_data['rank'].title()
            d['max_rank']=user_data['maxRank'].title()
            d['rating']=str(user_data['rating'])
            d['max_rating']=str(user_data['maxRating'])
            d['friend_of']=str(user_data['friendOfCount'])
            d['color']=colours[user_data['rank']]
            handle_details[curr_handle]=d
        member_handles[member.id]=handle
        await ctx.send(handle+' successfully set for '+member.display_name)


@bot.command(aliases=['whois', 'userdata', 'Userinfo'])
async def userinfo(ctx, mem: discord.Member):
    if mem.id not in member_handles.keys():
        await ctx.send('Please register the Member tag with his/her CF handle, before using this command')
    else:
        handle=member_handles[mem.id]
        member_details=handle_details[handle]
        member_name=member_details['first_name']+' '+member_details['last_name']
        if 'Not Found' in member_name:
            member_name=handle
        e=discord.Embed(title=member_name,description=handle+' AKA '+mem.display_name,color=member_details['color'])
        e.set_thumbnail(url=member_details['avatar'])
        e.add_field(name='Current Rating',value=member_details['rating']+' - '+member_details['rank'],inline=True)
        e.add_field(name='Maximum Rating',value=member_details['max_rating']+' - '+member_details['max_rank'],inline=True)
        e.add_field(name='Last Seen',value=member_details['last_seen'],inline=False)
        e.add_field(name='Friend of '+member_details['friend_of']+' users',value='‎')
        e.set_footer(icon_url=ctx.author.avatar_url,text='Requested by '+ctx.author.name)
        await ctx.send(embed=e)


@bot.command(aliases=['Meme', 'memes', 'Memes'])
async def meme(ctx):
    rmeme = random.choice(all_memes)
    e = discord.Embed(description=rmeme[0], color=discord.Colour.green())
    e.set_image(url=rmeme[1])
    e.set_footer(icon_url=ctx.author.avatar_url,
                 text='Requested by '+ctx.author.name)
    await ctx.send(embed=e)


@bot.command()
async def clist(ctx,*args):
    t0=time.time()
    def to_hrs(time):
        time=time.split()[0]
        hrs_left=0
        if ':' in time:
            hrs,mins,*secs=map(int,time.split(':'))
            hrs_left=hrs+mins/60
        else:
            hrs_left=int(time)*24
        return hrs_left
    
    def make_embed(contests,param):
        e=discord.Embed(title=(param+"Contests").upper(),description='All the upcoming/running '+param+'Contests are :',color=discord.Color.blue())
        for contest in contests:
            nam=f'[{contest[1][3]}]({contest[1][4]})'
            e.add_field(name="‎",value=f'**{nam}**\nStarting Time : {contest[1][0]}\nDuration : {contest[1][1]}\nTime Left : {contest[1][2]}\n')
        e.set_footer(icon_url=ctx.author.avatar_url,text="Requested by "+ctx.author.name)
        return e

    req=requests.get('https://clist.by/').text

    soup=BeautifulSoup(req,'html.parser')
    rows=soup.select('#contests > div')
    contest_details=[]

    for row in rows:

        divs=row.select('div')
        details=[" " for i in range(5)]

        if 'codeforces' in str(divs[-1].text).strip().lower() or 'codechef' in str(divs[-1].text).strip().lower():

            div2=divs[-1].parent
            title_anchor=div2.select('a.title_search')[0]
            title=title_anchor.text
            link=title_anchor['href']

            raw_date=str(divs[1].text).split()
            hr,min=map(int,raw_date[-1].split(':'))
            hr=(hr+5)%24
            if min+30>=60:
                hr=(hr+1)%24
            min=(min+30)%60
            raw_date[-1]=('0'+str(hr))[-2:]+":"+('0'+str(min))[-2:]

            details[0]=" ".join(raw_date)               # 0 starting-time  [date.month day hr:min]
            details[1]=str(divs[2].text).strip()        # 1 duration
            details[2]=str(divs[3].text).strip()        # 2 time-left
            details[3]=title                            # 3 contest-title
            details[4]=link                             # 4 contest-link

            contest_details.append([to_hrs(details[2]),details])

    contest_details.sort()
    short_contests=[]
    long_contests=[]
    for contest in contest_details:
        duration=contest[1][1]
        if to_hrs(duration)>=24:
            long_contests.append(contest)
        else:
            short_contests.append(contest)
    if len(args)==0:
        await ctx.send('Please write the command correctly. It should be either of the following:\n```;clist future\n;clist future short\n;clist future long```')
    else:
        if len(args)==1:
            e=make_embed(contest_details,'')
            await ctx.send(embed=e)
        else:
            if args[-1].lower()=='short':
                e=make_embed(short_contests,'Short ')
            elif args[-1].lower()=='long':
                e=make_embed(long_contests,'Long ')
            await ctx.send(embed=e)
    print(time.time()-t0)


@bot.command(aliases=['Stalk'])
async def stalk(ctx,handle):
    t0=time.time()    
    url='https://codeforces.com/api/user.status?handle='+handle+'&from=1&count=50'
    req=requests.get(url,'html.parser').text
    raw_data=json.loads(req)

    if raw_data['status']!='OK':
        await ctx.send('Some error occurred\n'+raw_data['comment'])
    else:
        def to_days(secs):
            hrs=int(secs//3600)
            if hrs<24:
                return str(hrs)+' hours'
            return str(hrs//24)+' days'
        result=raw_data['result']
        curr_time_secs=int(time.time())
        ctr=0
        colour=discord.Color.blurple()
        if handle in handle_details.keys():
            colour=handle_details[handle]['color']
        e=discord.Embed(title='Stalk is ON',description='Recently solved problems by **'+handle+'**',color=colour)
        for sub in result:
            if ctr>9:
                break
            if sub['verdict']=='OK':
                data=["[?]" for i in range(5)]
                data[0]=to_days(curr_time_secs-sub['creationTimeSeconds'])
                data[3]=sub['problem']['tags']
                data[2]=sub['problem']['index']+'. '+sub['problem']['name']
                sub_prob_keys=sub['problem'].keys()
                if 'rating' in sub_prob_keys:
                    data[4]=str(sub['problem']['rating'])
                    data[1]='https://codeforces.com/problemset/problem/'+str(sub['contestId'])+'/'+sub['problem']['index']
                else:
                    data[1]='https://codeforces.com/contest/'+str(sub['contestId'])+'/problem/'+sub['problem']['index']
                ctr+=1
                e.add_field(name='‎',value=f'**[{data[2]}]({data[1]})** : {data[4]}\nBefore {data[0]}\nTags : '+', '.join(data[3]),inline=False)
        e.set_footer(icon_url=ctx.author.avatar_url,text="Requested by "+ctx.author.name)
        await ctx.send(embed=e)
        t1=time.time()
        print(t1-t0)

@bot.command(aliases=['test'])
async def test_command(ctx,cmd):
    print('testing cmd ran')

bot.run(BOT_TOKEN)
