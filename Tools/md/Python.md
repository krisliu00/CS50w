- 引用数据库数据时，`get_object_or_404（）`返回的是一个单一的模型实例， 在template里可以直接用.field来引用，比如`{{ auction.image_url }}`

- `AuctionList.objects.filter()`返回的是QuerySet，包含所有符合条件的实例，即使只有一个实例，也需要用遍历来引用，比如
    ```
    {% for obj in auctions %}
    {{ obj.category }}
    {% endfor %}
    ```
- **list comprehension** 列表推导式:`[expression for item in iterable if condition]` 自动append, 具体例子可以看project commerce/app auctions里的index或watchlist views
- **list**: `list = [1, 2, 3, 4, 5]` 需要用`list.append(somethingnew)`来加新的元素*elements*或项*items*
- `title()` 返回一个字符串的副本，其中所有单词的第一个字符都被大写，而字符串方法 `capitalize()` 返回一个字符串的副本，其中只有整个字符串的第一个单词被大写。
