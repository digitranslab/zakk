import pytest

from onyx.auth.email_utils import build_user_email_invite
from onyx.auth.email_utils import send_email
from onyx.configs.constants import AuthType
from onyx.configs.constants import ZAKK_DEFAULT_APPLICATION_NAME
from onyx.db.engine.sql_engine import SqlEngine
from onyx.server.runtime.zakk_runtime import ZakkRuntime


@pytest.mark.skip(
    reason="This sends real emails, so only run when you really want to test this!"
)
def test_send_user_email_invite() -> None:
    SqlEngine.init_engine(pool_size=20, max_overflow=5)

    application_name = ZAKK_DEFAULT_APPLICATION_NAME

    zakk_file = ZakkRuntime.get_emailable_logo()

    subject = f"Invitation to Join {application_name} Organization"

    FROM_EMAIL = "noreply@digi-trans.org"
    TO_EMAIL = "support@digi-trans.org"
    text_content, html_content = build_user_email_invite(
        FROM_EMAIL, TO_EMAIL, ZAKK_DEFAULT_APPLICATION_NAME, AuthType.CLOUD
    )

    send_email(
        TO_EMAIL,
        subject,
        html_content,
        text_content,
        mail_from=FROM_EMAIL,
        inline_png=("logo.png", zakk_file.data),
    )
