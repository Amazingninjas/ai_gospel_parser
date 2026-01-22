
import json
from agents.slides_agent import SlidesAgent

def main():
    # 1. Read the JSON presentation
    with open('/home/justin/ai-projects/ai_gospel_parser/ai_presentation_builder/gospel_parser_presentation.json', 'r') as f:
        presentation_data = json.load(f)

    # 2. Initialize the SlidesAgent
    # This assumes 'token.pickle' and 'credentials.json' are in the same directory.
    # You might need to adjust paths if they are located elsewhere.
    slides_agent = SlidesAgent(token_path='token.pickle', credentials_path='credentials.json')

    # 3. Create a Google Slides presentation from the JSON data
    presentation_title = presentation_data.get('metadata', {}).get('title', 'AI Gospel Parser Presentation')
    presentation_id = slides_agent.create_presentation(presentation_title)

    # 4. For each slide in the JSON, create a corresponding Google Slide
    for slide_data in presentation_data.get('slides', []):
        title = slide_data.get('title')
        bullet_points = slide_data.get('content')
        if title:
            slides_agent.add_slide(presentation_id, title, bullet_points)

    # 6. Print the shareable Google Slides link
    presentation_url = slides_agent.get_presentation_url(presentation_id)
    print(f"Presentation created successfully!")
    print(f"Shareable link: {presentation_url}")

if __name__ == '__main__':
    main()
