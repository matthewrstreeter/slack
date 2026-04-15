# Slack-SendMessage.ps1
# This script sends a message to a specified Slack channel using the Slack API.
# V1.0 - 15-Apr-2026 - Initial version

# Prerequisites:
# 1. A Slack App with the 'chat:write', 'chat:write.customize', 'chat:write.public' permission scopes.
# 2. An OAuth token for the Slack App.
# 3. The channel ID or channel name where the message will be posted.

# See my guide for more information about this topic: https://www.matthewrstreeter.com/2026/04/15/send-message-in-slack-using-powershell/

# Function to send a message to Slack
function Send-SlackMessage {
    param (
        [Parameter(Mandatory)][string]$slackToken,
        [Parameter(Mandatory)][string]$channelId,
        [Parameter(Mandatory)][string]$message,
        [string]$iconEmoji = ':robot_face:', # Default emoji
        [string]$customUsername = $null      # Optional custom username
    )

    if (-not $slackToken) {
        throw "Slack token is required."
    }
    if (-not $channelId) {
        throw "Channel ID is required."
    }
    if (-not $message) {
        throw "Message is required."
    }

    # Prepare the headers and body for the request
    $headers = @{
        'Authorization' = "Bearer $slackToken"
        'Content-Type' = 'application/json'
    }
    $body = @{
        'channel' = $channelId
        'text' = $message
        'icon_emoji' = $iconEmoji
    } 
    if ($customUsername) {
        $body['username'] = $customUsername
    }
    $body = $body | ConvertTo-Json -Depth 3

    # Send the POST request to Slack API
    try {
        $response = Invoke-RestMethod -Uri 'https://slack.com/api/chat.postMessage' -Method Post -Headers $headers -Body $body
        if ($response.ok -eq $true) {
            Write-Host 'Message posted successfully!'
        } else {
            Write-Host "Failed to post message. Error: $($response.error)"
            if ($response.error -eq 'channel_not_found') {
                Write-Host "The channel ID may be incorrect or the bot has not been added to the channel."
            } elseif ($response.error -eq 'not_in_channel') {
                Write-Host "Ensure the bot is invited to the channel."
            } else {
                Write-Host "An unknown error occurred."
            }
        }
    } catch {
        Write-Host "An exception occurred: $($_.Exception.Message)"
    }
}

# Load environment variables and functions
$slackApp = 'xoxb-1234567890-0987654321-a1b2c3d4e5f6g7h8i9j0' # Example token, replace with actual token

# Define variables
$slackToken = $slackApp #OAuth Token
$channelId = 'C9999A0B1' #test-channel - #Channel ID or Channel Name
$message = "Test message" #Message text

# Send Slack message
Send-SlackMessage -slackToken $slackToken -channelId $channelId -customUsername "Test App" -message $message -iconEmoji ":sunglasses:" # Replace with actual values
