#!/bin/bash

sleep 300

celery -A Conferences worker -l INFO -B


