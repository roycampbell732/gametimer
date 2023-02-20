#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue, Feb 7, 2023

@author: roy campbell
"""

# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

# import views
import gametimer

app = gametimer


if __name__ == '__main__':

    app.run_timer()
