# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#
""" Userbot module for having some fun with people. """

import asyncio
import random
import re
import time

from collections import deque

import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from cowpy import cow

from userbot import CMD_HELP
from userbot.events import register, errors_handler

# ================= CONSTANT =================
METOOSTR = [
    "Me too thanks",
    "Haha yes, me too",
    "Same lol",
    "Me irl",
    "Same here",
    "Haha yes",
    "Me rn",
]

ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
             [
                 " ̍",
                 " ̎",
                 " ̄",
                 " ̅",
                 " ̿",
                 " ̑",
                 " ̆",
                 " ̐",
                 " ͒",
                 " ͗",
                 " ͑",
                 " ̇",
                 " ̈",
                 " ̊",
                 " ͂",
                 " ̓",
                 " ̈́",
                 " ͊",
                 " ͋",
                 " ͌",
                 " ̃",
                 " ̂",
                 " ̌",
                 " ͐",
                 " ́",
                 " ̋",
                 " ̏",
                 " ̽",
                 " ̉",
                 " ͣ",
                 " ͤ",
                 " ͥ",
                 " ͦ",
                 " ͧ",
                 " ͨ",
                 " ͩ",
                 " ͪ",
                 " ͫ",
                 " ͬ",
                 " ͭ",
                 " ͮ",
                 " ͯ",
                 " ̾",
                 " ͛",
                 " ͆",
                 " ̚",
             ],
             [
                 " ̕",
                 " ̛",
                 " ̀",
                 " ́",
                 " ͘",
                 " ̡",
                 " ̢",
                 " ̧",
                 " ̨",
                 " ̴",
                 " ̵",
                 " ̶",
                 " ͜",
                 " ͝",
                 " ͞",
                 " ͟",
                 " ͠",
                 " ͢",
                 " ̸",
                 " ̷",
                 " ͡",
             ]]

EMOJIS = [
    "😂",
    "😂",
    "👌",
    "✌",
    "💞",
    "👍",
    "👌",
    "💯",
    "🎶",
    "👀",
    "😂",
    "👓",
    "👏",
    "👐",
    "🍕",
    "💥",
    "🍴",
    "💦",
    "💦",
    "🍑",
    "🍆",
    "😩",
    "😏",
    "👉👌",
    "👀",
    "👅",
    "😩",
    "🚰",
]

INSULT_STRINGS = [
    "When you were born, your mom thought she just had shit herself.",
    "Even a trained chimp does everything better than you.",
    "You know what is the difference between you and cancer? Cancer evolves.",
    "If you were in a room with Hitler and Stalin and I had a gun, I would shoot you twice.",
    "Your girlfriend could have picked a better man, like Saddam Hussein or an indonesian pimp with lice and bad breath.",
    "If stupidity was taxed, you would be all stamped.",
    "Light travels faster than sound, which explains why you seemed bright until you speak.",
    "Your teeth are like stars, light years away and yellow.",
    "Your face is like a treasure, it needs to be burried very deep.",
    "Why don't you slip into something more comfortable, like a coma?",
    "I will never forget the first time we met, although I am trying.",
    "If you were a bit more intelligent, you would still be stupid.",
    "Not even your IQ test is positive.",
    "I heard you are very kind to animals, so please return that face to the gorilla.",
    "You got your head so far up your ass, you can chew food twice.",
]

UWUS = [
    "(・`ω´・)",
    ";;w;;",
    "owo",
    "UwU",
    ">w<",
    "^w^",
    r"\(^o\) (/o^)/",
    "( ^ _ ^)∠☆",
    "(ô_ô)",
    "~:o",
    ";-;",
    "(*^*)",
    "(>_",
    "(♥_♥)",
    "*(^O^)*",
    "((+_+))",
]

FACEREACTS = [
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    r"¯\_(ツ)_/¯",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
]

