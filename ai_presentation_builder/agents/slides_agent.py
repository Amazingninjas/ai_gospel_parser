
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

class SlidesAgent:
    def __init__(self, token_path='token.pickle', credentials_path='credentials.json'):
        self.creds = self._get_credentials(token_path, credentials_path)
        self.service = build('slides', 'v1', credentials=self.creds)

    def _get_credentials(self, token_path, credentials_path):
        creds = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, ['https://www.googleapis.com/auth/presentations'])
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def create_presentation(self, title):
        body = {'title': title}
        presentation = self.service.presentations().create(body=body).execute()
        return presentation.get('presentationId')

    def add_slide(self, presentation_id, title, bullet_points):
        requests = [
            {
                'createSlide': {
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_BODY'
                    },
                }
            }
        ]
        response = self.service.presentations().batchUpdate(
            presentationId=presentation_id, body={'requests': requests}).execute()
        
        slide_id = response['replies'][0]['createSlide']['objectId']

        # Get the title and body object IDs
        slide = self.service.presentations().pages().get(presentationId=presentation_id, pageObjectId=slide_id).execute()
        title_id = None
        body_id = None
        for shape in slide.get('pageElements', []):
            if shape.get('shape', {}).get('placeholder', {}).get('type') == 'TITLE':
                title_id = shape['objectId']
            if shape.get('shape', {}).get('placeholder', {}).get('type') == 'BODY':
                body_id = shape['objectId']

        
        requests = [
            # Set background color
            {
                "updatePageProperties": {
                    "objectId": slide_id,
                    "pageProperties": {
                        "pageBackgroundFill": {
                            "solidFill": {
                                "color": {
                                    "rgbColor": {
                                        "red": 0.258,
                                        "green": 0.521,
                                        "blue": 0.956
                                    }
                                }
                            }
                        }
                    },
                    "fields": "pageBackgroundFill"
                }
            }
        ]

        # Add title and bullet points
        if title_id:
            requests.extend([
                {'insertText': {'objectId': title_id, 'text': title, 'insertionIndex': 0}},
                {'updateTextStyle': {
                    'objectId': title_id,
                    'style': {'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}}},
                    'fields': 'foregroundColor'
                }}
            ])

        if body_id:
            requests.extend([
                {'insertText': {'objectId': body_id, 'text': '\n'.join(bullet_points)}},
                {'updateTextStyle': {
                    'objectId': body_id,
                    'style': {'foregroundColor': {'opaqueColor': {'rgbColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}}}},
                    'fields': 'foregroundColor'
                }}
            ])

        if requests:
            self.service.presentations().batchUpdate(
                presentationId=presentation_id, body={'requests': requests}).execute()

    def get_presentation_url(self, presentation_id):
        return f"https://docs.google.com/presentation/d/{presentation_id}/edit"
