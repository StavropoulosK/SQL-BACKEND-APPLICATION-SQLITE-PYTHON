# SQL-BACKEND-APPLICATION-SQLITE-PYTHON

This is the group project for the course Data Bases of year 2023-2024 of Stavropoulos Konstantinos and Panagiotis Housos.
It is the backend application for a tennis club and it is meant to be accessed by the club secretary to sign up new members,
sign them up to classes or book private lessons with a golf tutor and handle as well all payments. We have also built a python simulation that fills
the database for the year 2023-2024. Beyond the simulation for that year, one can easily use the application to create a new member (NEW MEMBER)
and book for them a reservation for a tennis court (RESERVATION) so they can play with a friend or even with a tutor. Also, the application handles
the payments for all the reservations (PAYMENT).

To run the application you need to have sqlite installed. Also, it is necessary to download the required libraries to do the following imports

import os<br />
import random<br />
import sqlite3<br />
from random import randint as ran<br />
import time<br />
import datetime<br />
from datetime import date, timedelta<br />
import tkinter as tk<br />
from tkinter import ttk<br />
from tkinter import messagebox<br />
import unicodedata as ud<br />

The project tree must have the following order




-readme.txt<br />
-project-<br />
	  -project.db<br />
	  -project.sql<br />
-python-<br />
	  -project.py<br />
	  -arxia_gia_prosomiosi-<br />
			     -andrika_eponima.txt<br />
			     -andrika_onomata.txt<br />
			     -dieuthinsi.txt<br />
			     -ginaikia_eponima.txt<br />
           -ginaikia_onomata.txt


The file project->project.sql contains the sql code for the creation of the sqlite database

The Database has already been created and should be in the file
project->project.db

The folder python->arxia_gia_prosomiosi contains files with names for the creation of person profiles for simulation

The file python->project.py contains the code to run the application

We just write Gui() at the bottom of the program python->project.py
to start the application. If we want to run the simulation program that
fills all arrays from the beginning we write Simulate().In the Simulate class at
constructor we can set the desired parameters of the simulation.