RUNSREACTS = [
    "Runs to Thanos..",
    "Runs far, far away from earth..",
    "Running faster than Bolt coz i'mma userbot !!",
    "Runs to Marie..",
    "This Group is too cancerous to deal with.",
    "Cya bois",
    "Kys",
    "I go away",
    "I am just walking off, coz me is too fat.",
    "I Fugged off!",
    "Will run for chocolate.",
    "I run because I really like food.",
    "Running...\nbecause dieting is not an option.",
    "Wicked fast runnah",
    "If you wanna catch me, you got to be fast...\nIf you wanna stay with me, you got to be good...\nBut if you wanna pass me...\nYou've got to be kidding.",
    "Anyone can run a hundred meters, it's the next forty-two thousand and two hundred that count.",
    "Why are all these people following me?",
    "Are the kids still chasing me?",
    "Running a marathon...there's an app for that.",
]

RUNREACTS = [
    "Where do you think you're going?",
    "Huh? what? did they get away?",
    "ZZzzZZzz... Huh? what? oh, just them again, nevermind.",
    "Get back here!",
    "Not so fast...",
    "Look out for the wall!",
    "Don't leave me alone with them!!",
    "You run, you die.",
    "Jokes on you, I'm everywhere",
    "You're gonna regret that...",
    "You could also try /kickme, I hear that's fun.",
    "Go bother someone else, no-one here cares.",
    "You can run, but you can't hide.",
    "Is that all you've got?",
    "I'm behind you...",
    "You've got company!",
    "We can do this the easy way, or the hard way.",
    "You just don't get it, do you?",
    "Yeah, you better run!",
    "Please, remind me how much I care?",
    "I'd run faster if I were you.",
    "That's definitely the droid we're looking for.",
    "May the odds be ever in your favour.",
    "Famous last words.",
    "And they disappeared forever, never to be seen again.",
    "\"Oh, look at me! I'm so cool, I can run from a bot!\" - this person",
    "Yeah yeah, just tap /kickme already.",
    "Here, take this ring and head to Mordor while you're at it.",
    "Legend has it, they're still running...",
    "Unlike Harry Potter, your parents can't protect you from me.",
    "Fear leads to anger. Anger leads to hate. Hate leads to suffering. If you keep running in fear, you might "
    "be the next Vader.",
    "Multiple calculations later, I have decided my interest in your shenanigans is exactly 0.",
    "Legend has it, they're still running.",
    "Keep it up, not sure we want you here anyway.",
    "You're a wiza- Oh. Wait. You're not Harry, keep moving.",
    "NO RUNNING IN THE HALLWAYS!",
    "Hasta la vista, baby.",
    "Who let the dogs out?",
    "It's funny, because no one cares.",
    "Ah, what a waste. I liked that one.",
    "Frankly, my dear, I don't give a damn.",
    "My milkshake brings all the boys to yard... So run faster!",
    "You can't HANDLE the truth!",
    "A long time ago, in a galaxy far far away... Someone would've cared about that. Not anymore though.",
    "Hey, look at them! They're running from the inevitable banhammer... Cute.",
    "Han shot first. So will I.",
    "What are you running after, a white rabbit?",
    "As The Doctor would say... RUN!",
]

HELLOSTR = [
    "Hi !",
    "‘Ello, gov'nor!",
    "What’s crackin’?",
    "‘Sup, homeslice?",
    "Howdy, howdy ,howdy!",
    "Hello, who's there, I'm talking.",
    "You know who this is.",
    "Yo!",
    "Whaddup.",
    "Greetings and salutations!",
    "Hello, sunshine!",
    "Hey, howdy, hi!",
    "What’s kickin’, little chicken?",
    "Peek-a-boo!",
    "Howdy-doody!",
    "Hey there, freshman!",
    "I come in peace!",
    "Ahoy, matey!",
    "Hiya!",
]

SHGS = [
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
]

