---
title: Useful Git Commands
permalink: /docs/useful-git-commands/
---

## Useful Git Commands

This appendix describes the minimal set of git commands necessary to follow the CSLE contribution workflow 
(see the <a href="./../development-conventions">developer guide</a>.).

When you start working on a new feature, first make sure that you have pulled the latest code changes by 
running the following commands in the root of the CSLE repository:

```bash
git checkout master
git pull origin master
```
<p class="captionFig">
Listing 184: Commands for pulling the latest code changes from the master branch.
</p>

If the above command did not succeed due to code conflicts you can either resolve the conflicts or choose to reset 
the code to the latest commit (this will override any local changes) by running the commands:

```bash
git reset --hard origin/master
git clean -fd
```
<p class="captionFig">
Listing 185: Commands for resetting the local version of the code to the upstream version. 
(Warning: this will override any local changes to the code.)
</p>

Next, create a new branch for your code changes by running the command:

```bash
git checkout -b mybranchname
```
<p class="captionFig">
Listing 186: Command for creating a new branch with name `mybranchname`.
</p>

Then you can make your code changes. When you have made a set of changes you can commit them by running the commands:

```bash
git add --all
git commit -m "comment for the commit"
```
<p class="captionFig">
Listing 187: Commands committing new code changes.
</p>

You can make several commits. When you feel that your new feature is ready to be merged into m
aster you can push the code to GitHub by running the command:

```bash
git push origin mybranchname
```
<p class="captionFig">
Listing 188: Command for pushing the branch `mybranchname` to GitHub.
</p>

After pushing the changes you can go with your web browser to:
<a href="https://github.com/Limmen/csle">https://github.com/Limmen/csle</a>
 and open a new pull request.

When the pull request is merged into the master branch you can delete the local branch and pull the new changes from 
the master branch by running the commands:

```bash
git checkout master
git pull origin master
git branch -d mybranchname
```
<p class="captionFig">
Listing 189: Commands for (1) switching to the master branch; (2) pulling the latest changes; and (3) 
delete the old feature branch with name `mybranchname`.
</p>

After running the above commands you can verify that your commits are available in the master branch by running the command:
```bash
git log
```
<p class="captionFig">
Listing 190: Command for viewing git commits.
</p>