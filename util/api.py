import re
import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

YURL = "https://fantasysports.yahooapis.com/fantasy/v2"

TOKEN = "Kh6EVMvJ4QNPu_YlCT9EqfmJCAPdEMi7OTwyDzFrLDnavTUImKlSDgRM4Jxp3237FvYWM_G4gQEp3DKT3hivMHxuarDF4jAcla.DBrwesMqzfByENgTXF33cY2nXP8Z25qsQMNtybJhfJta5sWg4u5lyoUTyf6rlR9BjEN3Tzn1iPpxDk1arQu.X30nk6zYgPUGOploDSZgJs3xE8M.K73W2DeTxYli1VSqRUsZt8TrVAJTRPcZY2Bhtwvd4Fp7VgKhmosZVAPu3tMw1pbMrCfg9g7GIKYvapYMVoQeuSCsUsCX4Y38WyI6LGa_G8DzAC2z9.MNsd7ep302BA0.FSN2.dEuvKxaorRKOqSmldiE0Tw3c_IcovWYNmBKYmWk67BEUsn5w5.eDm7KMCfh64vKmJVyj51.VRcHpfgVq.MbBAGYkEAmEUs9gbosnc_xcmH0qxMgISgOED5xkfgGuz731XwAp0XXtUAHNB3p9cCKzcqFkwr1QjcIuv_5JefjGALP.SB_SxAcKWhNK.O1IlpS38W4Bjsi0FoePqt77YfcSQ.b9cFHzx_EkthtXmdnPboehiWHry6LQWIFocFCjo8_z8V1C43KuLfGbA_b8rFM3al3KduuS26_sqNvETn1AT7Dsbkh__XeCThIaCNxCbjfp16.Wn.KQqQQTO17qyIeRnnIB9iPFZbzldVB5gkiY5P3tBFaKyuz2OeY43VQII1WSyYkVlMTZZgh_F3Ske5UoQpbdJJJuPeRjXEPO1lCp2iW7qCKf7SyqeiFf8aEtJXIo.lhqATboIsT_IQv2gJxypyeHW.G55f.aSKakYo6isOd4l.KHV6yDpqxUuTJA8dMlotQE3Rn4J.c2lDBjFvIAZavbOcjgq_Pkcqf0Ib4VBjTVU5W.yRQfSTmjZx9_JGyr76p9M27Nb8oFGF_yXDtLt3cW5grBP0c.67VYhsLRS8jzGxYdyISzvAb4pVmAbF9tadV6GH4uAvDDAGGGB_YnV7BLLjqCQ0zy2lsuDwXb95oRf_6b6JAibe8P60oh5SPnZj2aS8HOc52hU.G.rUjhK.XGVWMzq5TkZIf.KRRv2yBL.LtatMlR"  # noqa


class APIAttr(object):
    """ A generic class for API Attributes, just holds values """

    def __repr__(self):
        return str(self.__dict__)


def make_request(url, token=TOKEN, league=False, **kwargs):
    if league:
        url = "league/{}/{}".format(league, url)
    resp = requests.get(
        "{}/{}".format(YURL, url),
        headers={"Authorization": "Bearer {}".format(token)}
    )

    # Remove the namespace from the first XML element
    # Yahoo adds this namespace and the xml to json library
    # prefixes it on every json record, which is very annoying
    non_ns_text = re.sub(
        r'<fantasy_content[^>]*>', '<fantasy_content>', resp.text)

    # Return a JSON representation of the XML data returned from Yahoo
    return bf.data(fromstring(non_ns_text))
