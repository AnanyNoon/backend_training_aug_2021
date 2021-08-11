import time
import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import Response
from pydantic import ValidationError as ResponseValidationError
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy.exc import DatabaseError
from libfoo import DomainException, Context
from libutil import util
from noonutil.v1 import fastapiutil

logger = logging.getLogger(__name__)

app_params = fastapiutil.get_basic_params('bar', Context.env)
app = FastAPI(**app_params)
app.debug = not Context.is_production
g = fastapiutil.get_request_state_proxy(app)


errhandler_400 = fastapiutil.generate_exception_handler(400)
errhandler_400tb = fastapiutil.generate_exception_handler(400, include_traceback=True)
errhandler_500 = fastapiutil.generate_exception_handler(500, sentry_level='error', client_error_message="Sorry, something wrong on our side")

app.add_exception_handler(RequestValidationError, errhandler_400)
app.add_exception_handler(AssertionError, errhandler_400)
app.add_exception_handler(DomainException, errhandler_400)
app.add_exception_handler(ResponseValidationError, errhandler_500)
app.add_exception_handler(DatabaseError, errhandler_500)
app.add_exception_handler(Exception, errhandler_500)

@app.middleware('http')
def before_request(request: Request, call_next):
    if request.url.path != '/public/hc':
        request.state.customer_code = request.headers.get('x-forwarded-user')
        request.state.host = request.headers.get('host')
        locale = request.headers.get('x-locale') or 'en-ae'
        locale = locale.lower()
        language, country = locale.split('-')[:2] if '-' in locale else (locale, locale)
        request.state.country = country if country in ('ae', 'sa', 'eg') else 'ae'
        request.state.lang = language if language in ('en', 'ar') else 'en'
        request.state.params = {'lang': request.state.lang, 'country': request.state.country}
        request.state.mp_code = (request.headers.get('x-mp') or 'noon').lower()
    return call_next(request)


@app.get("/public/hc", status_code=200, tags=['system'])
def health_check():
    return "OK"

from appfoo.views import router
app.include_router(router)
app = SentryAsgiMiddleware(app)

