from yahoofantasy import logger
import requests

YURL = "https://fantasysports.yahooapis.com/fantasy/v2"
TOKEN = "wX8SGPaZtV9te.OpyMOxy_Np2VtNQAlz3oSlfzsNH6KziRyfgoMKi0KBrihXuXJhngjr05561bMFqeoFFJVXj4o1Cwk4jBe1H_Ul6P0HrFJUkuK5i2u4KXSn9.g16JjANMuxd47nMveTsxFvGqJ6JD.ZPQ0hz6c5jnRLCWtwd3LGOZJhVmcqnOpfMOnASfL8gaHOfbuRV0ESVT8qodVdRzSpEzDfTcWUdLlt1J1WbU9MqHq6iZ6F5FTM9errZV7i4DN0KqT_r73gdkChv5G3gduHPVuog80sGHTPmeCsbijPazJTtpI2YfSMWhxxwToAz4DeMJIqkpaWIJ2Dduj0.ahvBFsVIw_x4v_g7yDHF2Xzd4vU0DwHFhI8.SilHS.oEEN14j189__cZGM.uA2MfeqLHSM844lQz0tcUNFlkJSVScOXH_FkCbEr02ZCUzQggJSjG6d9z0VeGH29pQ9EcQPVMbiwUPzK.QMUofMmES.fFvqHz8l2qpDe.OMTd28rliWyEE5qJN2oSoojCx.di6h.vxddgN_SHSkhoW0M3ErxaIpOncmol93ajysCS7zYIItWc2qu3o3FCeZsOMqMU.5gm3B5_6jvTnAYWgtdjh55GOd1RhCb4bFb5Rdw1ZjE6fbzsSn.r38R8RsPgr6eEZfz2iK7QCskeJa3XEaiol_fcuAa1UBMdUfKzUsr_fGWAJR3nlN.oi3Fc5tFuPB_lzDHIwXWoXIRPqgzpP95hfyNmU7MYyeAjJQ_wZVr4QjC_mmoBW4a4Q_yTxWHRWk9vArC7vUCWyM2JOBC7ATBIVUspt5mT2bQaiUubLVG090tJylUIYUwPCb3SkxTlE.Ym5twQAGaBaFdGglabDmMcyHlXi0V1AOxJsK32Y6g_0C4U.lQh5pnRy0nRc_e63EU8RDV6w08XcfYXNvTNgVWEm.VMYSF5EyTKwPvqvGsbsCFNH29yeAW4QHnuEerPs2akM2K3v.SInADYL5q_BXIAW9aYDBM445TXw7PJD1DLgb7KspDbisGOn3JlV3uSjcavJycBnRu7uf9CNZQomsu4gqGNMQKA5nvqt6l.95n"  # noqa


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
