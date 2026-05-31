# Copyright (C) 2026  macmarrum (at) outlook (dot) ie
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from redmine_client import RedmineClient, RedmineProject

from settings import Env, Settings

s = Settings.of(Env.local)


def print_project_tree():
    pid_to_children = {}

    def print_tree(client: RedmineClient, parent_id: int | None = None, depth=0):
        indent = '  ' * depth
        child_projects: list[RedmineProject] = pid_to_children.get(parent_id, [])
        for proj in child_projects:
            print(f"{indent}{proj.identifier}")
            for isu in client.get_issues(proj.id):
                print(f"{indent}- ({isu.id}) {isu.subject}")
            print_tree(client, proj.id, depth + 1)

    with RedmineClient(s.base_url, s.api_key) as c:
        project: RedmineProject
        for project in c.get_projects():
            pid = project.parent.id if project.parent else None
            pid_to_children.setdefault(pid, []).append(project)
        print_tree(c, parent_id=None)  # start with top-level projects
    pass


print_project_tree()
