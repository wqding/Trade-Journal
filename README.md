### To generate a questrade refresh token
1. Login to your questrade account
2. Click on your user name on the top right
3. Click on App hub > REGISTER A PERSONAL APP
4. After saving, press Generate new token

Note: to get an access token, you can make a post request to: https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token=<your refresh token here>

Your refresh token is changed everytime you post to the above link