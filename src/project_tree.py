# Copyright (C) 2026  macmarrum (at) outlook (dot) ie
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from redmine_client import RedmineClient, RedmineProject
from settings import Env, Settings

s = Settings.of(Env.local)


def get_project_hierarchy(client: RedmineClient) -> dict[int | None, list[RedmineProject]]:
    pid_to_children = {}
    for project in client.get_projects():
        pid = project.parent.id if project.parent else None
        pid_to_children.setdefault(pid, []).append(project)
    return pid_to_children


def walk_project_tree(client: RedmineClient, pid_to_children: dict[int | None, list[RedmineProject]], parent_id: int | None = None, level=0):
    child_projects: list[RedmineProject] = pid_to_children.get(parent_id, [])
    for proj in child_projects:
        yield proj, level
        yield from walk_project_tree(client, pid_to_children, proj.id, level + 1)


def print_project_tree():
    with RedmineClient(s.base_url, s.api_key) as client:
        pid_to_children = get_project_hierarchy(client)
        for proj, level in walk_project_tree(client, pid_to_children, parent_id=None):  # start with top-level
            print(f"{'  ' * level}{{{proj.id}}} {proj.identifier}")
            for isu in client.get_issues(proj.id, subproject_id='!*'):
                print(f"{'  ' * (level + 1)}- ({isu.id}) {isu.subject}")
    pass


print_project_tree()
