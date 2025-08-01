from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import torch
import cv2
import ollama
import base64
import ultralytics

def moondream2(image,prompt,model):
    response=model.query(image, prompt)["answer"]

    return response
# model_id = "vikhyatk/moondream2"
# revision = "2024-08-26"  # Pin to specific version
# # model = AutoModelForCausalLM.from_pretrained(
# #     model_id, trust_remote_code=True, revision=revision
# # )

# # # # For gpus 
# model = AutoModelForCausalLM.from_pretrained(
#     model_id, trust_remote_code=True, revision=revision,
#     torch_dtype=torch.float16
# ).to("cuda")

# tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

# # image = Image.open('logo.png')
# enc_image = model.encode_image(image)
# print(model.answer_question(enc_image, "Describe this image.", tokenizer))
def tinyVision(vmodel,frame,prompt,tokenizer):
    enc_image = vmodel.encode_image(frame)
    responcse=vmodel.answer_question(enc_image, prompt, tokenizer)
    return responcse

import ollama

# prompt="Elaborate what is happeing in the image(situation), what action are being taken and also provide information on the individual avaible in the image"

# frame=cv2.imread("image.jpg")
# if frame is None:
#     raise ValueError("Image not found or failed to load")
# img = cv2.resize(frame, (512, 512))
# color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
# pil_image = Image.fromarray(color_coverted) 
# # # Encode image as JPEG
# success, buffer = cv2.imencode('.jpg', frame)
# img_base64 = base64.b64encode(buffer).decode('utf-8')
def ollama_model(prompt,image):
    #prompt3="Analyze the description {response}. If any of these conditions are identify. 1: Check for weapons, knife any other kind of weapons. 2: person is smoking, cigerete. 3: Person lying on the floor or person fallen. 4: Violence; if any are present, Just response with 'Yes'or 'No'."
    #image.show()
    #print(prompt3)
    res=ollama.chat(
    model='gemma3:4b',
    messages=[
        {
            'role':'user',
            'content':prompt,
           'images':[image]
        }
    ]
    )
    return res['message']['content']


def ollama_QA(text):
    #prompt3="Analyze the description {response}. If any of these conditions are identify. 1: Check for weapons, knife any other kind of weapons. 2: person is smoking, cigerete. 3: Person lying on the floor or person fallen. 4: Violence; if any are present, Just response with 'Yes'or 'No'."
    #image.show()
    #print(prompt3)
    prompt = f"""
        Analyze the following description of an image carefully. Based only on clear, direct evidence in the text, does it mention any of the following:

        - Guns or firearms e.g., pistol, rifle etc
        - Other weapons like a knife, a bat, a wire, any utility tool or hammer , wrench etc
        - Violence of any kind and hitting , strangling or choking a person 
        - Anything in the mouth of person
        - Smoking or smoke-related activity (e.g., cigarette, vaping, pipe)
        - A person lying on any kind of floor or ground 
        - A person who has injured or collapsed.
        - A person arms raised or saving him or avoiding or fighting stance
        IMPORTANT:
        - Only respond with "yes" if any of these is **explicitly and clearly described**.
        - Respond with "no" if **none** of these are confidently present or the evidence is ambiguous.
     
        Image description:
        \"\"\"{text}\"\"\"
        """
    res=ollama.chat(
    model='gemma3:4b',
    messages=[
        {
            'role':'user',
            'content':prompt,
        }
    ]
    )
    return res['message']['content']

# response=tinyVision(model,pil_image,prompt,tokenizer)
# print(response)
# res=ollama_model(prompt,img_base64,response)
# print(res)


# cap = cv2.VideoCapture(0)

# # Check if camera opened successfully
# if (cap.isOpened()== False):
#     print("Error opening video file")

# # Read until video is completed
# while(cap.isOpened()):
    
# # Capture frame-by-frame
#     ret, frame = cap.read()
#     if ret == True:
#     # Display the resulting frame
#         cv2.imshow('Frame', frame)
#         color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
  
#         # Displaying the Scanned Image by using cv2.imshow() method  
  
#         # Displaying the converted image 
#         pil_image = Image.fromarray(color_coverted) 
#         response=llava_model(prompt,pil_image)
#         print(response)
#     # Press Q on keyboard to exit
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

# # Break the loop
#     else:
#         break

# # When everything done, release
# # the video capture object
# cap.release()

# # Closes all the frames
# cv2.destroyAllWindows()