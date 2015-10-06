#!/usr/bin/env python

from ProjectFinder import ProjectFinder
from Project import Project
import sqlite3

DATA_POINTS = 100
BEGIN_AT = 24

projectFinder = ProjectFinder()
collected = 0
con = sqlite3.connect("db")
cursor = con.cursor()
id = 0
while collected < DATA_POINTS:
    projects = projectFinder.get_projects()
    collected += len(projects)
    if id < BEGIN_AT:
        id += collected
        continue
    for project in projects:
        project.generate_stats()
        avg_line_length = 0
        if project.nzero_line_count > 0:
            avg_line_length = project.nzero_line_sum / project.nzero_line_count
        cursor.executescript("INSERT INTO codestats (id, url, accessed_time, curly_same, curly_next, curly_other, paren_prec_space, paren_no_prec_space, whitespace_spaces, whitespace_tabs, avg_line_length, max_line_length, line_count) VALUES (%i, '%s', '%s', %i, %i, %i, %i, %i, %i, %i, '%d', %i, %i)" % (id, project.url, project.accessed_time, project.curly_same, project.curly_next, project.curly_other, project.paren_prec_space, project.paren_no_prec_space, project.whitespace_spaces, project.whitespace_tabs, avg_line_length, project.nzero_line_max, project.nzero_line_count))
        id += 1
