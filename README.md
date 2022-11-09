<p align = "center" draggable=”false” ><img src="https://user-images.githubusercontent.com/37101144/161836199-fdb0219d-0361-4988-bf26-48b0fad160a3.png" 
     width="200px"
     height="auto"/>
</p>



## <h1 align="center" id="heading">:wave: Branching out of the Notebook: ML Application Development with GitHub</h1>

Welcome to one of the most used modern development workflows - feature branch development! 

Massive thanks to [DeepLearning.ai](https://www.deeplearning.ai/) for coordinating this event!

## :books: Quick Review

Just a reminder that this repository is going to build off of the previous tutorial which you can find here:

<details>
<summary>Video Tutorials</summary>

  1. [M1 Tutorial](https://youtu.be/wiZWQjjvvyk)
  2. [Windows/WSL2 Tutorial](https://youtu.be/C7fBf33nQ7E)
  3. [Linux Tutorial](https://youtu.be/TePJhh4oRcA)
  
</details>

<details>
<summary>Repositories Used</summary>

  1. [FourthBrain's Intro to MLOps Repo](https://github.com/FourthBrain/software-dev-for-mlops-101)
  2. [deeplearning.ai's FastAPI/Docker Repo](https://github.com/https-deeplearning-ai/machine-learning-engineering-for-production-public/tree/main/course4/week2-ungraded-labs/C4_W2_Lab_1_FastAPI_Docker)
  
</details>

Also, make sure you have an activate Hugging Face account!

Once you've caught up using those you'll have the base knowledge you'll need to get started on this repository!


## :rocket: Let's get started!

### Creating a repository & cloning app content

  1. First steps, let's create a repository on GitHub! You can follow [these](https://docs.github.com/en/get-started/quickstart/create-a-repo) instructionsMake sure to include a README.md, a License and a `.gitignore`
  2. Now, we're going to clone our repository from GitHub using the command: 
  
      ```console
      git clone <YOUR REPO SSH LINK HERE>
      ```
  3. Now we can add this repository as an upstream remote to our local repo with the following command:
  
      ```console
      git remote add upstream git@github.com:FourthBrain/Branching-out-of-the-Notebook.git
      ```
    
  4. Next, we're going to pull this repo into our local using the following command: 
  
     ```console
     git pull upstream main -Xtheirs --allow-unrelated-histories
     ```
     
     <details>
     <summary>Command Explanation</summary>
     
     This command uses two flags:
     
     1. `-Xtheirs` this flag tells git to keep their files, should their be any merge conflicts.
     2. `--allow-unrelated-histories` this flag tells git to not worry about the fact that these are two separate repositories!
     
     </details>
 
 ### Optional: Locally testing our StableDiffusion App!
     
  1. Now that we have the app in our local branch, we'll need to do some set-up before we continue! The first thing we'll want to do is head to [this link](https://huggingface.co/CompVis/stable-diffusion-v1-4) and read/accept the ToS!
  
  2. Next, we'll want to create a Read key on HuggingFace by following [this](https://huggingface.co/docs/hub/security-tokens#:~:text=To%20create%20an%20access%20token,you're%20ready%20to%20go!) process!
  
  3. Now that you have your Hugging Face Read token, you'll want to make a file in the `v1` directory called: `hf_token.py` (this is already in `.gitignore`), which will be a simple `.py` file that only contains one row of code:
  
       ```
       hf_token = "<YOUR TOKEN HERE>"
       ```
       
 4. At this point, your repository should look something like this: 
 
     ![image](https://user-images.githubusercontent.com/19699016/198939212-aabad864-3eba-47f1-90ed-488446713f8f.png)
     
 5. Now we'll want to set-up a local `conda` env using the following command: 
 
     ```console
     conda create --name stable_diffusion_demo python=3.10 pip diffusers
     ```

 6. Once you've create `hf_token.py` and added your read key (again making sure to accept the ToS [here](https://huggingface.co/CompVis/stable-diffusion-v1-4), and set-up your `conda` env, you can run `retrieve_model.py`. This will take a while, and consume ~5GB of space - as it's pulling the v1-4 Stable Diffusion weights from Hugging Face!
 
     ```console
     conda activate stable_diffusion_demo
     cd v1
     python3 retrieve_model.py
     ```
 
 6. Once that is done, you will be able to build the Docker image! This process will take some time (~5min.), and is dependent on your hardware!
 
     ```console
     docker build -t stable_diff_demo .
     ```
    
7. Now that you've built the container - it's time to run it! We'll use the following command to ensure our container removes itself when we stop it!

     ```console
     docker run --rm --name stable_diff_demo_container -p 5000:5000 stable_diff_demo 
     ```
     
8. Head on over to [localhost:5000/docs](http://localhost:5000/docs) to play around with the new model! (CPU inference can take a long time, depending on your hardware. ~3-5min.)

## 🌳 Branching Out!

### Local Developement on a Feature Branch

Now that you've tested your app locally, it's time to add a feature branch do some work, and get ready to merge!

1. First things first we'll want to make a new branch called `feature_branch_img2img`, you'll want to use the command:

     ```console
     git checkout -b feature_branch_img2img
     ```
2. Once you have that done, you can check to make sure you're on the correct branch using the command: 

     ```conole
     git branch
     ```

3. After confirming you're on the correct branch - you can finally add your feature! We're going to add the `img2img` endpoint to our FastAPI application (located in `v1/app/app.py`, using the following code:


     ```python
     # create a img2img route
     @app.post("/img2img")
     def img2img(prompt: str, img: UploadFile = File(...)):
         device = get_device()
         img2img_pipe = StableDiffusionImg2ImgPipeline.from_pretrained("../model")
         img2img_pipe.to(device)

         img = Image.open(img.file).convert("RGB")
         init_img = img.resize((768, 512))

         # generate an image
         img = img2img_pipe(prompt, init_img).images[0]

         img = np.array(img)
         img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
         res, img = cv2.imencode(".png", img)

         del img2img_pipe
         if torch.cuda.is_available():
             torch.cuda.empty_cache()

         return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/png")
     ```
     
4. Once you have updated your `app.py`, you can once again test it using the processed outlined above!

5. Now that we've made the changes - we're ready to stage, and then commit them! First up, let's stage our changes using:

     ```console
     git add .
     ```
     
6. Next up, we'll commit the changes with a useful/helpful message using:

     ```console
     git commit -m "<YOUR HELPFUL MESSAGE HERE>"
     ```
     
7. Now that we've commited those changes - we need to push them to our remote repository. You'll notice that we're setting a new upstream in the upcoming command, that's because while the branch we created on our local exists; the remote is not aware of it! So we need to create the branch on the remote, as well! We can do this in one step with the following command:

     ```console
      git push --set-upstream origin feature_branch_img2img
      ```
      
8. With that, you're all done on the local side! The only thing left to do is navigate to your remote repo on GitHub.com!

### Merging into the Trunk Using a Pull Request!

1. When you arrive at your repository on GitHub.com, you should notice a brand new banner is present:

     ![image](https://user-images.githubusercontent.com/19699016/200868492-32df4085-f280-4ef5-bf1d-dbf9bf734fdb.png)
     
2. Once you click on the green "Compare & pull request" button - you'll be brought to the pull request screen where you'll want to leave an insightful comment, and add an appropriate title (it will use your commit message as a default title!)

     ![image](https://user-images.githubusercontent.com/19699016/200869067-8be34741-b382-4356-9760-e7c57eec7dc2.png)

3. Once you've done that, you can click the green "Create pull request" button!

4. After creating the pull request, you'll see there's an option to assign reviewers - which you can do by clicking the cog wheel icon, and either selecting (or typing) the name of your reviewer! (Remember: they have to be a collaborator on the repository!)

     ![image](https://user-images.githubusercontent.com/19699016/200869575-26297736-6236-477c-a7fa-da61a3139fb3.png)
     
5. After review (usually the reviewer will do this step), you can finally merge your changes into the trunk by clicking the green "Merge pull request" button! It will ask you to confirm, and leave additional comments - which should absolutely do!

     ![image](https://user-images.githubusercontent.com/19699016/200870756-34e2eb59-3440-4084-9fcf-f15fb0950a3c.png)
     
6. Afterwards, it will prompt you if you want to delete the branch. It is dependent on your organization if you will or not - but it is usually considered good practice to delete "hanging" branches!

     ![image](https://user-images.githubusercontent.com/19699016/200871153-5c699924-32fa-4d61-99a2-c15dbac603fa.png)

     

## :tada: Conclusion!

With that, you're all done! 

To recap, we've: Built a web-app based on the Diffusers library, "Dockerized" it, created a feature branch, added a feature, pushed our branch to GitHub, and created a PR!



     