CRI = [
    "أ‿أ",
    "╥﹏╥",
    "(;﹏;)",
    "(ToT)",
    "(┳Д┳)",
    "(ಥ﹏ಥ)",
    "（；へ：）",
    "(T＿T)",
    "（πーπ）",
    "(Ｔ▽Ｔ)",
    "(⋟﹏⋞)",
    "（ｉДｉ）",
    "(´Д⊂ヽ",
    "(;Д;)",
    "（>﹏<）",
    "(TдT)",
    "(つ﹏⊂)",
    "༼☯﹏☯༽",
    "(ノ﹏ヽ)",
    "(ノAヽ)",
    "(╥_╥)",
    "(T⌓T)",
    "(༎ຶ⌑༎ຶ)",
    "(☍﹏⁰)｡",
    "(ಥ_ʖಥ)",
    "(つд⊂)",
    "(≖͞_≖̥)",
    "(இ﹏இ`｡)",
    "༼ಢ_ಢ༽",
    "༼ ༎ຶ ෴ ༎ຶ༽",
]

SLAP_TEMPLATES = [
    "{hits} {victim} with **{item}**. {emoji}",
    "{hits} {victim} in the face with **{item}**. {emoji}",
    "{hits} {victim} around a bit with **{item}**. {emoji}",
    "{throws} **{item}** at {victim}. {emoji}",
    "grabs **{item}** and {throws} it at {victim}'s face. {emoji}",
    "launches **{item}** in {victim}'s general direction. {emoji}",
    "starts slapping {victim} silly with **{item}**. {emoji}",
    "pins {victim} down and repeatedly {hits} them with **{item}**. {emoji}",
    "grabs up **{item}** and {hits} {victim} with it. {emoji}",
    "ties {victim} to a chair and {throws} **{item}** at them. {emoji}",
]

ITEMS = (
    "a Samsung J5 2017",
    "a Samsung S10+",
    "an iPhone XS MAX",
    "a Note 9",
    "a Note 10+",
    "knox 0x0",
    "OneUI 2.0",
    "OneUI 69.0",
    "TwoUI 1.0",
    "Secure Folder",
    "Samsung Pay",
    "prenormal RMM state",
    "prenormal KG state",
    "a locked bootloader",
    "payment lock",
    "stock rom",
    "good rom",
    "Good Lock apps",
    "Q port",
    "Pie port",
    "8.1 port",
    "Pie port",
    "Pie OTA",
    "Q OTA",
    "LineageOS 16",
    "LineageOS 17",
    "a bugless rom",
    "a kernel",
    "a kernal",
    "a karnal",
    "a karnel",
    "official TWRP",
    "VOLTE",
    "kanged rom",
    "an antikang",
    "audio fix",
    "hwcomposer fix",
    "mic fix",
    "random reboots",
    "bootloops",
    "unfiltered logs",
    "a keylogger",
    "120FPS",
    "a download link",
    "168h uptime",
    "a paypal link",
    "treble support",
    "EVO-X gsi",
    "Q gsi",
    "Q beta",
    "a Rom Control",
    "a hamburger",
    "a cheeseburger",
    "a Big-Mac",
)

THROW = [
    "throws",
    "flings",
    "chucks",
    "hurls",
]

HIT = [
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "spanks",
    "bashes",
]

EMOJI = (
    "\U0001F923",
    "\U0001F602",
    "\U0001F922",
    "\U0001F605",
    "\U0001F606",
    "\U0001F609",
    "\U0001F60E",
    "\U0001F929",
    "\U0001F623",
    "\U0001F973",
    "\U0001F9D0",
    "\U0001F632",
)

# ===========================================


@register(outgoing=True, pattern=r"^.(\w+)say (.*)")
@errors_handler
async def univsaye(cowmsg):
    """ For .cowsay module, userbot wrapper for cow which says things. """
    if not cowmsg.text[0].isalpha() and cowmsg.text[0] not in ("/", "#", "@",
                                                               "!"):
        arg = cowmsg.pattern_match.group(1).lower()
        text = cowmsg.pattern_match.group(2)

        if arg == "cow":
            arg = "default"
        if arg not in cow.COWACTERS:
            return
        cheese = cow.get_cow(arg)
        cheese = cheese()

        await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")


@register(outgoing=True, pattern="^:/$")
@errors_handler
async def kek(keks):
    """ Check yourself ;)"""
    uio = ["/", "\\"]
    for i in range(1, 15):
        time.sleep(0.3)
        await keks.edit(":" + uio[i % 2])


