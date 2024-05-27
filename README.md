# UserProfile_MusicRecommend
基于用户画像以及协同过滤的音乐推荐系统


1.将基于用户的协同过滤算法与用户画像相结合进行推荐，提高推荐列表数据的成熟度。


2.系统在Windows平台上搭建，采用Python3实现各项功能；采取MySQL进行数据的存储，通过Django框架连接系统的前、后端。


3.使用的数据集为kaggle平台上kkbox举办的—KKBox's Music Recommendation Challenge比赛的公开数据集，kkbox是亚洲领先的音乐流媒体服务提供商，
        拥有世界上最全面的亚洲流行音乐库，拥有超过3000万首音乐曲目。
songs.csv
song_extra_info.csv

4.针对数据集使用SVD矩阵分解进行相似相关度的计算分析，根据已有的评分情况，
分析出评分者对各个因子的喜好程度以及歌曲包含各个因子的程度，最后再反过来根据分析结果预测评分，根据评分的结果生成推荐列表。

## Deploy

Create a virtual environment and install dependencies:
```sh
$ pip install -r requirements.txt
```

Migrate database:

```sh
$ py manage.py migrate
```

Run server:

```sh
$ py manage.py runserver
```

Visit http://localhost:8000

## Contributor
<div>
<a href="https://github.com/zhuxiangyualter">
<img src="https://avatars.githubusercontent.com/u/114237571?s=400&u=68d56aba088fac19dec2923c7415a939ec1d1ec5&v=4" height=50px; width=50px;>
</a>
</div>
