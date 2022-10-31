from diffusers import StableDiffusionPipeline
from hf_token import hf_token

if hf_token == "YOUR_HF_TOKEN":
    # read users token from cli
    hf_token = input("Please enter your HuggingFace token: ")

try:
    # grab the model from HF using your token
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4", 
        use_auth_token=hf_token
    )

    # save the model
    pipe.save_pretrained("model")

except OSError as e:
    print(e)
    print("Invalid Token, Please Try Again")

