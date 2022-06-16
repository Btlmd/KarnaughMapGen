# 最简与或表达式的计算

数电开卷了，因此我们应当避免考试时额外的计算。

像卡诺图这种只有不超过 $3^{16}=4304,6271$ 种答案的问题，我们应当进行预计算。

先修改 `Karnaugh.py` 中的长度参数，路径参数及高位低位设置，然后运行

文件会以多级目录树的形式保存在配置的路径中。

```bash
python Karnaugh.py
```

## 参见

Quine McCluskey 算法的实现参见 [kmaps_solver_tkinter](https://github.com/ttopal/kmaps_solver_tkinter) 。在其基础上进行了一定改动。

## 后记

图形学搓 GAN 失败，今天搓 QM 失败。我是如此的菜以至于我可能只配写 dataloader 罢了，设计或者实现算法我还是洗洗睡吧 x

另外，有兴趣的可以看看 [密码学的表](https://github.com/Btlmd/CryptographyTables/) 。说不定选课的时候也能用上 x
