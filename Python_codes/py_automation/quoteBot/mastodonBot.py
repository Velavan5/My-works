import requests
import Quote_pic
#My instance or server
base_url = 'https://mastodon.social'
access_token = 'YwhCMBSOxHD5J0KBqDCbosGH93HipWaPYEUAV1e0Nv8'
link="https://mastodon.social/@velbotmasto"
#function to upload image in mastodon
def upload_media(media_path):
    url = f'{base_url}/api/v1/media'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    files = {
        'file': open(media_path, 'rb')
    }
    try:
        response = requests.post(url, headers=headers, files=files)
    except requests.exceptions.ConnectionError:
        quit("No internet connection. Connect to a network")
    
    if response.status_code==200:
        print("Process 1 complete (image uploaded)")
        return response.json()['id']
    else:
        quit(f"Error uploading media: {response.status_code} - {response.text}")


#for post the image and status -text
def post_status_with_media(status, media_id):
    url = f'{base_url}/api/v1/statuses'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'status': status,
        'media_ids[]': media_id
    }

    response = requests.post(url, headers=headers, data=data)  
    if response.status_code==200:
        print("Process 2 complete (posted successfully)")
        print("To view the post use this : https://mastodon.social/@velbotmasto")
    else:
        quit(f"Error uploading media: {response.status_code} - {response.text}")

#calling
Quote_pic.execute()
img_path="final_img.jpeg"
img_id=upload_media(img_path)
text="Here's your daily dose of motivation! #Motivation #Quotes"
post_status_with_media(text,img_id)
