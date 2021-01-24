## OBJECTIVE
`
Use the Twitter Streaming API to track a given keyword and generate various reports about the tweets.
`

## PRE-REQUISITE
  - Apply for a developer account and receive approval.
  - If you already have a developer account, activate the new developer portal.
  - Create a **Project** and an associated **developer App** in the developer portal.
  - Navigate to your app's `Keys and tokens` page, and save your `API Keys`, `Access Tokens`, and `Bearer Token` to your password manager.
  
## INSTRUCTIONS
  - Get inside the directory `readTweets`.
  - Execute command: `python3 <keyword> <span> <bearer_token> <mode>`<br/>
  `<keyword>`: The keyword you want to search in tweets<br/>
  `<span>`: Time period for which the tweets should be fetched (seconds)<br/>
  `<bearer_token>`: Bearer token generated from your developer account<br/>
  `<mode>`:<br/>
  `0`: Run the flow once with provided credentials<br/>
  `1`: Run the flow continously with same credentials<br/>
  `2`: Run the flow first with span 60s, 120s, 180s and so on
