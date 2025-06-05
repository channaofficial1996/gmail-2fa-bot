# Gmail 2FA Telegram Bot

This bot allows:
- Reading QR codes from images sent in Telegram
- Extracting the secret key
- Generating current 2FA codes using `/code` command

## Setup

### Railway

1. Create new Railway project
2. Deploy from this GitHub repo
3. Add an environment variable:
   - `BOT_TOKEN=<your_bot_token_here>`
4. Set start command:
   ```
   python main.py
   ```

### Local

```bash
pip install -r requirements.txt
python main.py
```

Make sure ZBar DLL is available on Windows if you use QR code scanning.