@register(outgoing=True, pattern=r"^.coinflip (.*)")
@errors_handler
async def coin(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if event.fwd_from:
            return
        r = random.randint(1, 100)
        input_str = event.pattern_match.group(1)
        if input_str:
            input_str = input_str.lower()
        if r % 2 == 1:
            if input_str == "heads":
                await event.edit(
                    "The coin landed on: **Heads**.\nYou were correct.")
            elif input_str == "tails":
                await event.edit(
                    "The coin landed on: **Heads**.\nYou weren't correct, try again ..."
                )
            else:
                await event.edit("The coin landed on: **Heads**.")
        elif r % 2 == 0:
            if input_str == "tails":
                await event.edit(
                    "The coin landed on: **Tails**.\nYou were correct.")
            elif input_str == "heads":
                await event.edit(
                    "The coin landed on: **Tails**.\nYou weren't correct, try again ..."
                )
            else:
                await event.edit("The coin landed on: **Tails**.")
        else:
            await event.edit("Gimme another coin, this one fake AF !!")


@register(pattern="^.slap(?: |$)(.*)", outgoing=True)
@errors_handler
async def who(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        """ slaps a user, or get slapped if not a reply. """
        if event.fwd_from:
            return

        replied_user = await get_user(event)
        caption = await slap(replied_user, event)
        message_id_to_reply = event.message.reply_to_msg_id

        if not message_id_to_reply:
            message_id_to_reply = None

        try:
            await event.edit(caption)

        except BaseException:
            await event.edit(
                "`Can't slap this person, need to fetch some sticks and stones !!`"
            )


async def get_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))

        except (TypeError, ValueError):
            await event.edit("`I don't slap aliens, they ugly AF !!`")
            return None

    return replied_user


async def slap(replied_user, event):
    """ Construct a funny slap sentence !! """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    username = replied_user.user.username

    if username:
        slapped = "@{}".format(username)
    else:
        slapped = f"[{first_name}](tg://user?id={user_id})"

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    emoji = random.choice(EMOJI)

    caption = "..." + temp.format(
        victim=slapped, item=item, hits=hit, throws=throw, emoji=emoji)

    return caption


@register(outgoing=True, pattern="^-_-$")
@errors_handler
async def lol(lel):
    """ Ok... """
    okay = "-_-"
    for i in range(10):
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@register(outgoing=True, pattern="^.decide(?: |$)(.*)")
@errors_handler
async def decide(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if event.fwd_from:
            return
        message = event.pattern_match.group(1)
        message_id = None
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        if not message:
            r = requests.get("https://yesno.wtf/api").json()
        else:
            try:
                r = requests.get(
                    f"https://yesno.wtf/api?force={message.lower()}").json()
            except BaseException:
                await event.edit("`Available decisions:` *yes*, *no*, *maybe*")
                return
        await event.client.send_message(event.chat_id,
                                        str(r["answer"]).upper(),
                                        reply_to=message_id,
                                        file=r["image"])
        await event.delete()


@register(outgoing=True, pattern="^;_;$")
@errors_handler
async def fun(e):
    t = ";__;"
    for j in range(10):
        t = t[:-1] + "_;"
        await e.edit(t)


@register(outgoing=True, pattern="^.fp$")
@errors_handler
async def facepalm(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("🤦‍♂")


@register(outgoing=True, pattern="^.cry$")
@errors_handler
async def cry(e):
    """ y u du dis, i cry everytime !! """
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(random.choice(CRI))


@register(outgoing=True, pattern="^.insult$")
@errors_handler
async def insult(e):
    """ I make you cry !! """
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit(random.choice(INSULT_STRINGS))


@register(outgoing=True, pattern="^.cp(?: |$)(.*)")
@errors_handler
async def copypasta(cp_e):
    """ Copypasta the famous meme """
    if not cp_e.text[0].isalpha() and cp_e.text[0] not in ("/", "#", "@", "!"):
        textx = await cp_e.get_reply_message()
        message = cp_e.pattern_match.group(1)

        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await cp_e.edit("`😂🅱️IvE👐sOME👅text👅for✌️Me👌tO👐MAkE👀iT💞funNy!💦`")
            return

        reply_text = random.choice(EMOJIS)
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message).lower()
        for owo in message:
            if owo == " ":
                reply_text += random.choice(EMOJIS)
            elif owo in EMOJIS:
                reply_text += owo
                reply_text += random.choice(EMOJIS)
            elif owo.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += owo.upper()
                else:
                    reply_text += owo.lower()
        reply_text += random.choice(EMOJIS)
        await cp_e.edit(reply_text)


@register(outgoing=True, pattern="^.vapor(?: |$)(.*)")
@errors_handler
async def vapor(vpr):
    """ Vaporize everything! """
    if not vpr.text[0].isalpha() and vpr.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await vpr.get_reply_message()
        message = vpr.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await vpr.edit("`Ｇｉｖｅ ｓｏｍｅ ｔｅｘｔ ｆｏｒ ｖａｐｏｒ！`")
            return

        for charac in message:
            if 0x21 <= ord(charac) <= 0x7F:
                reply_text.append(chr(ord(charac) + 0xFEE0))
            elif ord(charac) == 0x20:
                reply_text.append(chr(0x3000))
            else:
                reply_text.append(charac)

        await vpr.edit("".join(reply_text))


@register(outgoing=True, pattern="^.str(?: |$)(.*)")
@errors_handler
async def stretch(stret):
    """ Stretch it."""
    if not stret.text[0].isalpha() and stret.text[0] not in ("/", "#", "@",
                                                             "!"):
        textx = await stret.get_reply_message()
        message = stret.text
        message = stret.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await stret.edit("`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")
            return

        count = random.randint(3, 10)
        reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])",
                            (r"\1" * count), message)
        await stret.edit(reply_text)


