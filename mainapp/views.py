from django.shortcuts import redirect
from django.views import View
from google.oauth2 import credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendarInitView(View):
    def get(self, request):
        # Step 1: Initialize the OAuth2 flow
        flow = Flow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES, redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/'))

        # Generate the authorization URL and redirect the user to it
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return redirect(authorization_url)



class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Get the authorization code from the request
        authorization_code = request.GET.get('code')

        # Exchange the authorization code for access token
        flow = Flow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES)
        '''redirect_uri=request.build_absolute_uri('/rest/v1/calendar/redirect/')
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri(), code=authorization_code)'''

        flow.redirect_uri = request.build_absolute_uri('/rest/v1/calendar/redirect/')
        flow.fetch_token(authorization_response=request.build_absolute_uri(), code=authorization_code)

        # Create a Google Calendar API service using the credentials
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        # Get a list of events from the user's calendar
        events = service.events().list(calendarId='primary').execute()

        # Process the events as required
        # ...

        return redirect('/')

# Google Calendar API scope
''''SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES)
        auth_url, _ = flow.authorization_url(prompt='consent')
        return Response({'auth_url': auth_url})

class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES)
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        service = build('calendar', 'v3', credentials=credentials)

        # Retrieve list of events from the calendar
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        # Process and return the events
        event_list = []
        for event in events:
            event_list.append(event['summary'])

        return Response({'events': event_list})'''

    






