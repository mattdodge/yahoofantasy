from yahoo_sdk import logger
import requests

YURL = "https://fantasysports.yahooapis.com/fantasy/v2"
TOKEN = "TzJMQGTJ4QPR1WjxP5hnARlEF6pOCyr84CtL5Am.mnYGGVGhT0fSNI2bgTpKwwzXWjnnPP5hGk0gLOJ7Ryh7HEeP3OVnHLYMOOLgA.FzmAairdt2kRYsV61AnqOgZMtGauofCjnS9uJ5Rnf2Jro_2cVi2fr8_8At_DGqOEF4tfef6Oo9lkCEYASmzB4P3LZr0eLokD_PZNaIyVcu38Zc03Rq2uaWuGF4DZRdZFyXbIDduwoMfYhTUg9lXAihtqft6pMfMjLsFiPhKPhqVL3znqDo1KhLG7.Rp0yPec4p18A.heH.rbmg6L_OVR5jaxhDptWWLc2xXnrVd3DIqL40Vlmg57iKw77wwTQaVmBSm1mk5lLvZx7z1blrjNKgYYkZeeMINV1ppo6s4dQE0qYBizY9fbgom_dGB4bM7ANLbee50G.wjTtuzu7TqP6JYotA9s8FsqYTEx0JcEJza39ak6hG_el5lfLFlWcsqe.YJ_okq1Lq9r.DLuIH1bd1i7a9sQ_T1VEkbh1Ug.XeP_gcKdCqcmJpBFbKX5ndaAuJjEpUKrpf7YYSfb36X_8QDbq2.Q4bHuZMSrHJq1LLXs05sX8aLbXMTX66nEaw_fAiClhgkJKbfagUZZBu.3GG1OSLr0ueeqoqPshJETT.ujT6pXR.kJ20jLjINUQHVgiRpdHeQLakM.jCzpRG6sbtps28v6EpORNcxB6JDmDjUS0OkfecHDouY4vT6ljfPeZuAd4DSxzx.aZvG.dmKLek4FBYhEg0Rg8mYFJil8p3eXdYEBu.yKyaIRGFIOvQEvh30dVjl77uQpftoLLsRdTNp4oY49Zi5M4.kVBZMR_q.Igb0LVDpWkrz3z2meNUKrMpuyeDV48PWlxCeepD2awbyu.EvYwbpILE2UNWdIw_XCAoEJau.jNTy2BwCm1tSL72HaTuLrKQWhATllxzX2IGcXlVog6qmWFZAcEuDsgAkQBdg7ZLZ7HaVtJ7m7zCiwSVvlMHWWWQpvcLAH1U1szRTUuNg9kASKhaGr3cRwOtT_9jpBAj7_BVAhOtA0KHEJTXinB4XWfBur8eJ.wUhGTKZM6iCcUEmX56ED8Z"  # noqa


def make_request(url, token=TOKEN, league=False, **kwargs):
    if league:
        url = "league/{}/{}".format(league, url)
    logger.debug("Making request to {}".format(url))
    resp = requests.get(
        "{}/{}".format(YURL, url),
        headers={"Authorization": "Bearer {}".format(token)}
    )

    try:
        resp.raise_for_status()
    except:
        logger.exception("Bad response status ({}) for request".format(
            resp.status_code))
        raise
    return resp.text
