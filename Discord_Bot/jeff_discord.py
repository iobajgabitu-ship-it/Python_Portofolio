import random
import discord
import requests
import json
import os
from PIL import Image
from io import BytesIO




def get_random_flip():
  flips = ["Sarpemiu.gif", "fu_fuck_you.gif", "fuck-u-kindly.gif", "gorilaflip.gif"]
  return random.choice(flips)


def attach_avatar(base_path, avatar_url, output_path):
  base_img = Image.open(base_path).convert("RGBA")
  response = requests.get(avatar_url)
  avatar = Image.open(BytesIO(response.content)).convert("RGBA")

  avatar = avatar.resize((212, 215))

  new_width = base_img.width + avatar.width
  new_height = max(base_img.height, avatar.height)

  combined = Image.new("RGBA", (new_width, new_height))
  combined.paste(base_img, (0, 0))
  combined.paste(avatar, (base_img.width, 0), avatar)

  combined.save(output_path)

def combine_gifs(base_img_path, base_img2_path, output_path):

  base_img = Image.open(base_img_path).convert("RGBA")
  base_img2 = Image.open(base_img2_path).convert("RGBA")

  new_width = base_img.width + base_img2.width
  new_height = max(base_img.height, base_img2.height)

  combined = Image.new("RGBA", (new_width, new_height))
  combined.paste(base_img, (0,0))
  combined.paste(base_img2, (base_img.width, 0), base_img2)

  combined.save(output_path)





def roll_dice():
  dice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  dice_roll = random.choice(dice)
  return dice_roll



def get_meme():
  response = requests.get('https://meme-api.com/gimme')
  json_data = json.loads(response.text)
  return json_data['url']

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))

  async def on_message(self, message):
    if message.author == self.user:
      return

    elif message.content.startswith('!hello'):
      await message.channel.send('My name is Jeff!')

    elif message.content.startswith('!meme'):
      meme_url = get_meme()
      await message.channel.send('My name is Jeff!')
      await message.channel.send(meme_url)

    elif message.content.startswith('!flip'):
      await message.channel.send('My name is Jeff!')
      
      if message.mention_everyone:

        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        base_img = os.path.join(base_dir, get_random_flip())
        base_img2 = os.path.join(base_dir, 'planet.gif')
        output_img = os.path.join(base_dir, "output.png")
        

        combine_gifs(base_img, base_img2, output_img)

        await message.channel.send(file=discord.File(output_img))

      elif not message.mentions:
        await message.channel.send("Mention a user: `!flip @user`")
        return

      elif message.mentions:
        user = message.mentions[0]
        avatar_url = user.display_avatar.url

        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_img = os.path.join(base_dir, get_random_flip())
        output_img = os.path.join(base_dir, "output.png")

        attach_avatar(base_img, avatar_url, output_img)

        await message.channel.send(file=discord.File(output_img))
    
    elif message.content.startswith('!roll'):
      await message.channel.send('My name is Jeff!')
      await message.channel.send(f'You rolled a {roll_dice()} Jeffs!')
    

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('**************') # Replace with your own token.
