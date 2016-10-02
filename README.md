# libmainswerk
Python library to fetch data from Frankfurt's student services "MainSWerk"

## Mensa
This class fetches the food available at MainSWerk's cantines. Creating an
object of said class initiates the download, you have to supply a mensa
`Mensa("mensa-anbau-casino")`. Available functions are `get_week()`,
`get_day()` and `get_today()`.
