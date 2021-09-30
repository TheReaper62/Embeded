import discord
from discord.ext import commands
from discord.app import slash_command

import requests, bs4
def Alchemy_GetRecipe(query):
    itemurl = f"https://www.gambledude.com/little-alchemy-cheats/{query.lower().replace(' ','-')}.html"
    response = requests.get(itemurl,headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs4.BeautifulSoup(response.text,features="html.parser")

    x, steps, raw_ingre = 0, [], {"fire":0,"earth":0,"air":0,"water":0}
    while True:
        x += 1
        try:
            raw = soup.findAll("li",{"id":f"step-{x}"})[0].text
            equa = raw.replace(" ","").replace("=","+").split("+")[:2]
            steps.append(f"{x}.\t{raw.title()}")
            for i in equa:
                if i in raw_ingre:
                    raw_ingre[i]+=1
        except IndexError:
            break
    if len(steps) == 0:
        return None,None
    ingredients = f"**Fire**:\t{raw_ingre['fire']}\n**Earth**:\t{raw_ingre['earth']}\n**Air**:\t{raw_ingre['air']}\n**Water**:\t{raw_ingre['water']}"
    return "\n".join(steps),ingredients

class Alchemy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @slash_command(name="alrecipe",description="Get Little Alchemy Recipes")
    async def slashrecipe(self,ctx,query):
        steps,ingredients = Alchemy_GetRecipe(query)
        if steps == None:
            await ctx.respond("Item not found")
            return
        embed=discord.Embed(title=f"Recipe for `{query.title()}`",description=f"**{steps}**",colour=discord.Colour.teal())
        embed.add_field(name="Ingredients",value=ingredients)
        embed.set_author(name = "Little Alchemy Recipes by Embeded")
        embed.set_footer(text="Resources from gambledude.com")
        await ctx.respond(embed=embed)

    @commands.command()
    async def recipe(self,ctx,*, query):
        steps,ingredients = Alchemy_GetRecipe(query)
        if steps == None:
            await ctx.send("Item not found")
            return
        embed=discord.Embed(title=f"Recipe for `{query.title()}`",description=f"**{steps}**",colour=discord.Colour.teal())
        embed.add_field(name="Ingredients",value=ingredients)
        embed.set_author(name = "Little Alchemy Recipes by Embeded")
        embed.set_footer(text="Resources from gambledude.com")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Alchemy(client))