@register(outgoing=True, pattern="^.zal(?: |$)(.*)")
@errors_handler
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    if not zgfy.text[0].isalpha() and zgfy.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await zgfy.get_reply_message()
        message = zgfy.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await zgfy.edit(
                "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
            )
            return

        for charac in message:
            if not charac.isalpha():
                reply_text.append(charac)
                continue

            for _ in range(0, 3):
                randint = random.randint(0, 2)

                if randint == 0:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[0]).strip()
                elif randint == 1:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[1]).strip()
                else:
                    charac = charac.strip() + \
                        random.choice(ZALG_LIST[2]).strip()

            reply_text.append(charac)

        await zgfy.edit("".join(reply_text))


@register(outgoing=True, pattern="^.hi$")
@errors_handler
async def hoi(hello):
    """ Greet everyone! """
    if not hello.text[0].isalpha() and hello.text[0] not in ("/", "#", "@",
                                                             "!"):
        await hello.edit(random.choice(HELLOSTR))


@register(outgoing=True, pattern="^.owo(?: |$)(.*)")
@errors_handler
async def faces(owo):
    """ UwU """
    if not owo.text[0].isalpha() and owo.text[0] not in ("/", "#", "@", "!"):
        textx = await owo.get_reply_message()
        message = owo.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await owo.edit("` UwU no text given! `")
            return

        reply_text = re.sub(r"(r|l)", "w", message)
        reply_text = re.sub(r"(R|L)", "W", reply_text)
        reply_text = re.sub(r"n([aeiou])", r"ny\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(UWUS), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text += " " + random.choice(UWUS)
        await owo.edit(reply_text)


@register(outgoing=True, pattern="^.react$")
@errors_handler
async def react_meme(react):
    """ Make your userbot react to everything. """
    if not react.text[0].isalpha() and react.text[0] not in ("/", "#", "@",
                                                             "!"):
        await react.edit(random.choice(FACEREACTS))


@register(outgoing=True, pattern="^.shg$")
@errors_handler
async def shrugger(shg):
    r""" ¯\_(ツ)_/¯ """
    if not shg.text[0].isalpha() and shg.text[0] not in ("/", "#", "@", "!"):
        await shg.edit(random.choice(SHGS))


@register(outgoing=True, pattern="^.lmr$")
@errors_handler
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if not run.text[0].isalpha() and run.text[0] not in ("/", "#", "@", "!"):
        await run.edit(random.choice(RUNSREACTS))


@register(outgoing=True, pattern="^.run$")
@errors_handler
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if not run.text[0].isalpha() and run.text[0] not in ("/", "#", "@", "!"):
        await run.edit(random.choice(RUNREACTS))

@register(outgoing=True, pattern="^.metoo$")
@errors_handler
async def metoo(hahayes):
    """ Haha yes """
    if not hahayes.text[0].isalpha() and hahayes.text[0] not in ("/", "#", "@",
                                                                 "!"):
        await hahayes.edit(random.choice(METOOSTR))


@register(outgoing=True, pattern="^Oof$")
@errors_handler
async def Oof(e):
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)


