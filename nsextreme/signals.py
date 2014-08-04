"""

import registration.signals
from hunger.receivers import invitation_code_used
import logging

log = logging.getLogger(__name__)


def user_activated(user, request, **kwargs):
    invitation_code = request.COOKIES.get('invitation_code', '')
    if invitation_code:
        log.info("signalling invitation used for %s, %s" % (user, invitation_code))
        invitation_code_used(None, user, invitation_code)
    else:
        log.info("user activated without invitation")

registration.signals.user_activated.connect(user_activated)

"""