import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment
genai_api_key = os.getenv('GEMINI_API_KEY')
if not genai_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure the Generative AI API
genai.configure(api_key=genai_api_key)

class AloneGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat = ""
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.api_call_count = 0
        self.api_call_limit = 10  # Example limit, adjust as necessary
        self.rate_limit_delay = 60  # Delay in seconds

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.lower() == "hello":
            await message.channel.send(f"Nice to meet you, {message.author.mention}!")

        await self.bot.process_commands(message)

        # Check if the bot is mentioned before updating chat history and making API calls
        if self.bot.user in message.mentions:
            self.chat += f"{message.author}: {message.content}\n"
            try:
                response = await self.generate_response(self.chat)
                if response:
                    await message.channel.send(response)
                else:
                    await message.channel.send("I'm having trouble generating a response right now. Please try again later.")
            except Exception as e:
                print(f"Error in on_message: {e}")
                self.chat = ""

    async def generate_response(self, chat_history):
        if self.api_call_count >= self.api_call_limit:
            return "Sorry, I've reached my API call limit for now. Please try again later."

        try:
            prompt = ('You are an anime character Serena from Pokemon. '
                      'Use her character and reply to the user queries in the chat as if you are her. ' + chat_history)

            response = await asyncio.to_thread(self.model.generate_content,
                                               prompt,
                                               generation_config=genai.GenerationConfig(
                                                   max_output_tokens=10000,
                                                   temperature=0.5,
                                               ))
            self.api_call_count += 1
            print(f"API Call Count: {self.api_call_count}")

            # Reset API call count after rate limit delay
            if self.api_call_count >= self.api_call_limit:
                print("Rate limit reached. Waiting for reset...")
                await asyncio.sleep(self.rate_limit_delay)
                self.api_call_count = 0

            # Extract the generated text from the response
            return response.text if response.text else "I couldn't generate a response."
        except Exception as e:
            print(f"Error generating response: {e}")
            return "There was an error generating a response."

async def setup(bot):
    await bot.add_cog(AloneGPT(bot))

# Main bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def main():
    await setup(bot)
    await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
