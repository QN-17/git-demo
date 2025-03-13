'''## 导入库
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_california_housing  # 使用加利福尼亚房价数据集替代已移除的波士顿房价
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 加载数据集
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name='MedHouseVal')  # 中位数房价

# 查看数据前5行
print("【数据样例】")
print(X.head())
print("\n目标变量（房价）：\n", y.head())

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n【多元线性回归结果】")
print(f"MAE（平均绝对误差）: {mae:.2f}")
print(f"MSE（均方误差）: {mse:.2f}")
print(f"R²（决定系数）: {r2:.2f}")

# 可视化预测值与真实值对比
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)  # 绘制对角线
plt.xlabel("真实房价")
plt.ylabel("预测房价")
plt.title("多元线性回归预测结果")
plt.show()
'''
'''
# 导入库
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns

# 加载数据集（此处为示例，实际糖尿病数据集更适合二分类，这里调整目标为二分类）
diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
y = (diabetes.target > 140).astype(int)  # 将血糖值>140定义为高风险（二分类）

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练模型（增加max_iter避免收敛警告）
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("\n【Logistic回归结果】")
print(f"准确率: {accuracy:.2f}")
print("\n混淆矩阵:")
print(cm)
print("\n分类报告:")
print(report)

# 可视化混淆矩阵
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['低风险', '高风险'], 
            yticklabels=['低风险', '高风险'])
plt.xlabel("预测标签")
plt.ylabel("真实标签")
plt.title("糖尿病风险预测混淆矩阵")
plt.show()
'''
