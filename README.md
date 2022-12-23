
<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">


<h1 align="center">Justo Technical Assesment - Back-End</h3>
<h2 align="center">Rodríguez Agiss Zuriel Uzai</h3>

  <p align="center">
    Flask project aimed at creating a hit and hitmen management
    <br />
    <a href="https://github.com/nowhereknight/flask-backend"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/nowhereknight/flask-backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/nowhereknight/flask-backend/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#built-with">Built With</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>




### Built With
* [![Python][Python.com]][Python-url]
* [![Flask][Flask.com]][Flask-url]
* [![Postgresql][PSQL.com]][PSQL-url]
* [![AWS][AWS.com]][AWS-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


## Installation
### Pre-requisites
1. An EC2 Instance up and running. With Amazon Linux preferably
2. A database set with the Hit and Hitmen table created. Check `db.sql` and the following image for reference
![DB Schema](db.png?raw=true "Db Schema")

### Steps
1. Connect to your EC2 instance either via SSH or through the AWS Console
2. Execute the following commands to install needed dependencies in the OS.
```
sudo yum update
sudo yum install python3 python3-pip
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
sudo yum install postgresql-libs
sudo yum install postgresql-devel
```

Note: For Ubuntu/Debian use apt instead
3. Initialize needed env variables with your own credentials. Ask for the administrator/DevOps help if needed
```
    export FLASK_APP=flasky.py
    export FLASK_CONFIG=development
    export DEV_DATABASE_USER=<DEV_DATABASE_USER>
    export DEV_DATABASE_PWD=<DEV_DATABASE_PWD>
    export DEV_DATABASE_HOST=<DEV_DATABASE_HOST>
    export DEV_DATABASE_NAME=<DEV_DATABASE_NAME>
```

4. Clone the repo
   ```
   git clone https://github.com/nowhereknight/hitmen-manager.git
   ```
5. Enter the repository
   ```
   cd flask-backend
   ```
6. Initialize your virtual environment, activate it and install all needed python dependencies
   ```
   python3 -m venv venv
   . venv/bin/active
   (venv) pip3 install -r requirements.txt
   ```
7. Start the flask service
   ```
   flask run --host=0.0.0.0 --port=5000
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Find attatched the:
- [Postman API Documentation](https://documenter.getpostman.com/view/18511827/2s8Z6u6ayy)
- [Postman API Collection](Justo.postman_collection.json). 

```Note: The Postman Collection has to be imported in Postman```

Each include testing evidence as well as a walkthrough the endpoints. Please pay special attention to the test cases included for consideration

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTACT -->
## Contact

Zuriel Uzai Rodríguez Agiss - [![LinkedIn][linkedin-shield]][linkedin-url] - zurieluzai2015@gmail.com

Project Link: [https://github.com/nowhereknight/hitmen-manager.git](https://github.com/nowhereknight/hitmen-manager.git)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/zuriel-uzai-rodr%C3%ADguez-agiss-4a77b8199/
[product-screenshot]: images/screenshot.png
[HTML.com]: https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white
[HTML-url]: https://html.com/
[CSS.com]: https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://www.w3.org/Style/CSS/Overview.en.html
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[JS.com]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JS-url]: https://www.javascript.com/
[Flask.com]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/2.2.x/
[Python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[PSQL.com]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PSQL-url]: https://www.postgresql.org/
[AWS.com]: https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://aws.amazon.com/