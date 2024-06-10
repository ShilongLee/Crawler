# 服务 - 主流媒体平台爬虫

抖音、快手、哔哩哔哩、淘宝、京东平台爬虫服务器项目。它可以获取这些平台上的公开信息，但请遵守下方的的免责声明。

## 免责声明

本项目的初衷是为了帮助开发者更好地了解和掌握这些平台，也希望能帮助企业和安全工程师了解爬虫手段，提高平台的反爬虫措施，而不是用于非法用途，反对用于任何违反相关法律法规的行为。

仅供学习和研究使用，不得用于任何商业用途或非法目的。使用本项目提供的功能时，用户需自行承担可能带来的一切法律责任。

我们提供的爬虫仅能获取抖音，快手、哔哩哔哩、淘宝、京东等平台上公开的信息，我们强烈反对任何形式的隐私侵犯行为。如果你使用本项目进行了侵犯他人隐私的行为，我们将与你保持距离，并支持受害者通过法律手段维护自己的权益。

使用本仓库的内容即表示您同意本免责声明的所有条款和条件。如果你不接受以上的免责声明，请立即停止使用本项目。

如有侵犯到您的知识产权、侵犯到您的个人隐私等，请立即联系我们， 我们将积极配合保护您的权益。

如有任何问题，可联系我的邮箱 <lishilong0101@gmail.com> 。

## 功能

- 快手、抖音、哔哩哔哩、淘宝、京东平台的爬虫接口
- 获取公开的用户信息，帖子信息等
- 使用简单，支持多种语言使用HTTP调用
- 哔哩哔哩视频[一键下载](docs/api/bilibili/bilibili.md#bilibili视频下载)

## 快速开始

### 使用Makefile

1. 准备好[python](https://www.python.org/)

2. 准备好js运行环境

    ```bash
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
    sudo apt-get install -y nodejs
    ```

3. 执行下列命令

    ```bash
    # 进入项目根目录
    cd Crawler
    make run
    # make run 参数
    #
    # 端口号，默认 8080
    # port=8081
    #
    # 线程数 默认 4
    # thread=4
    ```

4. 查看日志
    日志默认存放在`.log/`目录下，`access.log`和`error.log`为访问日志和错误日志，crawler.log为爬虫日志。

### 使用docker

1. 一键启动

    ```bash
    sudo docker run -d --name crawler -p 8080:8080 shilongli0101/crawler
    # 环境变量
    #
    # 线程数默认值4
    # -e THREADS=4
    ```

2. 查看日志

    ```bash
    sudo docker exec -it crawler /bin/bash
    cat .log/crawler.log # access.log error.log
    ```

首次使用需添加账号，例如：调用`http://localhost:8080/{platfrom}/add_account`添加账号，platfrom取`douyin`、`kuaishou`、`bilibili`、`taobao`、`jd`，接口详情请参考[API 文档](docs/doc.md)。

然后在你的代码中调用API，获取公开的信息。

## 文档

API文档：[API 文档](docs/doc.md)

## 相关项目参考

从以下这些项目中学习并开始了解爬虫，在此特别感谢这些项目的作者，感谢你们的开源和贡献。

- [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)

## 即将支持

- [x] Bilibili
- [ ] 微博
- [ ] 小红书

## 更新记录

更新记录：[更新记录](docs/record.md)

## star 趋势图

- 如果该项目对你有帮助，star一下 ❤️❤️❤️

[![Star History Chart](https://api.star-history.com/svg?repos=ShilongLee/Crawler&type=Date)](https://star-history.com/#ShilongLee/Crawler&Date)

## 贡献

如果你有任何想法或者建议，欢迎提交issue或者pull request。

## 许可

本项目遵循非商业使用许可，详情请见[LICENSE](LICENSE)文件。

---

**注意：** 本项目不承担用户因违反这些使用条件而产生的任何直接或间接的损失或责任。
