# 如何部署到四台测试机

```sh
fab deploy

# 分别进入四台测试机, 执行以下命令...
# 5.50
cd /src/ethereum-bft && python3 -m make server_run0
# 5.51
cd /src/ethereum-bft && python3 -m make server_run1
# 5.52
cd /src/ethereum-bft && python3 -m make server_run2
# 5.53
cd /src/ethereum-bft && python3 -m make server_run3
```


```sh
# 关闭所有节点
fab stop
```