@register(outgoing=True, pattern="^.10iq$")
@errors_handler
async def iqless(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        await e.edit("♿")


@register(outgoing=True, pattern="^.moon$")
@errors_handler
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if event.fwd_from:
            return
        deq = deque(list("🌗🌘🌑🌒🌓🌔🌕🌖"))
        try:
            for _ in range(32):
                await asyncio.sleep(0.1)
                await event.edit("".join(deq))
                deq.rotate(1)
        except BaseException:
            return


@register(outgoing=True, pattern="^.clock$")
@errors_handler
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if event.fwd_from:
            return
        deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
        try:
            for _ in range(32):
                await asyncio.sleep(0.1)
                await event.edit("".join(deq))
                deq.rotate(1)
        except BaseException:
            return


@register(outgoing=True, pattern="^.mock(?: |$)(.*)")
@errors_handler
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    if not mock.text[0].isalpha() and mock.text[0] not in ("/", "#", "@", "!"):
        reply_text = list()
        textx = await mock.get_reply_message()
        message = mock.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
            return

        for charac in message:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)

        await mock.edit("".join(reply_text))


@register(outgoing=True, pattern="^.clap(?: |$)(.*)")
@errors_handler
async def claptext(memereview):
    """ Praise people! """
    if not memereview.text[0].isalpha() and memereview.text[0] not in (
            "/", "#", "@", "!"):
        textx = await memereview.get_reply_message()
        message = memereview.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await memereview.edit("`Hah, I don't clap pointlessly!`")
            return
        reply_text = "👏 "
        reply_text += message.replace(" ", " 👏 ")
        reply_text += " 👏"
        await memereview.edit(reply_text)


@register(outgoing=True, pattern="^.bt$")
@errors_handler
async def bluetext(bt_e):
    """ Believe me, you will find this useful. """
    if not bt_e.text[0].isalpha() and bt_e.text[0] not in ("/", "#", "@", "!"):
        if await bt_e.get_reply_message():
            await bt_e.edit(
                "/BLUETEXT /MUST /CLICK.\n"
                "/ARE /YOU /A /STUPID /ANIMAL /WHICH /IS /ATTRACTED /TO /COLOURS ?"
            )


@register(outgoing=True, pattern=r"^.f (.*)")
@errors_handler
async def payf(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        paytext = e.pattern_match.group(1)
        pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
            paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
            paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
            paytext * 2, paytext * 2)
        await e.edit(pay)


