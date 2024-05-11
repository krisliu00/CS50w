- 从GitHub上copy需要clone的url下载到本地
  ```
  git clone URL_name
  ```
- 查看GitHub的url
  ```
  git config --get remote.origin.url
  ```
- 文件更新到缓存区
  ```
  git add file_name
  ```
- 确认所有更新
  ```
  git commit -m “some messages”
  ```
- 更新缓存一次性完成，包括所有文件
  ```
  git add --all && git commit -m "comment"
  ```
- 转到branch上
  ```
  git checkout branch_name
  ```
- push the current local branch to the remote repository (origin) and set it as the upstream branch
  ```
  git push --set-upstream origin branch_name
  ```
- 
  ```
  git fetch + git merge = git pull
  ```
- 把xxbranch和目前所在的branch内容合并
  ```
  git merge branch_name
  ```
- 显示commit的数量和内容 q退出
  ```
  git log
  ```
- 删掉本地branch, -D为强制
  ```
  git branch -d branch_name
  ```
- 删除远程branch
  ```
  git push origin --delete branch_name
  ```
- 同时推送main和branch
  ```
  git push origin main branch_name
  ```

