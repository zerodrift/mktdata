import urllib
import sys
from xml.etree import ElementTree
import datetime
import pandas as pd
from var.utils import Memoize


class PXWeb:
    """
    Initializes the csv downloader for pxweb for molecule.io
    """
    # fields = ('Close', 'Date', 'High', 'Low', 'OI', 'Open', 'Volume')
    fields = ['Ticker','Date', 'Close']


    def __init__(self, user='ws@moleculesoftware.com', password='Sb63Bx'):
        self.user = user
        self.password = password

    @Memoize
    def fetch(self, ticker):
        try:
            query = 'GetDailyHistory?UserID=%s&Password=%s&Type=F&Symbol=%s' % (self.user, self.password, ticker)
            url = 'http://pxweb.dtn.com/PXWebSvc/PXServiceWeb.svc'

            # Build and send the request
            request = '%s/%s' % (url, urllib.quote(query, '?&='))
            web = urllib.urlopen(request)
            response = web.read()

            # Convert string to XML tree and check for errors
            xml = ElementTree.fromstring(response)
            prices = []
            dates = []
            # For each <History> node returned
            for hNode in xml:
                # For each <Day> in the <History> node write a CSV line
                for dNode in hNode:
                    dates.append(datetime.datetime.strptime(dNode.attrib['Date'], '%Y-%m-%d'))
                    prices.append(float(dNode.attrib['Close']))

            return pd.Series(prices, dates)


        except Exception as e:
            raise RuntimeError("Couldn't get %s because: %s" % (ticker, str(e)))


######
def main(argv):
    p = PXWeb()
    p.fetch('NGF15')


if __name__ == "__main__":
    main(sys.argv)


