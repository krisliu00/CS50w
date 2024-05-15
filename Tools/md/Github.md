- 从GitHub上copy需要clone的url下载到本地
  ```
  git clone URL_name
  ```
- 查看GitHub的url
  ```
  git config --get remote.origin.url
  ```
- 文件更改提交和撤销功能
  - 文件更新到缓存区
    ```
    git add file_name
    ```
  - 所有上次commit后修改的文件更新到缓存区
    ```
    git add .
    ```
  - 在没有commit之前舍弃缓存区的内容
    ```
    git reset HEAD
    ```  
  - 把工作区内所有的文件都还原为上一次commit的状态（撤销所有更改）
    ```
    git checkout .
    ```  
  - 撤销单个文件的更改，还原为上一次commit的状态
    ``` 
    git checkout file_name
    ```  
  - 工作区的状态和当前HEAD信息
    ```
    git status
    ```  
- 对比文件状态
  - 显示工作区和缓存区的所有更改（对比上一次commit）
    ```
    git diff
    ```
  - 查看缓存区的更改（对比上一次commit）
    ```
    git diff --cached
    ```
  - 查看某个文件暂存区和工作区的差异
    ```
    git diff file_name
    ```



- 确认所有更新
  ```
  git commit -m “some messages”
  ```
- 更新缓存一次性完成，包括所有文件
  ```
  git add --all && git commit -m "comment"
  ```
- 查询commit信息
    - 显示commit的数量和内容 q退出
      ```
      git log
      ```
    - 查询上一次commit的信息
      ```
      git log -n 1
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

