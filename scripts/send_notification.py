import requests
import json
import os
from datetime import datetime

class OneSignalNotifier:
    def __init__(self, app_id, rest_api_key):
        """
        Initialize OneSignal notifier
        
        Args:
            app_id: Your OneSignal App ID
            rest_api_key: Your OneSignal REST API Key
        """
        self.app_id = app_id
        self.rest_api_key = rest_api_key
        self.endpoint = "https://onesignal.com/api/v1/notifications"
        
    def send_notification(self, title, message, url=None, image_url=None, 
                         segments=None, player_ids=None):
        """
        Send a notification via OneSignal
        
        Args:
            title: Notification title
            message: Notification message/body
            url: URL to open when notification is clicked
            image_url: Optional image URL for rich notification
            segments: List of segments to target (e.g., ['All'])
            player_ids: List of specific player IDs to target
            
        Returns:
            Response from OneSignal API
        """
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {self.rest_api_key}"
        }
        
        payload = {
            "app_id": self.app_id,
            "headings": {"en": title},
            "contents": {"en": message}
        }
        
        # Target either segments or specific players
        if segments:
            payload["included_segments"] = segments
        elif player_ids:
            payload["include_player_ids"] = player_ids
        else:
            # Default to all subscribers
            payload["included_segments"] = ["All"]
        
        # Add URL if provided
        if url:
            payload["url"] = url
        
        # Add image if provided
        if image_url:
            payload["big_picture"] = image_url
            payload["large_icon"] = image_url
        
        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None

def send_blog_notification(title, focus_kw, permalink, image_url=None):
    """
    Send a notification for a new blog post
    
    Args:
        blog_title: Title of the blog post
        blog_url: URL of the blog post
        excerpt: Short excerpt or description
        image_url: Featured image URL
    """
    # Get credentials from environment variables
    app_id = os.getenv('ONESIGNAL_APP_ID')
    rest_api_key = os.getenv('ONESIGNAL_REST_API_KEY')
    
    if not app_id or not rest_api_key:
        print("Error: OneSignal credentials not found in environment variables")
        print("Please set ONESIGNAL_APP_ID and ONESIGNAL_REST_API_KEY")
        return None
    
    notifier = OneSignalNotifier(app_id, rest_api_key)
    
    # Prepare notification content
    title = "New Blog Post!"
    message = excerpt if excerpt else blog_title
    
    # Send notification
    result = notifier.send_notification(
        title=title,
        message=message,
        url=blog_url,
        image_url=image_url
    )
    
    if result:
        print(f"✓ Notification sent successfully!")
        print(f"  Recipients: {result.get('recipients', 'N/A')}")
        print(f"  Notification ID: {result.get('id', 'N/A')}")
    else:
        print("✗ Failed to send notification")
    
    return result

if __name__ == "__main__":
    # Example usage
    # You can customize these values or pass them as command line arguments
    
    BLOG_TITLE = "My Awesome Blog Post"
    BLOG_URL = "https://langchain-tutorials.github.io/your-blog-post"
    EXCERPT = "Check out my latest thoughts on web development and design!"
    IMAGE_URL = "https://langchain-tutorials.github.io/images/featured-image.jpg"
    
    # Send the notification
    send_blog_notification(
        blog_title=BLOG_TITLE,
        blog_url=BLOG_URL,
        excerpt=EXCERPT,
        image_url=IMAGE_URL
    )