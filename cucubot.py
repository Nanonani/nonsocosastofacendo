import discord
import os
import random
from discord.ext import commands
TOK = "" #add discord bot token

client = commands.Bot(command_prefix = '$')

cartenapoletane = list(range(1,40))


giocatori = []
client.ongoing = False
@client.command()
async def partecipa(ctx):
    if client.ongoing:
        await ctx.send('non puoi partecipare durante una partita')
        return
    giocatori.append(ctx.author)
    await ctx.send(f'{ctx.author} sei entrato')


@client.command()
async def cucu(ctx): 
    if(len(giocatori)== 0):
        await ctx.send('non ci sono giocatori')
        return
    if(client.ongoing):
        await ctx.send('non puoi iniziare una partita duarante un altra')
        return
    client.ongoing = True
    
    await ctx.send('stiamo giocando a cucu')
    random.shuffle(cartenapoletane)

    random.shuffle(giocatori)
    for i in range(len(giocatori)): 
        if(cartenapoletane[i]%10 + 1 == 10):
            await ctx.send(f'{giocatori[i].mention} ha fatto cucù!')
        await giocatori[i].send(f'{giocatori[i]} la tua carta è {cartenapoletane[i]%10 + 1}')
    for i in range(len(giocatori) - 1):
        if(cartenapoletane[i+1] % 10 + 1 == 10 or cartenapoletane[i] % 10 + 1 == 10):
            continue
        await ctx.send(f'{giocatori[i].mention} come stai? (bene o scambia)')

        def check(m):
            if(m.content == 'bene' or m.content == 'scambia') and (m.author == giocatori[i]):
                return True
        msg = await client.wait_for("message", check=check)
        
        if(msg.content == 'scambia'):
            swap = cartenapoletane[i]
            cartenapoletane[i] = cartenapoletane[i+1]
            cartenapoletane[i+1] = swap
            await giocatori[i].send(f'{giocatori[i]} la tua carta è ora {cartenapoletane[i]%10 + 1}')
            await giocatori[i+1].send(f'{giocatori[i+1]} la tua carta è ora {cartenapoletane[i+1]%10 + 1}')
    if(cartenapoletane[len(giocatori)-1]%10 + 1 != 10):
        await ctx.send(f'{giocatori[len(giocatori)-1].mention} vuoi buttarti? (si o no)')
        def check(m):
            if(m.content == 'si' or m.content == 'no') and (m.author == giocatori[len(giocatori)-1]):
                return True
        msg = await client.wait_for("message", check=check)
        if(msg.content == "si"):
            swap = cartenapoletane[len(giocatori)-1]
            cartenapoletane[len(giocatori)-1] = cartenapoletane[len(giocatori)]
            cartenapoletane[len(giocatori)] = swap
            await ctx.send(f'hai pescato: {cartenapoletane[len(giocatori)-1] % 10 + 1}')
    perdenti = []
    mn = 11
    for i in range(len(giocatori)):
        if(cartenapoletane[i]%10 + 1 < mn):
            mn = cartenapoletane[i] % 10 + 1
    for i in range(len(giocatori)):
        if(cartenapoletane[i]%10 + 1 == mn):
            perdenti.append(giocatori[i])
            
    await ctx.send(f'i perdenti hanno fatto {mn} e sono: ')
    
    for i in perdenti:
        await ctx.send(i.mention)
    giocatori.clear()
    await ctx.send('la partita di cucu è finita')
    client.ongoing = False


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


    

client.run(TOK)

    