@register(outgoing=True, pattern="^.lfy (.*)")
@errors_handler
async def let_me_google_that_for_you(lmgtfy_q):
    if not lmgtfy_q.text[0].isalpha() and lmgtfy_q.text[0] not in ("/", "#",
                                                                   "@", "!"):
        textx = await lmgtfy_q.get_reply_message()
        qry = lmgtfy_q.pattern_match.group(1)
        if qry:
            query = str(qry)
        elif textx:
            query = textx
            query = query.message
        query_encoded = query.replace(" ", "+")
        lfy_url = f"http://lmgtfy.com/?s=g&iie=1&q={query_encoded}"
        payload = {'format': 'json', 'url': lfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        await lmgtfy_q.edit(f"[{query}]({r.json()['shorturl']})")


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
@errors_handler
async def scam(event):
    """ Just a small command to fake chat actions for fun !! """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        options = [
            'typing', 'contact', 'game', 'location', 'voice', 'round', 'video',
            'photo', 'document', 'cancel'
        ]
        input_str = event.pattern_match.group(1)
        args = input_str.split()
        if len(args) is 0:  # Let bot decide action and time
            scam_action = random.choice(options)
            scam_time = random.randint(30, 60)
        elif len(args) is 1:  # User decides time/action
            try:
                scam_action = str(args[0]).lower()
                scam_time = random.randint(30, 60)
            except ValueError:
                scam_action = random.choice(options)
                scam_time = int(args[0])
        elif len(args) is 2:  # User decides both action and time
            scam_action = str(args[0]).lower()
            scam_time = int(args[1])
        else:
            await event.edit("`Invalid Syntax !!`")
            return
        try:
            if (scam_time > 0):
                await event.delete()
                async with event.client.action(event.chat_id, scam_action):
                    await asyncio.sleep(scam_time)
        except BaseException:
            return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
@errors_handler
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    if not typew.text[0].isalpha() and typew.text[0] not in ("/", "#", "@",
                                                             "!"):
        textx = await typew.get_reply_message()
        message = typew.pattern_match.group(1)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await typew.edit("`Give a text to type!`")
            return
        sleep_time = 0.03
        typing_symbol = "█"
        old_text = ""
        await typew.edit(typing_symbol)
        await asyncio.sleep(sleep_time)
        for character in message:
            old_text = old_text + "" + character
            typing_text = old_text + "" + typing_symbol
            await typew.edit(typing_text)
            await asyncio.sleep(sleep_time)
            await typew.edit(old_text)
            await asyncio.sleep(sleep_time)


CMD_HELP.update({
    "memes":
    ".cowsay\
\nUsage: cow which says things.\
\n\n:/\
\nUsage: Check yourself ;)\
\n\n-_-\
\nUsage: Ok...\
\n\n;_;\
\nUsage: Like `-_-` but crying.\
\n\n.cp\
\nUsage: Copypasta the famous meme\
\n\n.vapor\
\nUsage: Vaporize everything!\
\n\n.str\
\nUsage: Stretch it.\
\n\n.10iq\
\nUsage: You retard !!\
\n\n.zal\
\nUsage: Invoke the feeling of chaos.\
\n\nOof\
\nUsage: Ooooof\
\n\n.fp\
\nUsage: Facepalm :P\
\n\n.moon\
\nUsage: kensar moon animation.\
\n\n.clock\
\nUsage: kensar clock animation.\
\n\n.hi\
\nUsage: Greet everyone!\
\n\n.coinflip <heads/tails>\
\nUsage: Flip a coin !!\
\n\n.owo\
\nUsage: UwU\
\n\n.react\
\nUsage: Make your userbot react to everything.\
\n\n.slap\
\nUsage: reply to slap them with random objects !!\
\n\n.cry\
\nUsage: y u du dis, i cri.\
\n\n.shg\
\nUsage: Shrug at it !!\
\n\n.lmr\
\nUsage: Let Me Run, run, RUNNN!\
\n\n.run\
\nUsage: You better start running\
\n\n.metoo\
\nUsage: Haha yes\
\n\n.mock\
\nUsage: Do it and find the real fun.\
\n\n.clap\
\nUsage: Praise people!\
\n\n.f <emoji/character>\
\nUsage: Pay Respects.\
\n\n.bt\
\nUsage: Believe me, you will find this useful.\
\n\n.type\
\nUsage: Just a small command to make your keyboard become a typewriter!\
\n\n.lfy <query>\
\nUsage: Let me Google that for you real quick !!\
\n\n.decide [Optional: (yes, no, maybe)]\
\nUsage: Make a quick decision.\
\n\n.scam <action> <time>\
\n[Available Actions: (typing, contact, game, location, voice, round, video, photo, document, cancel)]\
\nUsage: Create fake chat actions, for fun. (Default action: typing)\
\n\n\nThanks to 🅱️ottom🅱️ext🅱️ot (@NotAMemeBot) for some of these."
})