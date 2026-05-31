# Copyright (C) 2026  macmarrum (at) outlook (dot) ie
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from redmine_client import RedmineClient, RedmineProject

from settings import Env, Settings

s = Settings.of(Env.local)


def print_project_tree():
    pid_to_children = {}

    def print_tree(client: RedmineClient, pid: int, depth=0):
        indent = '  ' * depth
        for proj in pid_to_children.get(pid, []):
            proj: RedmineProject
            print(f"{indent}{proj.identifier}")
            for isu in client.get_issues(proj.id):
                print(f"{indent}- {isu.subject}")
            print_tree(client, proj.id, depth + 1)

    with RedmineClient(s.base_url, s.api_key) as c:
        project: RedmineProject
        for project in c.get_projects():
            pid = project.parent.id if project.parent else None
            pid_to_children.setdefault(pid, []).append(project)
        print_tree(c, None)
    pass


print_project_tree()
