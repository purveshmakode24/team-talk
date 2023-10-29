# TeamTalk
TeamTalk - Join teams and engage in discussions

- A simple SAAS based discussion platform backend services using DRF Viewsets.
- Users can join multiple teams created by admins and engage in topic discussions.

## Overview
1) User Registration and Team Creation:
   - Only registered users can create a team.
   - The user who creates a team automatically becomes the admin of that team.

2) Team Membership:
   - Any logged-in user can join a team.
   - When a user joins a team, they have the role of a regular user.

3) Admin Privileges:
   - Admins can create/delete/edit topics.
   - Admins have the authority to delete any comments made by team members.
     
4) User Interaction with Topics:
   - Regular users who have joined a team (with the role of a regular user) can discuss on topics created by the admin.
   - Regular users can comment on topics and can edit/delete their own comments.
   - Users can like or dislike topics if they wish.
