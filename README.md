# 成功高中網管 實作題目 登入系統
### 架構
+ 註冊
  - 檢查 `email` `username` 是否已經存在 
  - 錯誤提示
  - 把資料輸入資料庫
+ 登入
  - 檢查是否已經為登入狀態
  - `username` `password`比對資料庫
  - 錯誤提示
+ 登出
  - 檢查是否已經為登出狀態
+ 資料庫
  - Mongodb compass
  - 檢查是否正連線

---
### 筆記區

#### is_authenticated vs. is_active
is_authenticated
登入成功時return True(這時候才能過的了login_required)   

is_active
帳號啟用並且登入成功的時候return True 
可以使用 is_active 標誌阻止用戶登錄，而無需改變其密碼、刪除其帳戶或執行其他重大操作




#### mongodb一些函示
資料來源 https://www.cnblogs.com/shenh/p/16784599.html

增
mongo.db.user.insert_one()
mongo.db.user.insert_many()

 刪
mongo.db.user.delete_one()
mongo.db.user.delete_many()

 改
mongo.db.user.update_one()
mongo.db.user.update_many()

 查
mongo.db.user.find()    # 返回一個cursor對象，可以使用for循環進行遍歷
mongo.db.user.find_one()    # 返回一個dict對象

 計數
mongo.db.user.find().count()


 排序
mongo.db.user.find().sort('name', pymongo.ASCENDING)


 偏移，限制
mongo.db.user.find().sort('age', 18).skip(2).limit(3)



#### jQuery 選擇器
基本選擇器

$ ("element")：選出所有該 element 的節點
例如：$(“p”) ：選出所有 <p> </p>的節點

$(“#divId”)：選出所有 <div id=”divId”></div> 的節點

$(“.divClass”)：選出所有 <div class=”divClass”></div> 的節點
