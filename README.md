# libmainswerk
Python librariy to fetch data from Frankfurt's student services "MainSWerk"

## Mensa
This class fetches the food available at MainSWerk's cantines. Creating an
object of said class initiates the download, you can also supply an URL
(`Mensa(url="http://foo.bar/foobar")`). Available functions are `get_week()`,
`get_day()` and `get_today()`.
