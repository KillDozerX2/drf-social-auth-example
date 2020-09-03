# Table of Contents
* [Problem](##problem)

## Problem <a name="problem">
You've create ~~a dope~~ (pardon my street) **an amazing** rest api using django-rest-framework and an even more amazing front-end (with your flavour of javascript that is deployed and worked on separately) and you've enabled authentication using username/email and password. Now you'd like your users to sign up/sign in using one or many of the social providers and you're trying to find a way of doing this but every tutorial/documentation you read comes with it's own templates and uses sessions but your app doesn't have the concept of sessions as everything is happening through ajax.  
**If that's the case you've come to the right place.**

## What we'll be creating
In this tutorial, we'll create a bare metal api using django and django rest framework that hides some secret data that only authenticated users can see. We won't be implementing username/password login as it fairly easy to do and frankly, should be a prerequisite.  
We will only implement social login using google and facebook as they're very developer friendly and do not have any business requirements. The backend process is exactly the same for other FIP(Federated Identity Providers).
I have also create an interactive front-end that will walk you through the whole oauth2 flow, but that is also out of scope, you can find it [here](https://killdozerx2.github.io/drf-social-auth-example)

### Libraries that we'll be using
* Django
	* Version - 3.1.1
	* [Documentation](https://docs.djangoproject.com/en/3.1/)
	* Purpose - *duh*

* Django Rest Framework
	* Version - 3.11.1
	* [Documentation](https://www.django-rest-framework.org/)
	* Purpose - *duh*

* Django Rest Knox
	* Version - 4.1.1
	* [Documentation](http://james1345.github.io/django-rest-knox/)
	* Purpose - To generate access tokens for users, you can use any other library, I simply like knox.
	
* Python Social App
	* Version - 
	* [Documentation](https://python-social-auth.readthedocs.io/en/latest/)
	* Purpose - Most of the backend logic used in the app will be handled by this ***amazing library***

## Theory
Here's a little diagram for understanding better.
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/ee8zse5abjhd7ezx2rk7.png)  
I'm going to start by giving most if not all of the credit to [Nate Barbettini](https://twitter.com/nbarbettini) for the amazing oauth2.0 in plain english explanation, you can watch the video [here](https://youtu.be/996OiexHze0), you should definitely watch it.  
This is how the oauth2 workflow will work.
1. User clicks the sign in with social button.
2. Front end app sends a request to the api with the social provider that user selected and the redirect url for that provider.
3. The api sends back the *authorization url*(more on this in a bit)
4. The front end app redirects the user to this url
5. User clicks on confirm/authorize button and the oauth provider redirects the user back to our front-end app, remember the redirect url we sent to the api, the oauth2.0 provider with send the user back to this url along with an authorization code.
6. Our front end sends back the authorization code to our api.
7. Our api sends this authorization code to the oauth provider and requests information about the user.
8. If everything went well and good, the oauth provider will send back the information.
9. We create a user object(if it doesn't already exists and send back an authorization code of our own that our front end code can use to request protected data later.)  
  
Now if you're like me, then you're probably wondering
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/7lwbamz8wp2hliwmpiku.gif)  
That's why we'll be using PSA!!
On our api side, we only have to pass data to psa and it'll do all the work for us, but there are a few caveats.
* Before we send the user an authorization url, we'll have to generate two meaningless strings called session_state and request_state.  
	The session_state gets saved in the session and the request_state gets sent to the user.  
	Why this session state you ask? if some malicious person somehow gets a hold of the authorization code sent back by the oauth provider, they can pretend that they're the user and sign in on their behalf (cue serious drama backtrack).  
	On top of this `state` psa also saves the initial redirect url.  
	PSA also compares the time difference between these two states as oauth2.0 has an expiration on the authorization code sent by the provider.
	But I thought you said **no sessions**? That's where jwt comes in, we'll get this session state that psa generates, create a jwt for this state and send it back to the user so they can save it, you can use any type of storage but the interactive web app uses localstorage(*sighs*)

> Talk is cheap. Show me the code  
> *- Linus Torvalds*  

## Code
This app uses `Pipenv` but you can continue with pip and venv/anaconda whatever you like, just remember to replace the `pipenv` with just `pip`.
* Start by making a new directory and initializing Pipenv. Do this step only if you're using Pipenv
	```bash
	mkdir social_drf
	cd social_drf
	pipenv install
	pipenv shell
	```
	*This will initialize a new virtual environment and start a new shell in that environment*
* Install Django and django-rest-framework
	```bash
	pipenv install django
	pipenv install djangorestframework
	```
* Start a new django project in the same directory and create a new app
	```bash
	django-admin startproject social_drf .
	django-admin startapp secret_view
	```
* Add rest_framework and secret_view to the list of installed apps
* Add a new view that will simply return a response that says. `This is a secret message`