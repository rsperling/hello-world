---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.jpg')
---

![bg left:40% 80%](https://www.kloia.com/hubfs/devops-workshop.png)

# **DevOps Workshop**



https://marp.app/

---

# Workshop-as-Code

Let's build the environment

```


Split pages by horizontal ruler (`---`). It's very simple! :satisfied:

```markdown
# Slide 1

foobar

---

# Slide 2

foobar
```





# Welcome to the DevOps Workshop

Get ready to pipeline and to be introduced to he magic of automation, containers, IaC (Infrastructure-as-Code), revision control, and observability.

```text
┌──────────┐     ┌────────────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Code:   │     │  Version Control:  │      │  Build:      │      │  Release:    │      │  Operate:    │
│          │     │                    │      │              │      │              │      │              │
│  VSCode  ├────►│  GitHub            ├─────►│  Docker      ├─────►│  Watchtower  ├─────►│  Prometheus  │
│          │     │                    │      │  Docker Hub  │      │  Docker Hub  │      │  Grafana     │
└──────────┘     └────────────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
```

## Environment Registry

### Claim an environment

https://bit.ly/3t4YwXv

## Getting Started

### Prerequisite Tasks

1. Register with the DevOps Slack Workspace (http://slack.quokka.ninja)

2. Claim a User Env and Fake Switch in the Environment Registry

3. Open your claimed workspace by clicking on the Dev Env URL in the sheet

4. Test that you can SSH to your designated switch from the Terminal.

   1. To access the terminal us the shortcut CTRL+SHIFT+`
   2. Copy and paste the ssh comment form Column I in the spreadsheet for your assigned env into your terminal window

5. Create a GitHub account (if you don't already have one)

   1. https://github.com/

6. Create a Docker Hub Account (if you don't' already have one)

   1. https://hub.docker.com/

7. Connect Docker Hub to GitHub to automate builds on Git commits
   1. https://docs.docker.com/docker-hub/builds/link-source/

### Hello World

8. Let's make sure we can successfully run a container

   ```bash
   cd ./code/hello-world
   docker-compose up -d --build
   ```

9. Let's check the container started and is running

   ```bash
   docker ps
   ```

   ```bash
   docker logs -f hello-world

     ___________________
   | 04/05/2021 15:55:27 |
     ===================
                     \
                     \
                        ^__^
                        (oo)\_______
                        (__)\       )\/\
                           ||----w |
                           ||     ||
    _   _        _  _         __        __              _      _  _
   | | | |  ___ | || |  ___   \ \      / /  ___   _ __ | |  __| || |
   | |_| | / _ \| || | / _ \   \ \ /\ / /  / _ \ | '__|| | / _` || |
   |  _  ||  __/| || || (_) |   \ V  V /  | (_) || |   | || (_| ||_|
   |_| |_| \___||_||_| \___/     \_/\_/    \___/ |_|   |_| \__,_|(_)
   ```

   _NOTE: CTRL-C to break viewing the logs, or you can just open another terminal window._

10. Verify the flask app is running.

    ```html
    http://localhost:5000
    ```

11. Change the message by editing message.txt and rebuild and deploy the contianer

    ```bash
    docker stop hello-world
    docker-compose up -d --build
    docker logs -f hello-world
    ```

12. Create a GitHub repo called hello-world

13. Configure Git in your workspace

    ```bash
    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    ```

14. Commit hello-world to your newly created GitHub Repo

    _Note: Make sure you are in the hello-world directory._

    ```text
    git init
    git add . -A
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/[YOUR_GITHUB]/hello-world.git
    git push -u origin main
    ```

15. Create a Docker Hub Repository

    1. Name: hello-world
    2. Public
    3. Build Settings
       1. Click GitHub Logo
          1. Select Organization (aka your GitHub account)
          2. Select Repository (hello-world, this is the repo we just committed to.)
          3. Click the + to add a build rule
             1. Change the branch to "main"
    4. Click "Create & Build"

16. Stop the hello-world container

    ```bash
    docker stop hello-world
    ```

17. Modify the docker-compose.yml file use the docker image from DockerHub

    ```diff
    version: "3"
    services:
    hello-world:
       ### local build ###
    -   # build:
    -     # context: .
    -     # dockerfile: Dockerfile
       ### pull image from docker hub ###
    +   image: [DOCKER_HUB_ACCOUNT]/hello-world:latest
       ### required for flask app ###
       ports:
       - 5000:5000
       container_name: hello-world
       restart: unless-stopped
    ```

18. Start the Hello-World container

    ```bash
    cd ./code/hello-world
    docker-compose up -d --build
    ```

    _Note: For this to work your Docker Hub image has to be build and available. This can take a few minutes, so monitor the build and image availability before proceeding to this step._

19. Start Watchtower

    ```
    cd ./code/watchtower
    docker-compose up -d
    ```

20. Modify the message in message.txt

21. Commit changes to GitHub
    _The easy way._

    ```bash
      cd ./code/hello-world
      ../commit.sh "commit message"
    ```

### Once the commit happens, Docker Hub will rebuild the images, Watch tower will see a new image and will redeploy the container.

_Note: This all take a few minutes._

22. Monitor the hello-world container from the termina

    ```bash
    docker ps
    ```

    1. View hello-world container console output

    ```bash
    docker logs -f hello-world
    ```

    2. View flask app http output

    ```http
    http://localhost:5000
    ```

### Ansible for Switch Configuration.

1. Test connection to your switch

   ```bash
   ssh root@devops-workshop.quokka.ninja:2201

   ```

   _Username: root_
   _Password: root_

   ```bash
   show run
   ```

2. Let's config the switch with Ansible

   ```bash
   cd ./code/switch-ansible-example
   ```

   1. Modify the "inventory" file, remove all switches, except for the switch you are working with. Be kind to your fellow learners.
      _Note: You can simply comment the switches which are not yours._

   2. Validate example-playbook.yml

      ```bash
      ansible-playbook example-playbook.yml --check
      ```

   3. Run example playbook

      ```bash
      ansible-playbook example-playbook.yml
      ```

## Group GameDay Activities

1. Create an Anisble playbook, containerize it, and connect it to a pipeline like we did with hello-world. Make changes to your playbook, commmit to Git and watch the configurations be applied to your switch.

   1. Document a desired state switch configuration.
   2. Create an Ansible playbook to apply you desired state configuration.
   3. Containerize your Ansible playbook and connect it to a pipeline.
   4. Make changes to your Ansible config, commit to GitHub and have the configs applied to your switch.

#TODO

## INSERT INTRO TO SWITCH-WATCH HERE

2. Connect switch-watch and your Ansible playbook to monitor your switch for deviations from the desired state and reapply you desired state configuration.

## Noteworthy Helpers

- Commit Script

  ```sh
  ./code/commit.sh "commit message"
  ```

- Cleanup All Containers **(BE CAREFUL)**

  ```sh
  ./code/nuke.sh
  ```
