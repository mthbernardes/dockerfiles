# Dockerfiles
This repository is a hub of all redteam dockerfiles

# CircleCI status
[![CircleCI](https://circleci.com/gh/mthbernardes/dockerfiles.svg?style=svg&circle-token=fe140f9c65f17844b71630d362c58e215e9e22ce)](https://circleci.com/gh/mthbernardes/dockerfiles)

# New image
To add a new docker image create a new branch with a directory inside `images/` using the name of the desired image. Put all the necessary files and Dockerfile inside it.
```
├── test-image
│   ├── Dockerfile
│   └── config
│       └── conf.yml
```
Then open a new pull request and merge it using the option `merge and squash`.

# CircleCi Job
After you merge a pull request to master a pipeline will be trigged on circleci. This pipeline will check new images and changed images then build and publish it.
