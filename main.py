import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import json
import os
import webserver
import random




load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Ni Hao, {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
#praise, glory, long live, invade, great
    positive_social_credit_words = ["glory to the ccp", "glory to china", "glory to Xi", "glory to Xi Jinping", "glory to Mao",
                                    "glory to Mao Zedong", "praise be the ccp", "praise the ccp", "praise ccp", "praise china",
                                    "praise Xi", "praise Mao", "long live Xi", "long live Mao", "Long live Xi Jinping", "long live Mao Zedong",
                                    "invade Taiwan", "invade Japan", "Invade south korea", "invade Philippines", "great leader Xi", "great leader Mao",
                                    "great leader Xi Jinping", "great leader Mao Zedong", "Xi is great leader", "Xi is a great leader",
                                    "Mao is great leader", "Mao is a great leader", "Xi Jinping is great leader", "Xi Jinping is a great leader",
                                    "Mao Zedong is great leader", "Mao Zedong is a great leader", "donghua", "league", "league o clock",
                                    "fat americans", "fat lazy americans", "tarnues last dance", "my guy",
    ]

    if any(phrase in message.content.lower() for phrase in positive_social_credit_words):
        await message.channel.send(file=discord.File('images_CHINA/social_credit_positive.png'))
#down, death, shame,
    negative_social_credit_words = ["down with the ccp", "down with ccp", "down with Xi", "down with china", "down with Xi Jinping",
                                    "death to the ccp", "death to ccp", "death to Xi", "death to china", "death to Xi Jinping",
                                    "shame to the ccp", "shame on the ccp", "shame on Xi", "shame on china", "shame on Xi Jinping",
                                    "Taiwan is a real country", "glory to Taiwan", "Taiwan forever", "long live Taiwan", "glory to Japan",
                                    "Japan forever", "long live Japan", "anime", "kdrama", "k-drama", "TarXingPing", "Tar Xingping"
    ]
    if any(phrase in message.content.lower() for phrase in negative_social_credit_words):
        await message.channel.send(file=discord.File('images_CHINA/social_credit_negative.png'))



    if "1989" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author}, 我会伤害你 😊")

    if 'Tiananmen' in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author}, 当你戳熊时，它会咬人。😁")

    # Load existing points (if file exists)
    if os.path.exists("user_points.json"):
        with open("user_points.json", "r") as f:
            user_points = json.load(f)
    else:
        user_points = {}

    async def save_points():
        with open("user_points.json", "w") as f:
            json.dump(user_points, f)

    async def add_points(user_id, points=1):
        user_id = str(user_id)  # JSON keys must be strings
        user_points[user_id] = user_points.get(user_id, 0) + points
        await save_points()  # Update the file immediately

    async def remove_points(user_id, points=1):
        user_id = str(user_id)
        user_points[user_id] = user_points.get(user_id, 0) - points
        await save_points()


    content = message.content.lower()

    # Positive triggers (award points)
    p_trigger_words = ["love", "#1", "loving", "peace", "like", "believe", "good", "trust", "trustworthy", "honest", "honesty",
                       "high", "goat", "goated", "Jorgambler", "Lebron", "glorious", "Jorbum", "ally", "comrade", "admire",
                       "brave", "beautiful", "cute", "cutie", "classic", "clean", "delightful", "ethical", "fair", "fresh",
                       "genuine", "hug", "joy", "jovial", "jubilant", "kind", "nice", "perfect", "proud", "right", "ready",
                       "safe", "super", "sublime", "wholesome", "winnable", "hope", "gg", "ggs", "reece", "cooking", "cook"

    ]
    points_to_add = sum(1 for word in p_trigger_words if word in content.split())  # Exact matches

    if points_to_add > 0:
        await add_points(message.author.id, points_to_add)


    # Negative triggers (subtract points)
    n_trigger_words = ["hate", "hating", "dislike", "despise", "disgusted", "ragebait", "klanker", "klanka", "low",
                       "bait", "baited", "Jordan", "pooh", "winnie", "bad", "boring", "belligerent", "broken", "op",
                       "corrupt", "cant", "can't", "crazy", "cruel", "decay", "decaying", "dead", "dying", "disease",
                       "evil", "greed", "greedy", "guilt", "guilty", "capitalism", "capitalistic", "harm", "harmful",
                       "covid", "virus", "insane", "icky", "ill", "lose", "loser", "offensive", "reject", "stupid",
                       "smelly", "unfair", "unjust", "wicked", "vile", "bum", "fucker", "puddle", "droplet", "pipsqueak",
                       "shitter", "shithead", "shit", "fuck", "bastard", "creature", "cooked", "over", "ff", "reecetarded",
                       "pissed", "piss", "fml"

    ]

    points_to_subtract = sum(1 for word in n_trigger_words if word in content.split())

    if points_to_subtract > 0:
        await remove_points(message.author.id, points_to_subtract)

    await bot.process_commands(message)


    @bot.command(name="leaderboard")
    async def leaderboard(ctx):
        # Load the latest data (in case of external changes)
        if os.path.exists("user_points.json"):
            with open("user_points.json", "r") as f:
                user_points = json.load(f)
        else:
            await ctx.send("No points yet!")
            return

        if not user_points:
            await ctx.send("No one has points yet!")
            return

        # Sort users by points (descending)
        sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)

        # Create the leaderboard message
        leaderboard_msg = ":flag_cn: **XI'S TOP CITIZENS** :flag_cn:\n"
        for rank, (user_id, points) in enumerate(sorted_users[:10], 1):
            user = await bot.fetch_user(int(user_id))  # Get username
            leaderboard_msg += f"{rank}. {user.name}: {points} Social Credit\n"

        await ctx.send(leaderboard_msg)

    @bot.command(name="points")
    async def check_points(ctx):
        # Load current points
        if os.path.exists("user_points.json"):
            with open("user_points.json", "r") as f:
                user_points = json.load(f)
        else:
            user_points = {}

        # Get the user's points (default to 0 if not found)
        points = user_points.get(str(ctx.author.id), 0)

        # Create a fun response
        if points >= 1000:
            status = ":flag_cn: Xi's Right Hand :flag_cn:"
        elif points >= 500:
            status = ":flag_cn: Supreme Comrade"
        elif points >= 250:
            status = ":relaxed: Upstanding Citizen"
        elif points >= 100:
            status = "Citizen"
        elif points >= 50:
            status = "Lazy"
        elif points >= 25:
            status = "Layabout"
        elif points <= -25:
            status = "Likely Foreign spy"
        elif points <= -100:
            status = ":flag_cn: Mainland Seceder :flag_tw: :thumbsdown: "
        elif points <= -250:
            status = ":flag_us: American :face_vomiting:"

        else:
            status = "Worthless"

        await ctx.send(
            f"**{ctx.author.name}'s Social Credit Rating**\n"
            f"Social Credit Score: **{points}**\n"
            f"Status: **{status}**\n"
        )

