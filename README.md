# DM_LinkAnalysis

摘要 0
1. File structure
2. Implment
3. Graph
4. Result
5. How to Increase Hub, Authority and PageRank?
6. Discussion


Implement2
 HITS
 使用 list 結構記錄每個節點 Authority 和 hub 值,
並且初始化成 1 / n ^ 0.5。
 程式邏輯-進入迴圈
 對每個節點，將其 Authority 更新為其全部父節點之 Hub 值總和。
將其 Hub 更新為其全部子節點之 Authority 值總和。
 將全部 Authority 除以全部 Authority 平方和開根號 (歐基理德距離)
 將全部 Hub 除以全部 Hub 平方和開根號 (歐基理德距離)
 如果新舊 Authority 之差值平方和，加上新舊 Hub 之差值平方和小於
epsilon。(default: 1e‑10)，則跳出迴圈。
 輸出 Authority 及 Hub list。
 PageRank
 使用 list 結構記錄每個節點 PageRank 的值,初始化成 1 / n ^ 0.5。
 程式邏輯-進入迴圈
 對每個節點，將其 PageRank 更新為 d 除以總節點數，加上(1-d)乘以
其全部父節點 PageRank 值除以父節點對外分支數的總和
(default : d=0.1)
 將全部 Authority 除以全部 Authority 平方和開根號 (歐基理德距離)
 將全部 Hub 除以全部 Hub 平方和開根號 (歐基理德距離)
 如果新舊 Authority 之差值平方和，加上新舊 Hub 之差值平方和小於
epsilon。(default: 1e‑10)，則跳出迴圈。
 輸出 Authority 及 Hub list
Data Mining_Project3
_N96094196_張維峻 5
SimRank
 建立一個 dictionary 來儲存節點與節點之間的倆倆 SimRank 值，並初始
化自己對自己的 SimRank 為 1 ，其餘的 SimRank 為 0 。
 程式邏輯-進入迴圈
。 對於全部節點中的倆倆配對 a, b 節點，其中 a 不等於 b ，將
SimRank(a, b) 及 SimRank(b, a) 更新為 C 除以 a 之父節點數，除以
b 之父節點數，乘以全部 a 之父節點配對上全部 b 之父節點之
SimRank 總和。(default: C=1.0)
。 如果更新前後 SimRank 之差值平方和小於 epsilon
(default: 1e‑10)，則跳出迴圈。
 輸出 SimRank dictionary。
