# A.R.I — Artificial Response Intelligence

A desktop AI chatbot built in pure Python with live data



## Features

| Say this | What happens |
|---|---|
| `hi` | Greeting |
| `weather in London` | Live temperature + wind |
| `bitcoin price` | Live price + 24h change |
| `ethereum` | ETH live price |
| `latest news` | 3 space headlines |
| `movie Interstellar` | Rating, cast, plot |
| `tell me a joke` | Developer humour |
| `I'm feeling stressed` | Wellness response |
| `what time is it` | Current time |
| `what's the date` | Current date |



## Stack

- Python 3.10+
- Tkinter — GUI, zero extra dependencies
- Open-Meteo API — weather (free, no key)
- CoinGecko API — crypto (free, no key)
- Spaceflight News API — headlines (free, no key)
- OMDb API — movies (free key)



## Run it

```bash
git clone https://github.com/YOUR_USERNAME/ari-bot.git
cd ari-bot
pip install requests
python ari_bot.py
```



*Built as a portfolio project — A.R.I BOT*