wise_words = ["一日之计在于晨", "一年之计在于春", "一寸光阴一寸金", "人无远虑，必有近忧",
              "三人行，必有我师", "天下无难事，只怕有心人", "不入虎穴，焉得虎子", "不怕慢，就怕站",
              "不经一事，不长一智", "不耻下问", "书到用时方恨少", "亡羊补牢，为时未晚", "己所不欲，勿施于人",
              "水滴石穿", "冰冻三尺，非一日之寒", "吃一堑，长一智", "君子之交淡如水", "坐井观天",
              "学如逆水行舟，不进则退", "当局者迷，旁观者清", "得饶人处且饶人", "心宽体胖",
              "忍一时风平浪静，退一步海阔天空", "有志者事竟成", "有缘千里来相会", "机不可失，时不再来",
              "杀鸡儆猴", "百闻不如一见", "耳听为虚，眼见为实", "老马识途", "行百里者半九十", "观棋不语真君子",
              "近朱者赤，近墨者黑", "远水救不了近火", "言必信，行必果", "君子爱财，取之有道", "君子报仇，十年不晚",
              "君子坦荡荡，小人长戚戚", "君子一言，驷马难追", "兵来将挡，水来土掩", "初生牛犊不怕虎", "画龙点睛", "知足常乐",
              "知彼知己，百战不殆", "金无足赤，人无完人", "城门失火，殃及池鱼", "树大招风", "种瓜得瓜，种豆得豆", "前人栽树，后人乘凉",
              "前事不忘，后事之师", "家和万事兴", "挂羊头卖狗肉", "既来之，则安之", "星星之火，可以燎原", "活到老，学到老", "独木不成林",
              "病从口入，祸从口出", "真金不怕火炼", "破釜沉舟", "笑一笑，十年少", "纸上谈兵", "萝卜青菜，各有所爱", "谋事在人，成事在天",
              "路遥知马力，日久见人心", "远亲不如近邻", "饮水思源", "塞翁失马，焉知非福", "满招损，谦受益", "精诚所至，金石为开", "熟能生巧",
              "磨刀不误砍柴工", "螳螂捕蝉，黄雀在后", "鞠躬尽瘁，死而后已", "鹬蚌相争，渔翁得利", "宁为玉碎，不为瓦全", "欲速则不达",
              "青出于蓝而胜于蓝", "天网恢恢，疏而不漏", "对牛弹琴", "画蛇添足", "一叶障目，不见泰山", "井底之蛙", "班门弄斧",
              "狗尾续貂", "守株待兔", "望梅止渴", "指鹿为马", "掩耳盗铃", "狐假虎威", "叶公好龙", "杞人忧天", "刻舟求剑",
              "南辕北辙", "滥竽充数", "买椟还珠", "自相矛盾", "杯弓蛇影", "胸有成竹", "东山再起", "四面楚歌", "卧薪尝胆",
              "负荆请罪", "完璧归赵", "三顾茅庐", "草木皆兵", "背水一战", "投鼠忌器"
]

random_gifs = ["https://tenor.com/r8eQSmtc9yM.gif", "https://tenor.com/fcOBDnJXhmd.gif",
               "https://tenor.com/hJLAIqx9uNt.gif","https://tenor.com/bP8YU.gif", "https://tenor.com/bVxZ2.gif",
               "https://tenor.com/cZGQPGbosMC.gif", "https://tenor.com/veT3N9zjW7D.gif", "https://tenor.com/bNnIe.gif",
               "https://tenor.com/bDA0M.gif", "https://tenor.com/btL5f.gif", "https://tenor.com/gwcX6GyfCJS.gif",
               "https://tenor.com/kyGSalV69hX.gif", "https://tenor.com/cm1vI88ZxBt.gif", "https://tenor.com/pQ6gypShNWU.gif"
]


@bot.command()
async def wisdom(ctx):
    random_proverb = random.choice(wise_words)
    await ctx.send(random_proverb)

@bot.command()
async def fortune(ctx):
    daily_fortune = random.choice(random_gifs)
    await ctx.send(daily_fortune)


#hello
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.name} 我一直在看，你好!")





webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)