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

  1. First steps, let's create a repository on GitHub! Make sure to include a README.md, a License and a `.gitignore`
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



