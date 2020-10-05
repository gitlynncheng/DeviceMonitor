import json
import requests
import time,re
import subprocess
from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for

# 從其他.py裡import的內容
from main import app, db
from models import Permission, Role, User
from decorators import permission_required, admin_required

# login功能使用
from models import login_manager
from flask_login import login_required

from datetime import datetime


subvirtmgr = Blueprint('subvirtmgr', __name__)

@subvirtmgr.route('/virtmgr')
@login_required
@permission_required(Permission.Monitor)
def virtmgr():
    
    return render_template("virtmgr.html", current_time=datetime.utcnow())
