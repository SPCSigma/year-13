from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error
import logging

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

