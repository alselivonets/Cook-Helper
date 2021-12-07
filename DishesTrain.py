from azure.cognitiveservices.vision.customvision import training
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient 
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageFileCreateBatch
from msrest.authentication import ApiKeyCredentials
from msrest.exceptions import HttpOperationError

import os, time

endpoint = "https://northeurope.api.cognitive.microsoft.com/"
training_key = "32628b16a55341f599ae71076635c65f"
training_images = "Food_Dataset"

credentials = ApiKeyCredentials(in_headers={"training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint=endpoint, credentials=credentials)

#Wyświetlamy listę wszystkich domenów, żeby zdecydować nad tym, jaki będzie pasował do naszych wymagań   
# for domain in trainer.get_domains():   
#    print(domain.id, "\t", domain.name)

project = trainer.create_project("CookHelper - v1","c151d5b5-dd07-472a-acc8-15d29dea8518")

list_of_images = []
dir = os.listdir(training_images)
for tagName in dir:
  tag = trainer.create_tag(project.id, tagName)
  images = os.listdir(os.path.join(training_images,tagName))
  for img in images:
   with open(os.path.join(training_images,tagName,img), "rb") as image_contents:
    list_of_images.append(ImageFileCreateEntry(name=img, contents=image_contents.read(), tag_ids=[tag.id]))
    
# Upload the images in batches of 64 to the Custom Vision Service

for i in range(0, len(list_of_images)-1, 64):
    try:
     upload_result = trainer.create_images_from_files(project.id, batch=ImageFileCreateBatch(images = list_of_images[i:i + 64], tag_ids=[tag.id]))
     
    except HttpOperationError as e:
     print(e.response.text)
     exit(-1)
    print("Wait...")
 	
  
# Train the model
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print(f'{iteration.status} Training status:' ) 
    time.sleep(1)

# Publish the iteration of the model
publish_iteration_name = 'CookHelperItr'
resource_identifier = '546ce298309f4867b39e7d18edbde621'
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, resource_identifier)