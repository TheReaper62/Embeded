import discord
from discord.ext import commands
from discord.app import slash_command




import requests, json, datetime
from . import functionals

HEADERS  = {'AccountKey' : 'bmjTowwfQlucvxQpeJePDg==','accept' : 'application/json'}
BASE = "http://datamall2.mytransport.sg/ltaodataservice"

class AllStops:
    def __init__(self):
        stops = []
        for skip in range(0,5500,500):
            path = f"http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={skip}"
            r = requests.get(path,headers=HEADERS)
            r = json.loads(r.text)
            stops += r["value"]
        self.STOPS = stops

    def __getitem__(self,key):
        if str(key).startswith("#"):
            key = key[1:]
            if key in [i["BusStopCode"] for i in self.STOPS]:
                index = [i["BusStopCode"] for i in self.STOPS].index(key)
                return self.STOPS[index]
            else:
                return None
        else:
            if str(key).isdigit():
                return self.STOPS[int(key)]
            else:
                return None

    def Subset(self,method):
        if method in ['BusStopCode', 'RoadName', 'Description', 'Latitude', 'Longitude']:
            return [i[method] for i in self.STOPS]
        else:
            return None

    # Return BusStopCode(s) for all Bus Stops that match the given pattern
    def FindByName(self,pattern):
        desc  = self.Subset("Description")
        rdnm = self.Subset("RoadName")
        bscodes = self.Subset("BusStopCode")
        indexes = set.union({desc.index(i) for i in desc if pattern.lower() in i.lower()},{rdnm.index(i) for i in rdnm if pattern.lower() in i.lower()})
        return [bscodes[i] for i in indexes]

class NextBus:
    def __init__(this,**kwargs):

        # Return time in seconds from NOW (or additional seconds from NOW) to estimated
        def get_time_difference(estimated,add_secs=0):
            earlier = datetime.datetime.now().time()
            if add_secs != 0:
                earlier += datetime.timedelta(seconds=add_secs)
            later = datetime.datetime.strptime(estimated, '%Y-%m-%dT%I:%M:%S%z').time()
            diff = datetime.datetime.combine(datetime.date.today(), later) - datetime.datetime.combine(datetime.date.today(), earlier)
            return diff.seconds

        kwargs = functionals.OptionalKwargs(kwargs)
        print(f"\nNextBus Object: {kwargs.dictionary}")
        this.OriginCode = kwargs["OriginCode"]
        this.DestinationCode = kwargs["DestinationCode"]
        this.EstimatedArrival = kwargs["EstimatedArrival"]
        this.Latitude = kwargs["Latitude"]
        this.Longitude = kwargs["Longitude"]
        this.VisitNumber = kwargs["VisitNumber"]
        this.Load = kwargs["Load"]
        this.Feature = kwargs["Feature"]
        this.Type = kwargs["Type"]
        this.TimeTillArrive = get_time_difference(kwargs["EstimatedArrival"])

class NextBusArrival:
    def __init__(self,**kwargs):
        kwargs = functionals.OptionalKwargs(kwargs)
        print(f"\nNextBusArrival Object: {kwargs.dictionary}")
        self.ServiceNo = kwargs["ServiceNo"]
        self.Operator = kwargs["Operator"]
        self.NextBus = NextBus(**kwargs["NextBus"])
        self.NextBus2 = NextBus(**kwargs["NextBus2"])
        self.NextBus3 = NextBus(**kwargs["NextBus3"])


def ActiveStopInfo(BusStopCode, ServiceNo=None):
    path = BASE + f"/BusArrivalv2?BusStopCode={BusStopCode}"
    if ServiceNo != None:
        path += f"&ServiceNo={ServiceNo}"
    r = requests.get(path,headers=HEADERS)
    r = json.loads(r.text)
    return r['Services']


def BusRoutes():
    path = BASE + "/BusRoutes"


# stop = ActiveStopInfo(94051)
# servs = [NextBusArrival(**i).NextBus.TimeTillArrive for i in stop]
# print("\nServs",servs)




class TrafficAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.STOPS = AllStops()

    # @commands.cooldown(1, 10, commands.BucketType.user)
    @slash_command(name="findstop",description="Find Bus Stop by Name")
    async def findbusstop(self,ctx,query):
        response = {i['Description']:f"Stop Code: `{i['BusStopCode']}`\nRoad Name: {i['RoadName']}\n[View Stop](http://www.google.com/maps/place/{i['Latitude']},{i['Longitude']})" for i in [self.STOPS[f"#{i}"] for i in self.STOPS.FindByName(query)]}
        if len(response) == 0:
            await ctx.respond(f"*No Bus Stops with this identifier found...*")
            return
        embed = discord.Embed(
            title = f"{len(response)} Bus Stops Found (Matching '{query}')",
            colour = discord.Colour.green()
        )
        for i in response:
            embed.add_field(name=i,value=response[i])
            if len(embed)>5000:
                break
        await ctx.respond(embed=embed)

    @commands.command()
    async def findstop(self,ctx,*,query):
        response = {i['Description']:f"Stop Code: `{i['BusStopCode']}`\nRoad Name: {i['RoadName']}\n[View Stop](http://www.google.com/maps/place/{i['Latitude']},{i['Longitude']})" for i in [self.STOPS[f"#{i}"] for i in self.STOPS.FindByName(query)]}
        if len(response) == 0:
            await ctx.send(f"*No Bus Stops with this identifier found...*")
            return
        embed = discord.Embed(
            title = f"{len(response)} Bus Stops Found (Matching '{query}')",
            colour = discord.Colour.green()
        )
        for i in response:
            embed.add_field(name=i,value=response[i])
            if len(embed)>5000:
                break
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(TrafficAPI(client))
