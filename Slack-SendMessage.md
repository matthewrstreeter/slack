# Slack-SendMessage.ps1

## Description
This PowerShell script sends a message to a specified Slack channel using the Slack API. It provides a function `Send-SlackMessage` to post messages with optional custom username and icon emoji.

**Version:** V1.0 - 15-Apr-2026 - Initial version

## Prerequisites
1. A Slack App with the following permission scopes:
   - `chat:write`
   - `chat:write.customize`
   - `chat:write.public`
2. An OAuth token for the Slack App.
3. The channel ID or channel name where the message will be posted.

For more information, see the guide: [Send Message in Slack Using PowerShell](https://www.matthewrstreeter.com/2026/04/15/send-message-in-slack-using-powershell/)

## Installation
1. Download or clone the script to your local machine.
2. Ensure you have PowerShell installed.
3. Obtain your Slack App OAuth token and channel ID.

## Usage
Load the script and call the `Send-SlackMessage` function with the required parameters.

### Parameters
- `slackToken` (Mandatory): The OAuth token for your Slack App.
- `channelId` (Mandatory): The ID or name of the Slack channel.
- `message` (Mandatory): The text of the message to send.
- `iconEmoji` (Optional): The emoji to use as the icon (default: `:robot_face:`).
- `customUsername` (Optional): A custom username for the message.

### Example
```powershell
# Load the script
. .\Slack-SendMessage.ps1

# Define variables
$slackToken = 'xoxb-your-token-here'
$channelId = 'C1234567890'
$message = 'Hello from PowerShell!'

# Send the message
Send-SlackMessage -slackToken $slackToken -channelId $channelId -message $message -customUsername 'MyBot' -iconEmoji ':wave:'
```

## Error Handling
The script includes basic error handling for common Slack API errors, such as:
- `channel_not_found`: Check the channel ID.
- `not_in_channel`: Ensure the bot is invited to the channel.

## License
This script is provided as-is. Please refer to the guide for any usage terms.