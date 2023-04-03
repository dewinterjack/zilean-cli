import os
from flask import Flask, request, jsonify
from discord.ext import commands
import disc
import threading
import asyncio
app = Flask(__name__)

# Replace 'your-bot-token' with your Discord bot's token



# Endpoint to send a message to a specific channel
@app.route('/ask', methods=['POST'])
def send_message():
    data = request.get_json()

    if data["text"]:
        print(data["text"])
        asyncio.run_coroutine_threadsafe(disc.ask_api(data["text"]), disc.client.loop)
        return jsonify({'status': 'ok'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
    



def run_bot():
    disc.client.run('<token>')

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(debug=True, use_reloader=False)