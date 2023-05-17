from typing import Dict
from starlette.requests import Request
from app.common.constants import templates
from app.user.auth import decode_access_token, get_token


async def render_template(
        request: Request,
        page_vars: Dict[str, ...] | None = None,
):
    token = get_token(request)
    auth: bool = False if token == "None" else True
    current_user_data = decode_access_token(token) if auth else ""
    context = {
        "request": request,
        "auth": auth,
        "current_user": current_user_data,
    }
    if page_vars: context.update(page_vars)

    return templates.TemplateResponse(
        name="base.html",
        context=context,
    )
