import requests
from datetime import datetime
from dateutil import parser

# Fetvch Bot's info
def get_bot_info(bot_token):
    url = "https://discord.com/api/v9/users/@me"
    response = requests.get(url, headers={"Authorization": f"Bot {bot_token}"})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch bot info: {response.status_code}, {response.text}")
        return None

# List all channel in the server
def list_channels(server_id, bot_token):
    url = f"https://discord.com/api/v9/guilds/{server_id}/channels"
    response = requests.get(url, headers={"Authorization": f"Bot {bot_token}"})
    
    if response.status_code == 200:
        channels = response.json()
        print("Channels in the server:")
        for channel in channels:
            channel_type = "Text Channel" if channel["type"] == 0 else "Voice Channel" if channel["type"] == 2 else "Unknown Type"
            print(f"- Name: {channel['name']}, ID: {channel['id']}, Type: {channel_type}")
    else:
        print(f"Failed to fetch channels: {response.status_code}, {response.text}")

# Fetch messages from a spesific channel
def get_messages(channel_id):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    response = requests.get(url, headers={"Authorization": f"Bot {bot_token}"})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch messages: {response.status_code}, {response.text}")
        return None

# Main function
if __name__ == "__main__":
    bot_token = input("Enter your Bot Token: ")
    server_id = input("Enter your Server ID: ")
    print("-" * 40)
    bot_info = get_bot_info(bot_token)
    if bot_info:
        print("Bot Information:")
        print(f"ID: {bot_info.get('id')}")
        print(f"Username: {bot_info.get('username')}")
        print(f"Discriminator: {bot_info.get('discriminator')}")
        print(f"Avatar URL: https://cdn.discordapp.com/avatars/{bot_info.get('id')}/{bot_info.get('avatar')}.png")
        print(f"Bot Account: {bot_info.get('bot', False)}")
        print(f"MFA Enabled: {bot_info.get('mfa_enabled', False)}")
        print(f"Locale: {bot_info.get('locale')}")
        print(f"Flags: {bot_info.get('flags')}")
        print(f"Public Flags: {bot_info.get('public_flags')}")
    print("-" * 40)

    list_channels(server_id, bot_token)
    print("-" * 40)
    channel_id = input("Enter channel ID: ")
    messages = get_messages(channel_id, bot_token)
    print("-" * 40)
    if messages:
        messages.reverse()
        for message in messages:
            timestamp_iso = message.get("timestamp", "No Timestamp")
            try:
                timestamp = parser.parse(timestamp_iso)  
                formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")  
            except Exception as e:
                formatted_timestamp = timestamp_iso  

            print(f"[{formatted_timestamp}] {message['author']['username']}: {message['content']}")

            if "attachments" in message and message["attachments"]:
                print("Attachments:")
                for attachment in message["attachments"]:
                    print(f"\tName: {attachment['filename']}\n\tURL: {attachment['url']}")
        
            if "embeds" in message and message["embeds"]:
                print("Embeds:")
                for embed in message["embeds"]:
                    if "title" in embed:
                        print(f"  Title: {embed['title']}")
                    if "description" in embed:
                        print(f"  Description: {embed['description']}")
                    if "url" in embed:
                        print(f"  URL: {embed['url']}")
                    if "image" in embed and "url" in embed["image"]:
                        print(f"  Image URL: {embed['image']['url']}")
                    if "thumbnail" in embed and "url" in embed["thumbnail"]:
                        print(f"  Thumbnail URL: {embed['thumbnail']['url']}")
                    if "fields" in embed:
                        print("  Fields:")
                        for field in embed["fields"]:
                            name = field.get("name", "No Name")
                            value = field.get("value", "No Value")
                            print(f"    {name}: {value}")
            print("-" * 40)  
