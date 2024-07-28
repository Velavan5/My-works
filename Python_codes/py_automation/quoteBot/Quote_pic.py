import uuid
import requests
from io import BytesIO
from PIL import Image
from random import randint
import cloudinary
import cloudinary.uploader
import cloudinary.api

#config the api of cloudinary ,I think making it a global is  a good practice
cloudinary.config( 
cloud_name='dnadeynjn',
api_key="sorry-cann't give you",
api_secret='generate-yours'
)


#This fun uses the forismatic api to get the quote | returns - quote , author
def generate_quote():
    key=uuid.uuid4()
    parameter={
        'method':'getQuote',
        'format':'json',
        'lang':"en" ,
        'key':key
    }
    quote_url="http://api.forismatic.com/api/1.0/"

    while True:
        try:
            response=requests.get(quote_url,params=parameter)
            if response.status_code == 200:
                data=response.json()
                quote=data.get("quoteText")
                author=data.get("quoteAuthor","Unknown")#sometimes we don't have author
                return (quote,author)
            
        except requests.exceptions.ConnectionError:
            quit("No internet connection. Connect to a network")
        except:
            print("Something went wrong, While getting the quote\n Retrying...")
    #--usage talks to the api and a quote return : (quote,author)


#Pexels Api gives the image url , then get the image using the url
def generate_image():
    randomPageNo =randint(1,500) #there is no random ,this api is like a static website , So i am creating the randomness
    PexelsApik= "generate-yours"
    url=f'https://api.pexels.com/v1/search?query=nature&page={randomPageNo}&per_page=1&w=800'
    header={   'Authorization':PexelsApik  }
    reponse=requests.get(url,headers=header)
    data=reponse.json()
    image_url=data["photos"][0]["src"]["original"]
    print("Link of generated image(Pexels) : ",image_url)
    return image_url
    #--usage get a image for the api and saves it with the name "generated_img.jpeg"--
   

def edit_image(img_url,quote,author): #using cloudinary api
    try:
        response = cloudinary.uploader.upload(img_url)
    except:
        print("Error in uploading image")
    public_id = response['public_id']
    # Create the transformation URL with the text overlay
    transformation = [
    {'width': 600, 'crop': "auto" ,'height':450},
    {'overlay': {'font_family': "Arial", 'font_size':35, 'font_weight': "normal", 'text': f"“ {quote} ”\n\n\t\t   - {author}",'effect': 'sharpen'}, 'width': 550,'crop': "fit",'color': '#ffffff','background': '#737373'},
    {'flags': "layer_apply"}
    ]

    # Appling the changes and Getting the URL of the transformed image
    limit=5
    for count in range(limit):
        try:
            transformed_image_url = cloudinary.CloudinaryImage(public_id).build_url(transformation=transformation)
            break
        except:
            if(count==limit-1):
                quit("quiting the program")
            print("Something went wrong during transformation, Retrying..")
    print(transformed_image_url)
    #downloading the image
    f_image_data=requests.get(transformed_image_url) 
    if f_image_data.status_code != 200:
        quit("Something went while editing")   
    f_image_ob=BytesIO(f_image_data.content)
    image=Image.open(f_image_ob)
    imgName="final_img.jpeg"
    image.save(imgName)
    #edits the image and saves it as final_img.jpeg

#executer
def execute():
    quote,author=generate_quote()
    img_url=generate_image()
    edit_image(img_url,quote,author)